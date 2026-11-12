"""Validate immutable publication data and research tables without any API calls."""
from pathlib import Path
import csv
import hashlib
import json
import math

ROOT=Path(__file__).resolve().parents[1]
R1='e44be8272a9a4592888eee2d63e19667'
R2='adbb87a0aa394be6a8319624686f12fd'


def verify(core_only=False):
    frozen=json.loads((ROOT/'provenance/publication-freeze.json').read_text())
    for name,h in frozen['frozen_v3'].items():
        assert hashlib.sha256((ROOT/'benchmark_v3'/name).read_bytes()).hexdigest()==h,name
    for name,h in frozen['frozen_v2'].items():
        assert hashlib.sha256((ROOT/'multiagent_llm_experiment'/name).read_bytes()).hexdigest()==h,name
    all_rows=[]
    for run,rep in [(R1,1),(R2,2)]:
        path=ROOT/'research/benchmark-v3/runs'/run
        with (path/'raw_results.csv').open(encoding='utf-8',newline='') as f:rows=list(csv.DictReader(f))
        assert len(rows)==120
        assert {int(r['repeat_index']) for r in rows}=={rep}
        assert len({(r['model'],r['architecture'],r['task_id']) for r in rows})==120
        assert all(r['usage_available']=='True' for r in rows)
        assert all(int(r['input_tokens'])+int(r['output_tokens'])==int(r['total_tokens']) for r in rows)
        for r in rows:
            if r['final_code_path']:assert (path/r['final_code_path'].replace('\\','/')).is_file()
        all_rows.extend(rows)
        manifest=json.loads((path/'manifest.json').read_text())
        assert manifest['status']=='complete' and manifest['max_tokens']==4096
        assert manifest['source_sha256']==frozen['frozen_v2']
    assert len(all_rows)==240
    audit=ROOT/'research/benchmark-v3/audit/requests.csv'
    with audit.open(encoding='utf-8',newline='') as f:requests=list(csv.DictReader(f))
    for r in all_rows:
        key=f"{r['experiment_id']}:{r['model']}:{r['architecture']}:{r['task_id']}:{r['repeat_index']}"
        group=[q for q in requests if q['evaluation']==key]
        assert len(group)==int(r['llm_calls'])
        assert all(q['state']=='complete' for q in group)
        assert sum(int(q['input_tokens']) for q in group)==int(r['input_tokens'])
        assert sum(int(q['output_tokens']) for q in group)==int(r['output_tokens'])
        assert sum(int(q['total_tokens']) for q in group)==int(r['total_tokens'])
    main=[q for q in requests if q['experiment'] in {R1,R2}]
    assert len(main)==965
    assert sum(int(q['total_tokens'])+int(q['cached_input_tokens']) for q in main)==548141
    unknown=[q for q in requests if q['state']!='complete']
    assert len(unknown)==1 and unknown[0]['total_tokens']==''
    assert int(unknown[0]['input_reserve'])+int(unknown[0]['output_reserve'])==69632
    tables=ROOT/'research/benchmark-v3/runs'/R2/'analysis'
    with (tables/'model-architecture-by-repetition.csv').open(encoding='utf-8',newline='') as f:summary=list(csv.DictReader(f))
    for s in summary:
        selected=[r for r in all_rows if r['model']==s['model'] and r['architecture']==s['architecture'] and r['repeat_index']==s['repetition']]
        assert len(selected)==int(s['evaluations'])==20
        assert sum(r['status']=='passed' for r in selected)==int(s['passed'])
        assert math.isclose(float(s['success_rate']),int(s['passed'])/20)
        assert sum(int(r['total_tokens']) for r in selected)==int(s['provider_total_tokens'])
    inherited=json.loads((ROOT/'provenance/inherited-baseline-files.json').read_text())
    for item in inherited['files']:
        assert hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest()==item['sha256'],item['path']
    if not core_only:
        lineage=json.loads((ROOT/'provenance/artifact-lineage.json').read_text())
        for record in lineage['records']:
            path=ROOT/record['public_path']
            assert path.is_file(),record['public_path']
            assert hashlib.sha256(path.read_bytes()).hexdigest()==record['public_sha256'],record['public_path']
            if path.suffix=='.csv':assert record['public_sha256']==record['original_sha256'],record['public_path']
    return {'main_records':240,'main_calls':965,'combined_main_tokens':548141,'unknown_reserved_tokens':69632,'status':'passed'}


if __name__=='__main__':print(json.dumps(verify(),indent=2))
