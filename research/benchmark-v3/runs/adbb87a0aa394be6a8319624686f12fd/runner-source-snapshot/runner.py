"""Hash-checked pilot and approved one-repeat main runner."""
import argparse
import csv
from dataclasses import asdict
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import shutil
import sqlite3
import math
import uuid
from .adapter import ROOT,V2,digest,load_backend
from .catalog import get_tasks
from .ledger import Ledger,IntegrityStop
from .transport import ENDPOINT,MAX_OUTPUT,INPUT_ENVELOPE,MAX_PROMPT_BYTES,MeteredClient,SDKTransport

MODELS=['GigaChat-2','GigaChat-3-Ultra']
ARCHITECTURES=['single_agent','feedback_graph','parallel_consensus']
PILOT_TASKS=['v3_03','v3_10','v3_17']


def atomic_json(path,value):
    temp=path.with_suffix(path.suffix+'.tmp')
    with temp.open('w',encoding='utf-8') as stream:
        json.dump(value,stream,ensure_ascii=False,indent=2)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temp,path)


def export(ledger,experiment,folder):
    rows=ledger.results(experiment)
    if not rows:
        return
    target=folder/'raw_results.csv'
    temp=target.with_suffix('.tmp')
    with temp.open('w',newline='',encoding='utf-8') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]))
        writer.writeheader()
        for row in rows:
            writer.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in row.items()})
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temp,target)
    from metrics import write_summary_from_raw
    write_summary_from_raw(target,folder/'summary_results.csv',replace=True)


def execute(folder,ledger,send,backend=None):
    coordinators,hashes=load_backend()
    manifest=json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
    if manifest['source_sha256']!=hashes or manifest['runner_sha256']!=runner_hashes():
        raise IntegrityStop('Source revision changed since experiment creation')
    experiment=manifest['experiment_id']
    repetition=manifest.get('repetition_index',1)
    manifest['shared_ledger_path']=str(ledger.path.resolve())
    tasks={t.task_id:t for t in get_tasks()}
    export(ledger,experiment,folder)  # Recover CSV if interrupted after SQLite commit.
    try:
        if backend:
            # Only offline tests inject a fake sandbox. Paid runs use unchanged backend.
            coordinators.run_code_in_sandbox=backend
        for model in manifest['requested_models']:
            for architecture in manifest['architectures']:
                for task_id in manifest['tasks']:
                    task=tasks[task_id]
                    key=f'{experiment}:{model}:{architecture}:{task_id}:{repetition}'
                    if ledger.claim_evaluation(key,experiment) is not None:
                        continue
                    client=MeteredClient(model,ledger,experiment,key,send)
                    coordinator=coordinators.COORDINATORS[architecture](client,folder/'generated_solutions',max_iterations=3)
                    print(f'{model} {architecture} {task_id}',flush=True)
                    result=asdict(coordinator.run(task,hashlib.sha256(key.encode()).hexdigest()[:16]))
                    requests=list(ledger.db.execute('SELECT finish_reason,latency FROM requests WHERE evaluation=? ORDER BY created',(key,)))
                    result.update(experiment_id=experiment,repeat_index=repetition,protocol_version=manifest['protocol_version'],
                                  requested_model=model,returned_models=client.returned_models,endpoint=ENDPOINT,
                                  finish_reasons=[r['finish_reason'] for r in requests],
                                  request_latency_seconds=[r['latency'] for r in requests],
                                  difficulty=task.difficulty,task_sha256=digest(ROOT/'benchmark_v3/catalog.py'),
                                  source_manifest_sha256=digest(folder/'source-manifest.json'))
                    ledger.save_evaluation(key,result)
                    export(ledger,experiment,folder)
                    if result['status'] in {'sandbox_timeout','sandbox_error','sandbox_unavailable','provider_error'}:
                        raise IntegrityStop('Infrastructure/provider failure; experiment stopped')
        manifest['status']='complete'
    except BaseException as exc:
        manifest['status']='incomplete'
        manifest['stop_reason']=str(exc) if isinstance(exc,IntegrityStop) else type(exc).__name__
        raise
    finally:
        manifest['updated_utc']=datetime.now(timezone.utc).isoformat()
        manifest['ledger_totals']=ledger.totals()
        atomic_json(folder/'manifest.json',manifest)
        export(ledger,experiment,folder)


def runner_hashes():
    return {p.name:digest(p) for p in (ROOT/'benchmark_v3').glob('*.py')}


def create_run(parent,available,kind='paid',stage='pilot',repetition_index=1):
    if stage not in {'pilot','main'}:
        raise IntegrityStop('Unknown experiment stage')
    _,hashes=load_backend()
    experiment=uuid.uuid4().hex
    folder=Path(parent)/experiment
    folder.mkdir(parents=True,exist_ok=False)
    git=lambda *args:subprocess.check_output(['git','-c',f'safe.directory={V2.parent}',*args],cwd=V2,text=True).strip()
    revision=git('rev-parse','HEAD')
    status=git('status','--short','--untracked-files=no')
    source={'v2_path':str(V2),'git_revision':revision,'tracked_worktree_status':status,
            'v2_sha256':hashes,'runner_sha256':runner_hashes(),
            'preparation_manifest_sha256':digest(ROOT/'benchmark_v3/preparation-manifest.json')}
    atomic_json(folder/'source-manifest.json',source)
    manifest={'experiment_id':experiment,'protocol_version':f'v3-{stage}-1','kind':kind,'stage':stage,'status':'created',
              'started_utc':datetime.now(timezone.utc).isoformat(),'endpoint':ENDPOINT,
              'requested_models':MODELS,'available_models':available,'architectures':ARCHITECTURES,
              'tasks':PILOT_TASKS if stage=='pilot' else [t.task_id for t in get_tasks()],
              'repeats':1,'repetition_index':repetition_index,'max_iterations':3,'max_tokens':MAX_OUTPUT,
              'execution_approval':'User approved one complete balanced main repetition in chat' if stage=='main' else 'User approved calibration pilot',
              'max_tokens_approval':'Explicit user approval in chat: 4096 tokens per answer for pilot and v3',
              'generation_parameters':'provider defaults except approved max_tokens=4096; n=1, stream=false',
              'input_reservation_per_request':INPUT_ENVELOPE,'max_serialized_prompt_bytes':MAX_PROMPT_BYTES,
              'reservation_assumptions':'Text-only byte/subword tokenizer; prompt framing fits conservative envelope; provider honors max_tokens. No unconditional guarantee against provider accounting/limit violations.',
              'budget_ceiling':1000000,'budget_target':850000,'source_sha256':hashes,
              'runner_sha256':runner_hashes(),'python':platform.python_version(),
              'sdk_version':__import__('importlib.metadata',fromlist=['version']).version('gigachat'),
              'limitation':'Known adversarial sandbox RPC integrity limitation; not secure against malicious candidates.'}
    atomic_json(folder/'manifest.json',manifest)
    snapshot=folder/'runner-source-snapshot'
    snapshot.mkdir()
    for p in (ROOT/'benchmark_v3').glob('*.py'):
        shutil.copyfile(p,snapshot/p.name)
    return folder


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--preflight',action='store_true')
    parser.add_argument('--pilot',action='store_true')
    parser.add_argument('--main',action='store_true',help='Approved 120-evaluation main run; exactly one repeat')
    parser.add_argument('--restart-main',action='store_true',help='One explicitly authorized fresh main run; retain all prior costs and holds')
    parser.add_argument('--second-main',action='store_true',help='Exactly one additional balanced main repetition')
    parser.add_argument('--approved-target',type=int)
    parser.add_argument('--resume',type=Path)
    parser.add_argument('--approved-max-tokens',type=int)
    args=parser.parse_args()
    if sum(bool(v) for v in (args.pilot,args.main,args.restart_main,args.second_main,args.resume))>1:
        parser.error('--pilot, --main and --resume are mutually exclusive')
    if not args.preflight and not args.pilot and not args.main and not args.restart_main and not args.second_main and not args.resume:
        parser.error('Select --preflight, --pilot, --main or --resume')
    load_backend()
    from sandbox_runner import run_code_in_sandbox,IMAGE
    check=run_code_in_sandbox('def f(): return 42','assert f()==42',timeout=20)
    if check.status!='passed':
        raise IntegrityStop('Docker preflight: '+check.status)
    from dotenv import load_dotenv
    load_dotenv(ROOT/'multiagent_llm_experiment/.env')
    key=os.getenv('GIGACHAT_AUTH_KEY')
    if not key:
        raise IntegrityStop('GigaChat credentials absent')
    send=SDKTransport(key,os.getenv('GIGACHAT_VERIFY_SSL','true').lower() in {'true','1','yes'},int(os.getenv('GIGACHAT_TIMEOUT','60')))
    try:
        available=send.models()
        if not set(MODELS)<=set(available):
            raise IntegrityStop('Required models unavailable on intended endpoint')
        print('Preflight passed; endpoint:',ENDPOINT,'models:',MODELS,'image:',IMAGE,flush=True)
        if args.preflight and not (args.pilot or args.main or args.restart_main or args.second_main or args.resume):
            return
        if args.approved_max_tokens!=MAX_OUTPUT:
            raise IntegrityStop('Explicit approved max_tokens=4096 required')
        ledger_path=ROOT/'research_v3/shared-budget.sqlite3'
        current_target=850000
        if ledger_path.exists():
            with sqlite3.connect(ledger_path) as settings_db:
                current_target=settings_db.execute('SELECT target FROM settings WHERE id=1').fetchone()[0]
        ledger=Ledger(ledger_path,target=current_target)
        stage='main' if args.main or args.restart_main or args.second_main else 'pilot'
        second_metadata=None
        if args.second_main:
            if args.approved_target!=853000:
                raise IntegrityStop('Explicit approved target 853000 required for second repetition')
            if ledger.db.execute("SELECT 1 FROM runs WHERE stage='main-repetition-2'").fetchone():
                raise IntegrityStop('Second repetition already registered; no duplicate or third repetition')
            first=ledger.db.execute("SELECT * FROM runs WHERE stage='main-restart-1'").fetchone()
            if not first:
                raise IntegrityStop('Complete first balanced repetition required')
            first_manifest=json.loads((Path(first['folder'])/'manifest.json').read_text(encoding='utf-8'))
            if first_manifest['status']!='complete' or len(ledger.results(first['experiment']))!=120:
                raise IntegrityStop('First repetition is not complete and balanced')
            if ledger.target==850000:
                ledger.approve_target(853000,'User explicitly approved target 853000 and second 120-evaluation main repetition on 2026-11-12; hard ceiling remains 1000000.')
            if ledger.target!=853000:
                raise IntegrityStop('Unexpected approved target')
            observed=ledger.db.execute("SELECT SUM(total_tokens+COALESCE(json_extract(response,'$.usage.precached_prompt_tokens'),0)) FROM requests WHERE experiment=? AND state='complete'",(first['experiment'],)).fetchone()[0]
            budget=ledger.totals()
            forecast=budget['actual']+budget['reserved']+math.ceil(observed*1.5)+INPUT_ENVELOPE+MAX_OUTPUT
            if budget['unresolved'] or forecast>min(ledger.target,ledger.ceiling):
                raise IntegrityStop('Second repetition no longer fits conservative approved budget')
            second_metadata={'first_complete_run':first['experiment'],'observed_first_tokens_including_cache':observed,
                             'forecast_with_margin_and_reservations':forecast,'planning_margin':1.5,
                             'approval':'User: Да, одобряю цель 853 000 и второй прогон',
                             'first_results_not_reused':True}
        restart_metadata=None
        if args.restart_main:
            if ledger.db.execute("SELECT 1 FROM runs WHERE stage='main-restart-1'").fetchone():
                raise IntegrityStop('Authorized restart already registered; no second restart')
            old=ledger.db.execute("SELECT * FROM runs WHERE stage='main-one-repeat'").fetchone()
            if not old:
                raise IntegrityStop('Original main run not found')
            old_manifest=json.loads((Path(old['folder'])/'manifest.json').read_text(encoding='utf-8'))
            if old_manifest['status']!='incomplete':
                raise IntegrityStop('Only an incomplete main can be restarted')
            unknown=list(ledger.db.execute("SELECT * FROM requests WHERE state!='complete'"))
            if len(unknown)!=1 or unknown[0]['experiment']!=old['experiment']:
                raise IntegrityStop('Unexpected unresolved requests; restart cannot bypass them')
            authorization='User requested a fresh complete main run on 2026-11-12; preserve abandoned attempt and its full unknown-request reserve.'
            if not ledger.db.execute('SELECT 1 FROM authorized_holds WHERE request_key=?',(unknown[0]['key'],)).fetchone():
                ledger.hold_unknown_for_restart(unknown[0]['key'],authorization)
            restart_metadata={'replaces_for_analysis':old['experiment'],'authorization':authorization,
                              'unknown_request':unknown[0]['key'],'retained_reserve':unknown[0]['input_reserve']+unknown[0]['output_reserve'],
                              'previous_results_not_reused':True}
        if args.resume:
            folder=args.resume.resolve()
        else:
            if stage=='main':
                pilot=ledger.db.execute("SELECT * FROM runs WHERE stage='calibration-pilot'").fetchone()
                if not pilot or len(ledger.results(pilot['experiment']))!=18:
                    raise IntegrityStop('Complete calibration pilot required before main')
                budget=ledger.totals()
                if not args.second_main and (budget['unresolved'] or budget['actual']+budget['reserved']+464328+69632>ledger.target):
                    raise IntegrityStop('Approved main planning margin does not fit remaining target')
            folder=create_run(ROOT/f'research_v3/{stage}-runs',available,stage=stage,repetition_index=2 if args.second_main else 1)
        saved=json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
        saved['budget_target']=ledger.target
        if second_metadata:
            saved['second_repetition']=second_metadata
            saved['budget_before_run']=ledger.totals()
            saved['execution_approval']='Explicit user approval: second independent balanced 120-evaluation repetition, target 853000.'
            atomic_json(folder/'manifest.json',saved)
        if restart_metadata:
            saved['restart']=restart_metadata
            saved['budget_before_run']=ledger.totals()
            atomic_json(folder/'manifest.json',saved)
        if saved['kind']!='paid':
            raise IntegrityStop('Cannot execute an offline fixture run against provider')
        registration='main-repetition-2' if saved.get('second_repetition') else ('main-restart-1' if saved.get('restart') else ('main-one-repeat' if saved.get('stage')=='main' else 'calibration-pilot'))
        if not args.resume:
            ledger.register_run(registration,saved['experiment_id'],folder)
        else:
            registered=ledger.db.execute('SELECT * FROM runs WHERE stage=?',(registration,)).fetchone()
            if not registered or registered['experiment']!=saved['experiment_id']:
                raise IntegrityStop('Resume identity does not match registered pilot')
        print('Experiment folder:',folder,flush=True)
        try:
            execute(folder,ledger,send)
        finally:
            ledger.close()
    finally:
        send.close()


if __name__=='__main__':
    try:
        main()
    except IntegrityStop as exc:
        print('STOP:',exc,flush=True)
        raise SystemExit(2)
