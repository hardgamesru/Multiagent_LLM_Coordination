"""Offline transport, accounting, recovery and coordination-interface tests."""
import csv
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from .adapter import load_backend
from .catalog import get_tasks
from .ledger import Ledger,IntegrityStop
from .transport import MeteredClient,SDKTransport,MAX_OUTPUT
from .runner import create_run,execute,export


def response(content='def f(): return 1',usage=None):
    return {'model':'provider-resolved-test-version',
            'choices':[{'finish_reason':'stop','message':{'content':content}}],
            'usage': {'prompt_tokens':20,'completion_tokens':10,'total_tokens':30} if usage is None else usage}


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.path=Path(self.temp.name)/'ledger.sqlite3'
        self.ledger=Ledger(self.path,1000,850)

    def tearDown(self):
        self.ledger.close()
        self.temp.cleanup()

    def reserve(self,key='a',amount=100):
        return self.ledger.reserve(key,'exp','eval','model','endpoint','hash',amount,50)

    def test_persistence_replay_and_no_duplicate_charge(self):
        self.reserve()
        self.ledger.settle('a',response(),1)
        self.ledger.close()
        self.ledger=Ledger(self.path,1000,850)
        self.assertEqual(self.reserve()['model'],'provider-resolved-test-version')
        self.assertEqual(self.ledger.totals()['actual'],30)
        with self.assertRaises(IntegrityStop):
            self.ledger.settle('a',response(),1)

    def test_shared_models_budget_and_reservation(self):
        self.reserve(amount=700)
        self.assertEqual(self.ledger.totals()['reserved'],750)
        with self.assertRaises(IntegrityStop):
            self.reserve('b')
        self.ledger.settle('a',response(usage={'prompt_tokens':700,'completion_tokens':50,'total_tokens':750}),1)
        with self.assertRaises(IntegrityStop):
            self.ledger.reserve('b','e','v','other_model','endpoint','h',100,50)

    def test_crash_before_response_never_retries(self):
        self.reserve()
        self.ledger.close()
        self.ledger=Ledger(self.path,1000,850)
        with self.assertRaises(IntegrityStop):
            self.reserve()
        with self.assertRaises(IntegrityStop):
            self.reserve('new')

    def test_missing_inconsistent_negative_and_overbound_usage(self):
        for i,usage in enumerate([{}, {'prompt_tokens':1,'completion_tokens':2},
                {'prompt_tokens':1,'completion_tokens':2,'total_tokens':4},
                {'prompt_tokens':-1,'completion_tokens':2,'total_tokens':1},
                {'prompt_tokens':101,'completion_tokens':1,'total_tokens':102}]):
            with self.subTest(usage=usage),tempfile.TemporaryDirectory() as tmp:
                ledger=Ledger(Path(tmp)/'x.db',1000,850)
                ledger.reserve('x','e','v','m','url','h',100,50)
                with self.assertRaises(IntegrityStop):
                    ledger.settle('x',response(usage=usage),0)
                saved=ledger.db.execute('SELECT * FROM requests').fetchone()
                self.assertEqual(saved['state'],'unknown')
                if not usage:
                    self.assertIsNone(saved['total_tokens'])
                with self.assertRaises(IntegrityStop):
                    ledger.reserve('y','e','v','m','url','h',1,1)
                ledger.close()

    def test_prompt_drift_and_config_change_rejected(self):
        self.reserve()
        self.ledger.settle('a',response(),1)
        with self.assertRaises(IntegrityStop):
            self.ledger.reserve('a','exp','eval','model','endpoint','otherhash',100,50)
        with self.assertRaises(IntegrityStop):
            Ledger(self.path,2000,850)

    def test_unknown_transport_usage_stays_reserved(self):
        self.reserve()
        self.ledger.unknown('a')
        self.assertEqual(self.ledger.totals(),{'actual':0,'reserved':150,'unresolved':1})

    def test_concurrent_connections_prevent_second_flight(self):
        other=Ledger(self.path,1000,850)
        self.reserve()
        with self.assertRaises(IntegrityStop):
            other.reserve('b','e','v','m','url','h',1,1)
        other.close()

    def test_duplicate_pilot_stage_is_rejected(self):
        self.ledger.register_run('pilot','e','folder')
        with self.assertRaises(IntegrityStop):
            self.ledger.register_run('pilot','other','other_folder')


class TransportTests(unittest.TestCase):
    def test_replay_without_transport_or_duplicate_tokens(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger=Ledger(Path(tmp)/'l.db')
            sent=[]
            def send(*args):
                sent.append(args)
                return response()
            for _ in range(2):
                client=MeteredClient('GigaChat-2',ledger,'e','evaluation',send)
                client.generate('system','user')
                self.assertEqual(client.cumulative_total_tokens,30)
            self.assertEqual(len(sent),1)
            self.assertEqual(sent[0][2],4096)
            ledger.close()

    def test_byte_limit_rejects_before_reservation_or_transport(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger=Ledger(Path(tmp)/'l.db')
            def fail(*args):
                self.fail('transport should not be called')
            client=MeteredClient('GigaChat-2',ledger,'e','v',fail)
            with self.assertRaises(IntegrityStop):
                client.generate('s','x'*20000)
            self.assertEqual(ledger.totals()['reserved'],0)
            ledger.close()

    def test_network_failure_is_unknown_and_fatal(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger=Ledger(Path(tmp)/'l.db')
            def fail(*args):
                raise TimeoutError('sensitive error must not leak')
            client=MeteredClient('GigaChat-2',ledger,'e','v',fail)
            with self.assertRaises(IntegrityStop):
                client.generate('s','u')
            self.assertEqual(ledger.totals()['unresolved'],1)
            ledger.close()

    def test_sdk_retries_disabled_offline(self):
        send=SDKTransport('not-a-real-secret')
        self.assertEqual(send.client._settings.max_retries,0)
        send.close()


class RunnerTests(unittest.TestCase):
    def test_all_18_cells_export_recovery_and_private_test_separation(self):
        coordinators,_=load_backend()
        from sandbox_runner import SandboxResult
        tasks={t.task_id:t for t in get_tasks()}
        with tempfile.TemporaryDirectory() as tmp:
            folder=create_run(Path(tmp)/'runs',['GigaChat-2','GigaChat-3-Ultra'],kind='offline-fixture-test')
            ledger=Ledger(Path(tmp)/'offline-only.db')
            calls=[]
            def send(model,messages,max_output):
                current=ledger.db.execute("SELECT evaluation FROM requests WHERE state='pending'").fetchone()[0]
                task=tasks[current.split(':')[-2]]
                text=json.dumps(messages)
                for t in tasks.values():
                    self.assertNotIn(t.hidden_tests,text)
                    self.assertNotIn(json.dumps(t.hidden_tests),text)
                calls.append(current)
                return response(task.reference_source)
            def sandbox(code,tests,**kwargs):
                from .validate import run_source
                run_source(code,tests)
                return SandboxResult(True,'','','',0.01,'passed')
            with patch.object(coordinators,'run_code_in_sandbox',sandbox):
                execute(folder,ledger,send)
                with (folder/'raw_results.csv').open(encoding='utf-8',newline='') as stream:
                    rows=list(csv.DictReader(stream))
                self.assertEqual(len(rows),18)
                self.assertTrue(all(r['status']=='passed' for r in rows))
                self.assertTrue(all(r['protocol_version']=='v3-pilot-1' for r in rows))
                total=ledger.totals()['actual']
                (folder/'raw_results.csv').unlink()
                execute(folder,ledger,lambda *args:self.fail('completed pilot must not resend'))
                self.assertEqual(ledger.totals()['actual'],total)
                self.assertTrue((folder/'raw_results.csv').exists())
                self.assertEqual(len(calls),66)
            ledger.close()

    def test_exception_after_response_replays_then_finishes_evaluation(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger=Ledger(Path(tmp)/'l.db')
            client=MeteredClient('GigaChat-2',ledger,'e','v',lambda *args:response())
            ledger.claim_evaluation('v','e')
            client.generate('s','u')
            ledger.close()  # Simulate interruption before result commit.
            ledger=Ledger(Path(tmp)/'l.db')
            self.assertIsNone(ledger.claim_evaluation('v','e'))
            client=MeteredClient('GigaChat-2',ledger,'e','v',lambda *args:self.fail('duplicate'))
            client.generate('s','u')
            ledger.save_evaluation('v',{'status':'passed'})
            self.assertEqual(ledger.claim_evaluation('v','e'),{'status':'passed'})
            ledger.close()


if __name__=='__main__':
    unittest.main()
