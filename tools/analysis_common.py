"""Support code copied to tools/analysis_common.py by the local packager."""
from pathlib import Path
import ast
import csv
import io
import json
import math
import sqlite3
import statistics
from collections import Counter

ROOT=Path(__file__).resolve().parents[1]
ARCHS=['single_agent','feedback_graph','parallel_consensus']
MODELS=['GigaChat-2','GigaChat-3-Ultra']
DIFFICULTIES=['easy','medium','hard']


def equivalent(a,b):
    if a==b:return True
    try:return math.isclose(float(a),float(b),rel_tol=1e-11,abs_tol=1e-8)
    except (ValueError,TypeError):
        try:return ast.literal_eval(a)==ast.literal_eval(b)
        except (ValueError,SyntaxError):return False


def save_table(path,rows):
    output=io.StringIO(newline='')
    writer=csv.DictWriter(output,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    if path.exists():
        with path.open(encoding='utf-8',newline='') as f:old=list(csv.DictReader(f))
        new=list(csv.DictReader(io.StringIO(output.getvalue())))
        assert len(old)==len(new),path
        for a,b in zip(old,new):
            assert set(a)==set(b),path
            assert all(equivalent(a[k],b[k]) for k in a),(path,a,b)
        return  # Keep original measured/derived CSV bytes unchanged.
    path.write_bytes(output.getvalue().encode('utf-8'))


def aggregate(rows):
    passed=sum(r['status']=='passed' for r in rows);total=sum(r['budget_tokens'] for r in rows)
    return {'evaluations':len(rows),'passed':passed,'success_rate':passed/len(rows),
            'input_usage_tokens':sum(int(r['input_tokens']) for r in rows),
            'cached_input_tokens':sum(r['cached_tokens'] for r in rows),
            'output_tokens':sum(int(r['output_tokens']) for r in rows),
            'provider_total_tokens':sum(int(r['total_tokens']) for r in rows),
            'combined_tokens_including_cache':total,'llm_calls':sum(int(r['llm_calls']) for r in rows),
            'elapsed_seconds':sum(float(r['elapsed_seconds']) for r in rows),
            'mean_seconds':statistics.mean(float(r['elapsed_seconds']) for r in rows),
            'mean_api_seconds':statistics.mean(r['api_seconds'] for r in rows),
            'tokens_per_pass':total/passed if passed else None,
            'failures':dict(Counter(r['status'] for r in rows if r['status']!='passed'))}


def md_table(headers,rows):
    return ['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(map(str,row))+' |' for row in rows]


def load_audit():
    """Read exported measured metadata into memory; no raw responses or disk DB."""
    db=sqlite3.connect(':memory:');db.row_factory=sqlite3.Row
    path=ROOT/'research/benchmark-v3/audit/requests.csv'
    with path.open(encoding='utf-8',newline='') as f:
        reader=csv.DictReader(f);columns=reader.fieldnames
        integer={'input_reserve','output_reserve','input_tokens','output_tokens','total_tokens','cached_input_tokens'}
        real={'created','latency'}
        definitions=[name+(' INTEGER' if name in integer else ' REAL' if name in real else ' TEXT') for name in columns]
        db.execute('CREATE TABLE requests ('+','.join(definitions)+')')
        for row in reader:
            values=[None if row[k]=='' else int(row[k]) if k in integer else float(row[k]) if k in real else row[k] for k in columns]
            db.execute('INSERT INTO requests VALUES('+','.join('?' for _ in columns)+')',values)
    budget=json.loads((ROOT/'research/benchmark-v3/audit/budget.json').read_text())['settings']
    db.execute('CREATE TABLE settings (target INTEGER,ceiling INTEGER)')
    db.execute('INSERT INTO settings VALUES(?,?)',(budget['target'],budget['ceiling']))
    return db
