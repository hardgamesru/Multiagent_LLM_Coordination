"""Pilot-only runner. No main-experiment execution option is provided yet."""
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
    manifest['shared_ledger_path']=str(ledger.path.resolve())
    tasks={t.task_id:t for t in get_tasks()}
    export(ledger,experiment,folder)  # Recover CSV if interrupted after SQLite commit.
    try:
        if backend:
            # Only offline tests inject a fake sandbox. Paid runs use unchanged backend.
            coordinators.run_code_in_sandbox=backend
        for model in MODELS:
            for architecture in ARCHITECTURES:
                for task_id in PILOT_TASKS:
                    task=tasks[task_id]
                    key=f'{experiment}:{model}:{architecture}:{task_id}:1'
                    if ledger.claim_evaluation(key,experiment) is not None:
                        continue
                    client=MeteredClient(model,ledger,experiment,key,send)
                    coordinator=coordinators.COORDINATORS[architecture](client,folder/'generated_solutions',max_iterations=3)
                    print(f'{model} {architecture} {task_id}',flush=True)
                    result=asdict(coordinator.run(task,hashlib.sha256(key.encode()).hexdigest()[:16]))
                    requests=list(ledger.db.execute('SELECT finish_reason,latency FROM requests WHERE evaluation=? ORDER BY created',(key,)))
                    result.update(experiment_id=experiment,repeat_index=1,protocol_version='v3-pilot-1',
                                  requested_model=model,returned_models=client.returned_models,endpoint=ENDPOINT,
                                  finish_reasons=[r['finish_reason'] for r in requests],
                                  request_latency_seconds=[r['latency'] for r in requests],
                                  difficulty=task.difficulty,task_sha256=digest(ROOT/'benchmark_v3/catalog.py'),
                                  source_manifest_sha256=digest(folder/'source-manifest.json'))
                    ledger.save_evaluation(key,result)
                    export(ledger,experiment,folder)
                    if result['status'] in {'sandbox_timeout','sandbox_error','sandbox_unavailable','provider_error'}:
                        raise IntegrityStop('Infrastructure/provider failure; pilot stopped')
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


def create_run(parent,available,kind='paid'):
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
    manifest={'experiment_id':experiment,'protocol_version':'v3-pilot-1','kind':kind,'status':'created',
              'started_utc':datetime.now(timezone.utc).isoformat(),'endpoint':ENDPOINT,
              'requested_models':MODELS,'available_models':available,'architectures':ARCHITECTURES,
              'tasks':PILOT_TASKS,'repeats':1,'max_iterations':3,'max_tokens':MAX_OUTPUT,
              'max_tokens_approval':'Explicit user approval in chat: 4096 tokens per answer for pilot and v3',
              'generation_parameters':'provider defaults except approved max_tokens=4096; n=1, stream=false',
              'input_reservation_per_request':INPUT_ENVELOPE,'max_serialized_prompt_bytes':MAX_PROMPT_BYTES,
              'reservation_assumptions':'Text-only byte/subword tokenizer; prompt framing fits conservative envelope; provider honors max_tokens. No unconditional guarantee against provider accounting/limit violations.',
              'budget_ceiling':1000000,'budget_target':850000,'source_sha256':hashes,
              'runner_sha256':runner_hashes(),'python':platform.python_version(),
              'sdk_version':__import__('importlib.metadata',fromlist=['version']).version('gigachat'),
              'limitation':'Known adversarial sandbox RPC integrity limitation; not secure against malicious candidates.'}
    atomic_json(folder/'manifest.json',manifest)
    return folder


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--preflight',action='store_true')
    parser.add_argument('--pilot',action='store_true')
    parser.add_argument('--resume',type=Path)
    parser.add_argument('--approved-max-tokens',type=int)
    args=parser.parse_args()
    if not args.preflight and not args.pilot and not args.resume:
        parser.error('Select --preflight, --pilot or --resume')
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
        if args.preflight and not (args.pilot or args.resume):
            return
        if args.approved_max_tokens!=MAX_OUTPUT:
            raise IntegrityStop('Explicit approved max_tokens=4096 required')
        ledger=Ledger(ROOT/'research_v3/shared-budget.sqlite3')
        folder=args.resume.resolve() if args.resume else create_run(ROOT/'research_v3/pilot-runs',available)
        saved=json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
        if saved['kind']!='paid':
            raise IntegrityStop('Cannot execute an offline fixture run against provider')
        if not args.resume:
            ledger.register_run('calibration-pilot',saved['experiment_id'],folder)
        else:
            registered=ledger.db.execute('SELECT * FROM runs WHERE stage=?',('calibration-pilot',)).fetchone()
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
