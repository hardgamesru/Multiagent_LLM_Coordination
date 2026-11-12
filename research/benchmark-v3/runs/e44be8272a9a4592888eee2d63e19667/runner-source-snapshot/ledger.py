"""Durable serial request reservations. Unresolved usage blocks all further calls."""
import json
from pathlib import Path
import sqlite3
import time


class IntegrityStop(BaseException):
    """Bypass coordinators' ordinary provider-error recovery paths."""


class Ledger:
    def __init__(self,path,ceiling=1000000,target=850000):
        self.path=Path(path)
        self.path.parent.mkdir(parents=True,exist_ok=True)
        self.db=sqlite3.connect(self.path,timeout=30,isolation_level=None)
        self.db.row_factory=sqlite3.Row
        self.db.execute('PRAGMA journal_mode=WAL')
        self.db.execute('PRAGMA synchronous=FULL')
        self.db.executescript('''
          CREATE TABLE IF NOT EXISTS settings (id INTEGER PRIMARY KEY, ceiling INTEGER, target INTEGER);
          CREATE TABLE IF NOT EXISTS requests (
            key TEXT PRIMARY KEY, experiment TEXT, evaluation TEXT, model TEXT, endpoint TEXT,
            prompt_hash TEXT, input_reserve INTEGER, output_reserve INTEGER,
            state TEXT, created REAL, response TEXT, input_tokens INTEGER, output_tokens INTEGER,
            total_tokens INTEGER, returned_model TEXT, finish_reason TEXT, latency REAL, error TEXT);
          CREATE TABLE IF NOT EXISTS evaluations (
            key TEXT PRIMARY KEY, experiment TEXT, state TEXT, result TEXT);
          CREATE TABLE IF NOT EXISTS runs (stage TEXT PRIMARY KEY, experiment TEXT UNIQUE, folder TEXT);
          CREATE TABLE IF NOT EXISTS authorized_holds (
            request_key TEXT PRIMARY KEY REFERENCES requests(key), authorization TEXT NOT NULL, created REAL NOT NULL);
        ''')
        self.db.execute('INSERT OR IGNORE INTO settings VALUES(1,?,?)',(ceiling,target))
        settings=self.db.execute('SELECT * FROM settings').fetchone()
        if (settings['ceiling'],settings['target'])!=(ceiling,target):
            self.db.close()
            raise IntegrityStop('Ledger budget configuration mismatch')
        self.ceiling,self.target=ceiling,target

    def totals(self):
        return dict(self.db.execute('''SELECT COALESCE(SUM(total_tokens),0) AS billed_actual,
          COALESCE(SUM(json_extract(response,'$.usage.precached_prompt_tokens')),0) AS cached_input,
          COALESCE(SUM(total_tokens+COALESCE(json_extract(response,'$.usage.precached_prompt_tokens'),0)),0) AS actual,
          COALESCE(SUM(CASE WHEN state!='complete' THEN input_reserve+output_reserve ELSE 0 END),0) AS reserved,
          COALESCE(SUM(CASE WHEN state!='complete' AND key NOT IN
            (SELECT request_key FROM authorized_holds) THEN 1 ELSE 0 END),0) AS unresolved FROM requests''').fetchone())

    def hold_unknown_for_restart(self,key,authorization):
        """Retain unknown usage AND its full reservation; allow only new requests."""
        row=self.db.execute('SELECT * FROM requests WHERE key=?',(key,)).fetchone()
        if not row or row['state']!='unknown' or row['response'] is not None or row['total_tokens'] is not None:
            raise IntegrityStop('Only an unreturned unknown request can receive an explicit full-reserve hold')
        if not authorization:
            raise IntegrityStop('Restart authorization required')
        self.db.execute('INSERT INTO authorized_holds VALUES(?,?,?)',(key,authorization,time.time()))

    def reserve(self,key,experiment,evaluation,model,endpoint,prompt_hash,input_reserve,output_reserve):
        if min(input_reserve,output_reserve)<=0:
            raise IntegrityStop('Invalid reservation')
        self.db.execute('BEGIN IMMEDIATE')
        try:
            previous=self.db.execute('SELECT * FROM requests WHERE key=?',(key,)).fetchone()
            if previous:
                if (previous['prompt_hash'],previous['model'],previous['endpoint'],previous['output_reserve'])!=(prompt_hash,model,endpoint,output_reserve):
                    raise IntegrityStop('Replay identity mismatch')
                if previous['state']!='complete':
                    raise IntegrityStop('Ambiguous request already exists; never resend automatically')
                self.db.execute('COMMIT')
                return json.loads(previous['response'])
            totals=self.totals()
            if totals['unresolved'] or totals['actual']+totals['reserved']+input_reserve+output_reserve>min(self.ceiling,self.target):
                raise IntegrityStop('Unresolved usage or insufficient pre-request budget')
            self.db.execute('''INSERT INTO requests(key,experiment,evaluation,model,endpoint,prompt_hash,
              input_reserve,output_reserve,state,created) VALUES(?,?,?,?,?,?,?,?,?,?)''',
              (key,experiment,evaluation,model,endpoint,prompt_hash,input_reserve,output_reserve,'pending',time.time()))
            self.db.execute('COMMIT')
            return None
        except BaseException:
            if self.db.in_transaction:
                self.db.execute('ROLLBACK')
            raise

    def settle(self,key,response,latency):
        usage=response.get('usage') or {}
        counts=[usage.get(k) for k in ('prompt_tokens','completion_tokens','total_tokens')]
        cached=usage.get('precached_prompt_tokens') or 0
        valid=all(type(n) is int and n>=0 for n in counts) and counts[0]+counts[1]==counts[2] and type(cached) is int and cached>=0
        self.db.execute('BEGIN IMMEDIATE')
        try:
            row=self.db.execute('SELECT * FROM requests WHERE key=?',(key,)).fetchone()
            if not row or row['state']!='pending':
                raise IntegrityStop('Unexpected/duplicate response settlement')
            bounds=valid and counts[0]+cached<=row['input_reserve'] and counts[1]<=row['output_reserve']
            choices=response.get('choices') or []
            finish=choices[0].get('finish_reason') if choices else None
            self.db.execute('''UPDATE requests SET state=?,response=?,input_tokens=?,output_tokens=?,
              total_tokens=?,returned_model=?,finish_reason=?,latency=?,error=? WHERE key=?''',
              ('complete' if bounds else 'unknown',json.dumps(response,ensure_ascii=False),
               *[n if type(n) is int and n>=0 else None for n in counts],response.get('model'),finish,latency,
               None if bounds else 'missing/inconsistent usage or reservation exceeded',key))
            self.db.execute('COMMIT')
        except BaseException:
            if self.db.in_transaction:
                self.db.execute('ROLLBACK')
            raise
        if not bounds:
            raise IntegrityStop('Provider accounting invalid; response preserved, further requests blocked')

    def unknown(self,key,diagnostic=None,latency=None):
        # No exception string, response body, URL, credential or arbitrary header.
        safe={'billing':'unknown'}
        if diagnostic:
            for name in ('exception_type','http_status','retry_after_seconds','provider_request_id'):
                if name in diagnostic:
                    safe[name]=diagnostic[name]
        self.db.execute("UPDATE requests SET state='unknown',error=?,latency=? WHERE key=? AND state='pending'",
                        (json.dumps(safe),latency,key))

    def claim_evaluation(self,key,experiment):
        self.db.execute("INSERT OR IGNORE INTO evaluations VALUES(?,?,'in_progress',NULL)",(key,experiment))
        row=self.db.execute('SELECT * FROM evaluations WHERE key=?',(key,)).fetchone()
        if row['state']=='complete':
            return json.loads(row['result'])
        return None

    def register_run(self,stage,experiment,folder):
        try:
            self.db.execute('INSERT INTO runs VALUES(?,?,?)',(stage,experiment,str(folder)))
        except sqlite3.IntegrityError:
            raise IntegrityStop('Stage already registered; use explicit --resume, never launch a duplicate pilot') from None

    def save_evaluation(self,key,result):
        self.db.execute("UPDATE evaluations SET state='complete',result=? WHERE key=? AND state='in_progress'",(json.dumps(result,ensure_ascii=False),key))

    def results(self,experiment):
        return [json.loads(r[0]) for r in self.db.execute("SELECT result FROM evaluations WHERE experiment=? AND state='complete' ORDER BY rowid",(experiment,))]

    def close(self):
        self.db.close()
