"""Publication privacy/secret scan. Never prints matched values."""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

ROOT=Path(__file__).resolve().parents[1]


def scan(credentials_env_file=None):
    secrets=[]
    if credentials_env_file:
        for line in Path(credentials_env_file).read_text(encoding='utf-8').splitlines():
            if '=' not in line or line.lstrip().startswith('#'):continue
            name,value=line.split('=',1);value=value.strip().strip('"\'')
            if re.search('AUTH_KEY|TOKEN|SECRET|PASSWORD',name,re.I) and len(value)>=16:
                secrets.append(value)
                try:
                    decoded=base64.b64decode(value,validate=True).decode('utf-8')
                    secrets.extend(part for part in decoded.split(':') if len(part)>=16)
                except (ValueError,UnicodeError):pass
    secrets.extend(v for k,v in os.environ.items() if re.search('GIGACHAT.*(?:KEY|TOKEN|SECRET)',k,re.I) and len(v)>=16)
    failures=[];inherited=[];count=0;largest=0
    personal=re.compile(r'(?<![A-Za-z])[A-Za-z]:[\\/]'+r'|/'+r'Users/',re.I)
    generic=[re.compile(r'gh[pousr]_[A-Za-z0-9]{20,}'),re.compile(r'\bAKIA[0-9A-Z]{16}\b'),re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')]
    for p in ROOT.rglob('*'):
        if not p.is_file() or p.name=='.git' or any(part in {'__pycache__','.git','.venv','.ruff_cache','.pytest_cache'} for part in p.relative_to(ROOT).parts):continue
        rel=p.relative_to(ROOT).as_posix();data=p.read_bytes();count+=1;largest=max(largest,len(data))
        if p.suffix in {'.sqlite3','.db','.zip','.7z','.pyc'} or p.name=='.env' or (p.name.startswith('.env.') and p.name!='.env.example'):
            failures.append({'file':rel,'reason':'forbidden private/cache/archive artifact'})
        if len(data)>5*1024*1024:failures.append({'file':rel,'reason':'oversized artifact'})
        try:text=data.decode('utf-8')
        except UnicodeError:
            failures.append({'file':rel,'reason':'unexpected binary artifact'});continue
        if any(value in text for value in secrets) or any(pattern.search(text) for pattern in generic):
            failures.append({'file':rel,'reason':'credential-like value (redacted)'})
        if personal.search(text):
            if rel=='multiagent_llm_experiment/results/raw_results.csv':
                original=subprocess.check_output(['git','show','5e469e9cfcb185ae9650136dc5c539a9dad50256:'+rel],cwd=ROOT)
                if original==data:
                    inherited.append({'file':rel,'reason':'byte-identical pre-existing legacy dataset; not public-facing documentation','sha256':hashlib.sha256(data).hexdigest()})
                else:failures.append({'file':rel,'reason':'changed legacy private path metadata'})
            else:failures.append({'file':rel,'reason':'personal path/name'})
    return {'status':'passed' if not failures else 'failed','files_scanned':count,'largest_file_bytes':largest,
            'configured_credentials_scanned':bool(secrets),'failures':failures,'documented_inherited_exceptions':inherited}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--credentials-env-file',type=Path)
    result=scan(parser.parse_args().credentials_env_file);print(json.dumps(result,indent=2))
    raise SystemExit(0 if result['status']=='passed' else 1)
