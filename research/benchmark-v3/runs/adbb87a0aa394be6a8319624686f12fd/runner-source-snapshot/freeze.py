"""Produce an offline task inventory and immutable initial source manifest."""
import dataclasses
import hashlib
import json
from pathlib import Path
from .catalog import get_tasks


def main():
    root=Path(__file__).resolve().parent
    destination=root/'preparation-manifest.json'
    if destination.exists():
        raise SystemExit('Preparation manifest exists; explicitly version changes instead of overwriting.')
    tasks=get_tasks()
    inventory=[]
    docs=['# Benchmark v3 task specifications','',
          'Predefined before any model run. Expected evaluation values are stored privately in catalog.py.', '']
    for task in tasks:
        item=dataclasses.asdict(task)
        inventory.append(item)
        docs += [f'## {task.task_id}: {task.name} ({task.difficulty})','',
                 f'Domain: {task.domain}. Rationale: {task.rationale}', '', task.description,'',
                 'Visible examples:', '', *['- `'+example+'`' for example in task.visible_examples], '',
                 f'Development cases: {len(task.development)}. Held-out cases: {len(task.evaluation)}.', '']
    (root/'task-inventory.json').write_text(json.dumps(inventory,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    (root/'task-specifications.md').write_text('\n'.join(docs),encoding='utf-8')
    sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.iterdir())
             if p.suffix in {'.py','.md','.json'} and p.name!=destination.name}
    manifest={'protocol_version':'v3-preparation-1','status':'validated; no paid experiments',
              'suite_size':20,'difficulty_counts':{'easy':4,'medium':8,'hard':8},
              'development_cases':sum(len(t.development) for t in tasks),
              'evaluation_cases':sum(len(t.evaluation) for t in tasks),
              'pilot_task_ids':['v3_03','v3_10','v3_17'],
              'models':['GigaChat-2','GigaChat-3-Ultra'],
              'architectures':['single_agent','feedback_graph','parallel_consensus'],
              'planned_repeats':3,'planned_evaluations':360,'pilot_evaluations':18,
              'total_new_experiment_token_ceiling':1000000,'target_tokens':850000,
              'api_calls_preparation':0,
              'v2_base_commit':'5e469e9cfcb185ae9650136dc5c539a9dad50256',
              'v2_source_snapshot':'../lite-benchmark-work',
              'known_limitation':'Adversarial candidate RPC integrity not guaranteed.',
              'sha256':sources}
    destination.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print('Frozen initial preparation inventory and source hashes.')


if __name__=='__main__':
    main()
