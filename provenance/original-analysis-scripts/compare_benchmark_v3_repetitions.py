"""Offline paired two-repetition analysis; never calls a provider.

Reproduce: python compare_benchmark_v3_repetitions.py RUN1 RUN2
"""
import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import shutil
import sqlite3
import statistics
from analyze_benchmark_v3 import aggregate,save_table,md_table,MODELS,ARCHS,DIFFICULTIES

ROOT=Path(__file__).resolve().parent


def read_run(folder,db,number):
    manifest=json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
    assert manifest['status']=='complete' and manifest['max_tokens']==4096
    assert manifest['endpoint']=='https://api.giga.chat/v1/' and manifest['repeats']==1
    assert manifest['requested_models']==MODELS and manifest['architectures']==ARCHS
    for name,h in manifest['runner_sha256'].items():
        assert hashlib.sha256((folder/'runner-source-snapshot'/name).read_bytes()).hexdigest()==h,name
    with (folder/'raw_results.csv').open(encoding='utf-8',newline='') as f:
        rows=list(csv.DictReader(f))
    assert len(rows)==120
    assert len({(r['model'],r['architecture'],r['task_id']) for r in rows})==120
    assert {int(r['repeat_index']) for r in rows}=={number}
    calls=list(db.execute('SELECT * FROM requests WHERE experiment=?',(folder.name,)))
    assert all(r['state']=='complete' for r in calls)
    assert len(calls)==sum(int(r['llm_calls']) for r in rows)
    for row in rows:
        request_key=f"{folder.name}:{row['model']}:{row['architecture']}:{row['task_id']}:{number}"
        group=[r for r in calls if r['evaluation']==request_key]
        assert sum(r['total_tokens'] for r in group)==int(row['total_tokens'])
        assert all(r['input_tokens']+r['output_tokens']==r['total_tokens'] for r in group)
        row['cached_tokens']=sum(json.loads(r['response'])['usage'].get('precached_prompt_tokens') or 0 for r in group)
        row['budget_tokens']=int(row['total_tokens'])+row['cached_tokens']
        row['api_seconds']=sum(r['latency'] for r in group)
        row['repetition']=number
        assert (folder/row['final_code_path']).is_file()
    return manifest,rows,calls


def compare(first,second):
    first,second=Path(first).resolve(),Path(second).resolve()
    db=sqlite3.connect(second/'ledger-snapshot.sqlite3');db.row_factory=sqlite3.Row
    m1,r1,c1=read_run(first,db,1);m2,r2,c2=read_run(second,db,2)
    assert m1['source_sha256']==m2['source_sha256']
    assert m1['tasks']==m2['tasks'] and m1['generation_parameters']==m2['generation_parameters']
    assert len({r['key'] for r in c1}&{r['key'] for r in c2})==0
    assert m2['second_repetition']['first_complete_run']==first.name
    out=second/'analysis';out.mkdir(exist_ok=True)
    all_rows=r1+r2
    save_table(out/'evaluations-two-repetitions.csv',all_rows)
    per_run=[];difficulty=[];pooled=[];overall=[]
    for rep,rows in [(1,r1),(2,r2)]:
        for model in MODELS:
            overall.append({'repetition':rep,'model':model,**aggregate([r for r in rows if r['model']==model])})
            for arch in ARCHS:
                selected=[r for r in rows if r['model']==model and r['architecture']==arch]
                per_run.append({'repetition':rep,'model':model,'architecture':arch,**aggregate(selected)})
                for level in DIFFICULTIES:
                    difficulty.append({'repetition':rep,'model':model,'architecture':arch,'difficulty':level,
                                       **aggregate([r for r in selected if r['difficulty']==level])})
    for model in MODELS:
        baseline=aggregate([r for r in all_rows if r['model']==model and r['architecture']=='single_agent'])
        for arch in ARCHS:
            g=aggregate([r for r in all_rows if r['model']==model and r['architecture']==arch])
            rates=[p['success_rate'] for p in per_run if p['model']==model and p['architecture']==arch]
            pooled.append({'model':model,'architecture':arch,**g,'unique_tasks':20,
                           'repeat_rate_min':min(rates),'repeat_rate_max':max(rates),
                           'repeat_rate_sample_sd':statistics.stdev(rates),
                           'tokens_per_pass_relative_to_single':g['tokens_per_pass']/baseline['tokens_per_pass'] if g['tokens_per_pass'] and baseline['tokens_per_pass'] else None})
    save_table(out/'model-architecture-by-repetition.csv',per_run)
    save_table(out/'difficulty-by-repetition.csv',difficulty)
    save_table(out/'pooled-descriptive-results.csv',pooled)
    save_table(out/'overall-by-repetition.csv',overall)
    a={(r['model'],r['architecture'],r['task_id']):r for r in r1}
    b={(r['model'],r['architecture'],r['task_id']):r for r in r2}
    assert set(a)==set(b)
    stability=[]
    for key in sorted(a):
        x,y=a[key],b[key]
        px,py=x['status']=='passed',y['status']=='passed'
        category='stable_success' if px and py else ('stable_failure' if not px and not py else ('improved' if py else 'regressed'))
        stability.append({'model':key[0],'architecture':key[1],'task_id':key[2],'task_name':x['task_name'],
                          'difficulty':x['difficulty'],'run1_status':x['status'],'run2_status':y['status'],'category':category})
    save_table(out/'task-stability.csv',stability)
    paired=[]
    for rep,rows in [(1,r1),(2,r2)]:
        lookup={(r['model'],r['architecture'],r['task_id']):r for r in rows}
        for model in MODELS:
            for arch in ARCHS[1:]:
                for task in m1['tasks']:
                    base=lookup[model,'single_agent',task];co=lookup[model,arch,task]
                    bp,cp=base['status']=='passed',co['status']=='passed'
                    paired.append({'repetition':rep,'model':model,'architecture':arch,'task_id':task,
                                   'difficulty':base['difficulty'],'single_status':base['status'],
                                   'coordination_status':co['status'],'single_only':int(bp and not cp),
                                   'coordination_only':int(cp and not bp),'both_passed':int(bp and cp),'both_failed':int(not bp and not cp)})
    save_table(out/'paired-coordination-vs-single.csv',paired)
    # Reproducible publication artifacts. All data are measured and task-paired.
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'svg.hashsalt':'benchmark-v3-two-repetitions','font.family':'DejaVu Sans','font.size':10})
    colors=['#336699','#e68a2e','#41955d']
    fig,axes=plt.subplots(1,2,figsize=(11,4),sharey=True)
    for ax,model in zip(axes,MODELS):
        for rep,offset,color in [(1,-.17,'#336699'),(2,.17,'#e68a2e')]:
            stats=[next(p for p in per_run if p['repetition']==rep and p['model']==model and p['architecture']==arch) for arch in ARCHS]
            bars=ax.bar([i+offset for i in range(3)],[100*p['success_rate'] for p in stats],width=.32,color=color,label=f'Repetition {rep}')
            for bar,p in zip(bars,stats):
                ax.text(bar.get_x()+bar.get_width()/2,bar.get_height()+1,f"{p['passed']}/20",ha='center',fontsize=8)
        ax.set_title(model);ax.set_xticks(range(3),['Single','Feedback','Consensus']);ax.set_ylim(0,112);ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
    axes[0].set_ylabel('Held-out success (%)');axes[1].legend(frameon=False,loc='upper center',bbox_to_anchor=(.5,-.12),ncol=2)
    fig.suptitle('Two repetitions of the same 20 tasks; descriptive results');fig.tight_layout()
    for ext in ['svg','png']:fig.savefig(out/f'success-by-repetition.{ext}',metadata={'Date':None} if ext=='svg' else None,dpi=140)
    plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(11,4),sharey=True)
    for ax,model in zip(axes,MODELS):
        for index,arch in enumerate(ARCHS):
            for rep,style in [(1,'--'),(2,'-')]:
                stats=[next(d for d in difficulty if d['repetition']==rep and d['model']==model and d['architecture']==arch and d['difficulty']==level) for level in DIFFICULTIES]
                ax.plot(range(3),[100*d['success_rate'] for d in stats],linestyle=style,marker='o' if rep==1 else 's',color=colors[index],label=f'{arch}, R{rep}')
        ax.set_title(model);ax.set_xticks(range(3),['Easy (4)','Medium (8)','Hard (8)']);ax.set_ylim(-3,105);ax.grid(alpha=.2)
    axes[0].set_ylabel('Held-out success (%)');axes[1].legend(fontsize=8,frameon=False,loc='upper center',bbox_to_anchor=(.5,-.13),ncol=2)
    fig.suptitle('Predefined difficulty; dashed R1 / solid R2, no fitted trend');fig.tight_layout()
    for ext in ['svg','png']:fig.savefig(out/f'success-by-difficulty-two-repetitions.{ext}',metadata={'Date':None} if ext=='svg' else None,dpi=140)
    plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(11,4),sharey=True)
    for ax,model in zip(axes,MODELS):
        bottom=[0,0,0]
        for category,color,label in [('stable_success','#41955d','Passed both'),('stable_failure','#9b9b9b','Failed both'),('changed','#e68a2e','Changed')]:
            counts=[sum(s['model']==model and s['architecture']==arch and (s['category']==category if category!='changed' else s['category'] in {'improved','regressed'}) for s in stability) for arch in ARCHS]
            bars=ax.bar(range(3),counts,bottom=bottom,color=color,label=label)
            for bar,n,base in zip(bars,counts,bottom):
                if n:ax.text(bar.get_x()+bar.get_width()/2,base+n/2,str(n),ha='center',va='center',color='white' if category=='stable_success' else 'black')
            bottom=[x+y for x,y in zip(bottom,counts)]
        ax.set_title(model);ax.set_xticks(range(3),['Single','Feedback','Consensus']);ax.set_ylim(0,21);ax.set_yticks([0,5,10,15,20])
    axes[0].set_ylabel('Distinct tasks (20 per architecture)');axes[1].legend(frameon=False,loc='upper center',bbox_to_anchor=(.5,-.12),ncol=3)
    fig.suptitle('Task stability across two repetitions');fig.tight_layout()
    for ext in ['svg','png']:fig.savefig(out/f'task-stability.{ext}',metadata={'Date':None} if ext=='svg' else None,dpi=140)
    plt.close(fig)
    # Preserve the prior single-run report before publishing the requested update.
    report_path=ROOT/'benchmark-v3-research-report.md'
    old_report=first/'analysis/research-report-first-repetition.md'
    if not old_report.exists():shutil.copyfile(report_path,old_report)
    total=aggregate(all_rows)
    all_requests=list(db.execute('SELECT * FROM requests'))
    known=sum((r['total_tokens'] or 0)+((json.loads(r['response'])['usage'].get('precached_prompt_tokens') or 0) if r['response'] else 0) for r in all_requests)
    held=sum(r['input_reserve']+r['output_reserve'] for r in all_requests if r['state']!='complete')
    target=db.execute('SELECT target FROM settings').fetchone()[0]
    versions={rep:sorted({(c['model'],c['returned_model']) for c in calls}) for rep,calls in [(1,c1),(2,c2)]}
    audit={'run1':first.name,'run2':second.name,'main_combined':total,'known_all_v3_including_cache':known,
           'unknown_request_count':sum(r['state']!='complete' for r in all_requests),'retained_unknown_reservation':held,
           'known_plus_reserved':known+held,'approved_target':target,'hard_ceiling':1000000,
           'remaining_target_after_reservations':target-known-held,'remaining_hard_after_reservations':1000000-known-held,
           'returned_model_versions':versions,'request_finish_reasons':dict(Counter(c['finish_reason'] for c in c1+c2))}
    (out/'two-repetition-audit.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
    def success_cell(rep,model,arch):
        p=next(p for p in per_run if p['model']==model and p['architecture']==arch and p['repetition']==rep)
        return f"{p['passed']}/20 ({100*p['success_rate']:.1f}%)"
    report=['# Benchmark v3: two balanced main repetitions','',
      '## Research question and hypotheses','',
      'Does multi-agent coordination help code generation as task difficulty increases, and does stronger model capability reduce that benefit? H1 predicts increasing coordination advantage with difficulty. H2 predicts a smaller advantage for Ultra than Lite. Neither is assumed true. This is a descriptive study of 20 predefined tasks, reused across conditions and repetitions; it is not a causal experiment on a random task population.','',
      '## Dataset, environment and evidence lineage','',
      f'First complete main: `{first.name}`. Second independently executed main: `{second.name}`. Each contains 120 new evaluations: 20 tasks × 2 models × 3 architectures. No first-run observation substitutes for a second-run observation. Repetition indices are 1 and 2. There are 240 main evaluations of the same **20 distinct tasks**, not 240 independent tasks.','',
      f"R1 UTC: {m1['started_utc']} to {m1['updated_utc']}. R2 UTC: {m2['started_utc']} to {m2['updated_utc']}. Client timezone: Asia/Barnaul.",'',
      'Benchmark v2 used nine tasks and six architectures; its measured full runs were Lite 26/54 and Ultra 51/54. It remains archived unchanged with original data and source. Older publication-era files are separately labelled historical_unverified; missing records are not reconstructed. V3 has 4 easy, 8 medium and 8 hard preregistered tasks, each with visible examples, independent development and held-out tests, trusted references, negative/edge cases and a difficulty rationale. Before API calls, 70 development cases, 121 held-out cases and 1,285 oracle/property checks passed, together with Docker fixture validation.','',
      'Difficulty is an a-priori judgement: easy means simple scanning/indexing, medium combines boundary/state rules or a standard graph/data-structure algorithm, hard includes recursive parsing, dynamic programming, global graph problems and transactional/patch semantics. These labels are not human-calibrated; size limits do not enforce a particular asymptotic complexity. Task definitions and expected outputs were not tuned after model outcomes.','',
      'The adapter explicitly uses the frozen v2 worktree at `multiagent_llm_experiment`, base commit `5e469e9cfcb185ae9650136dc5c539a9dad50256`, with its pre-existing dirty files. All 19 Python hashes match the saved Lite snapshot; both main manifests have identical v2 source hashes. Frozen v3 preparation hashes remain checked. Exact per-run runner/source snapshots, task hashes and manifests accompany the datasets. Only repetition metadata, budgeting and execution control changed to enable repetition 2; tasks, prompts, coordinators, development tests and held-out tests did not change. All six architectures remain in the codebase.','',
      'Both models used `https://api.giga.chat/v1/`, max_tokens=4096, max feedback iterations=3, one non-streaming choice and other provider generation defaults. Host Python 3.14.4, gigachat SDK 0.2.1, Windows; unchanged pinned Docker Python 3.12.8 Alpine image. No seed control is available. These are fresh API executions, but stochastic independence cannot be verified. Serial model/architecture/task order was preserved, not randomized; temporal and provider/cache effects may confound comparisons. Automatic SDK retries were disabled. Development feedback and final held-out scoring remain separate.','',
      'The calibration pilot is cost calibration only. The earlier aborted main `d682d606a0ee4fc69d0e6b3cee054efb` remains separately preserved with seven completed observations and one unknown-billing request. Its outcomes are excluded from both complete main datasets. The user explicitly approved a full restart for main 1 and then a second balanced repetition. All historical costs and the full 69,632-token unknown-request reservation remain in the shared ledger. No third repetition was executed.','',
      'Provider-returned model identifiers: '+json.dumps(versions)+'.','',
      '## Success and resource use in each repetition','']
    report+=md_table(['Model','Architecture','R1 passed/20','R2 passed/20','R1 tokens incl. cache','R2 tokens incl. cache','R1 calls','R2 calls','R1 mean seconds','R2 mean seconds'],
      [[model,arch,*[success_cell(rep,model,arch) for rep in (1,2)],
        *[next(p for p in per_run if p['model']==model and p['architecture']==arch and p['repetition']==rep)['combined_tokens_including_cache'] for rep in (1,2)],
        *[next(p for p in per_run if p['model']==model and p['architecture']==arch and p['repetition']==rep)['llm_calls'] for rep in (1,2)],
        *[f"{next(p for p in per_run if p['model']==model and p['architecture']==arch and p['repetition']==rep)['mean_seconds']:.2f}" for rep in (1,2)]] for model in MODELS for arch in ARCHS])
    report+=['','Overall by model and repetition:','']
    report+=md_table(['Repeat','Model','Passed/60','Success','Input usage','Cached input','Output','Provider total','Combined incl. cache','Calls','Evaluation seconds'],
      [[p['repetition'],p['model'],f"{p['passed']}/60",f"{100*p['success_rate']:.1f}%",p['input_usage_tokens'],p['cached_input_tokens'],p['output_tokens'],p['provider_total_tokens'],p['combined_tokens_including_cache'],p['llm_calls'],f"{p['elapsed_seconds']:.2f}"] for p in overall])
    report+=['',f"Across the two complete main runs: {total['input_usage_tokens']:,} input usage + {total['cached_input_tokens']:,} cached input + {total['output_tokens']:,} output = **{total['combined_tokens_including_cache']:,} combined tokens**, {total['llm_calls']} LLM calls, {total['elapsed_seconds']:.2f} summed evaluation seconds. Provider total excluding cached input: {total['provider_total_tokens']:,}. All failed attempts are included in resource totals.",'',
      f"Summed client-side API latency across both complete repetitions is {sum(r['api_seconds'] for r in all_rows):.2f} seconds. Mean summed API latency per evaluation is {total['mean_api_seconds']:.2f} seconds. Evaluation time additionally includes sandbox, coordination and persistence. Complete per-evaluation latency and mean API seconds are in the CSV tables. Full response JSON and each request latency are durable in SQLite. Requested and returned identifiers are both recorded; model versions are not independently verified beyond the provider response.",'',
      f"Failures across complete main runs: {total['failures']}. Finish reasons: {audit['request_finish_reasons']}. Candidate timeouts and invalid code are not infrastructure successes. Missing usage is never zero-filled; the older unknown-billing request is excluded from measured main totals and remains reserved in budget accounting.",'',
      '![Success by repetition](research_v3/main-runs/'+second.name+'/analysis/success-by-repetition.svg)','',
      '## Task stability across repetitions','']
    report+=md_table(['Model','Architecture','Stable success','Stable failure','Improved R2','Regressed R2'],
      [[model,arch,*[sum(s['model']==model and s['architecture']==arch and s['category']==category for s in stability) for category in ['stable_success','stable_failure','improved','regressed']]] for model in MODELS for arch in ARCHS])
    report+=['','Stable failure means neither repetition passed; failure categories may differ. Every task’s name, difficulty, two statuses and stability label are in `task-stability.csv`, including all stable and changing outcomes. The observations are paired on identical tasks.','',
      '![Task stability](research_v3/main-runs/'+second.name+'/analysis/task-stability.svg)','',
      '## Paired coordination comparisons','',
      'For each task, compare a coordinated architecture with Single Agent in the same model and repetition. “Coord only” and “Single only” are discordant pairs; their difference is the observed change in passed-task count. No unpaired test or significance claim is made.','']
    report+=md_table(['Repeat','Model','Architecture','Both pass','Coord only','Single only','Both fail','Net passed-task difference'],
      [[rep,model,arch,*[sum(p[k] for p in paired if p['repetition']==rep and p['model']==model and p['architecture']==arch) for k in ['both_passed','coordination_only','single_only','both_failed']],
        sum(p['coordination_only']-p['single_only'] for p in paired if p['repetition']==rep and p['model']==model and p['architecture']==arch)] for rep in (1,2) for model in MODELS for arch in ARCHS[1:]])
    report+=['','## Predefined task difficulty','']
    report+=md_table(['Repeat','Model','Architecture','Easy /4','Medium /8','Hard /8'],
      [[rep,model,arch,*[next(d['passed'] for d in difficulty if d['repetition']==rep and d['model']==model and d['architecture']==arch and d['difficulty']==level) for level in DIFFICULTIES]] for rep in (1,2) for model in MODELS for arch in ARCHS])
    report+=['','![Difficulty and repetition](research_v3/main-runs/'+second.name+'/analysis/success-by-difficulty-two-repetitions.svg)','',
      'The lines connect predefined categories for readability and are not fitted trends. Difficulty denominators are only 4/8/8 tasks; task content and labels cannot be separated as causal factors.','',
      '## Descriptive pooled efficiency and repetition variability','',
      'The denominator below is 40 task-repetition observations per model/architecture, representing the same 20 tasks twice. It must not be interpreted as 40 independent tasks. Tokens per pass include unsuccessful attempts. Repeat-rate sample SD uses only two rates and is unstable; it is not a confidence interval.','']
    report+=md_table(['Model','Architecture','Passed /40','Tokens/pass','Ratio to Single','Repeat rate range','Sample SD (pp)'],
      [[p['model'],p['architecture'],f"{p['passed']}/40",f"{p['tokens_per_pass']:.1f}" if p['tokens_per_pass'] else 'undefined',f"{p['tokens_per_pass_relative_to_single']:.2f}" if p['tokens_per_pass_relative_to_single'] else 'undefined',f"{100*p['repeat_rate_min']:.1f}%–{100*p['repeat_rate_max']:.1f}%",f"{100*p['repeat_rate_sample_sd']:.2f}"] for p in pooled])
    report+=['','## Hypotheses and limitations','',
      'Observed coordination differences for both repetitions:','']
    for rep in (1,2):
        for model in MODELS:
            baseline=next(p for p in per_run if p['repetition']==rep and p['model']==model and p['architecture']=='single_agent')
            text=[]
            for arch in ARCHS[1:]:
                co=next(p for p in per_run if p['repetition']==rep and p['model']==model and p['architecture']==arch)
                text.append(f"{arch}: {100*(co['success_rate']-baseline['success_rate']):+.1f} pp")
            report.append(f"- R{rep}, {model}: "+'; '.join(text)+'.')
    report+=['','These paired contrasts and the difficulty table allow assessment of the direction observed in this suite. They do not justify a universal claim that stronger models benefit less from coordination. A benefit confined to one hard task, a ceiling effect on easy tasks or differences that reverse between repetitions require replication. No statistical significance, population-level or causal claim is made. Detailed changing task IDs permit inspection without post-hoc test tuning.','',
      'Only two repetitions and 20 authored tasks were observed, with dependent repeated task measurements. There is no seed control, randomized execution order or assurance of stochastic independence. Provider defaults/versions and input caching may drift. Difficulty is subjective, reference validation is dynamic rather than formal proof, and task coverage is narrow. The known adversarial sandbox RPC integrity limitation remains; Docker test passage does not establish security against intentionally malicious generated code. Future work should use independently reviewed tasks, more preregistered repetitions, counterbalanced order and stronger isolation.','',
      '## Budget, approval and preserved artifacts','',
      'The conservative preflight used existing known usage 313,152 + unknown-request reserve 69,632 + ceil(266,903 × 1.5) = 400,355 + an additional request reserve 69,632 = 852,771 tokens. The user explicitly approved increasing the target from 850,000 to 853,000 before repetition 2. The 1,000,000 hard ceiling and all prior costs/reservations remained unchanged. The approval is durable in the ledger and second manifest.','',
      f"Known usage across pilot, abandoned attempt and both complete mains: **{known:,} tokens including cache**. Unknown-billing requests: {audit['unknown_request_count']}; full retained reserve: {held:,}. Known plus reservations: **{known+held:,}**. Remaining after reservations: {target-known-held:,} to approved target {target:,}, and {1000000-known-held:,} to hard ceiling 1,000,000. The exact aggregate actual consumption remains unknown until the older unresolved request is reconciled; the reserve is an allowance, not measured usage. No third repetition was run.",'',
      f'- First complete main: `{first}`',f'- Second complete main: `{second}`',f'- Paired tables and SVG figures: `{out}`',f'- Shared ledger: `{ROOT / "research_v3/shared-budget.sqlite3"}`',
      f'- Offline analysis script: `{Path(__file__).resolve()}`',f'- First single-run report preserved: `{old_report}`',
      f'- Reproduce offline: `python compare_benchmark_v3_repetitions.py {first} {second}`','',
      'Original raw CSV, summaries, manifests and source snapshots are unchanged. The comparison reads the second run’s frozen SQLite snapshot. No API calls are performed by this script.']
    task_identification=['### Identified stable and changing tasks','',
                         'IDs map to the frozen task inventory; full task names and exact statuses are retained in task-stability.csv.','']
    task_identification+=md_table(['Model','Architecture','Stable passed IDs','Stable failed IDs','Improved IDs','Regressed IDs'],
        [[model,arch,*[', '.join(s['task_id'] for s in stability if s['model']==model and s['architecture']==arch and s['category']==category) or 'none' for category in ['stable_success','stable_failure','improved','regressed']]] for model in MODELS for arch in ARCHS])
    task_identification.append('')
    position=report.index('## Paired coordination comparisons')
    report[position:position]=task_identification
    version_note='The provider-returned versions were identical across repetitions.' if versions[1]==versions[2] else 'Provider-returned versions differed across repetitions; this weakens comparability and is not controlled by the client.'
    report.insert(report.index('## Success and resource use in each repetition'),version_note+'\n')
    findings=['### Interpretation of the two measured repetitions','',
              'Lite improves from 12/60 to 23/60, while Ultra has 53/60 in both repetitions. Equal Ultra totals hide task-level changes: three task–architecture cells improve and three regress. Across both models, 17 of the 120 matched task–architecture pairs change pass/fail outcome; the other 103 are stable. These are condition-level pairs sharing the same 20 tasks, not 120 independent tasks.','',
              'Feedback changes the passed-task count relative to Single Agent by -1 then +2 for Lite, and -1 then 0 for Ultra. Consensus changes it by -2 then 0 for Lite, and 0 then +2 for Ultra. Thus the second repetition shows some coordination gains, but the direction is architecture- and repetition-specific. The feedback contrast in R2 is compatible with a smaller Ultra benefit; the consensus contrasts do not support that generalization. Neither H1 nor H2 is established by these two repetitions.','',
              'On hard tasks, the Ultra feedback advantage seen in R1 (7/8 versus 6/8) does not repeat in R2 (6/8 versus 6/8). Lite feedback has 3/8 versus 1/8 in R2, compared with 1/8 versus 1/8 in R1. Ultra consensus reaches 7/8 hard tasks in R2 versus 6/8 for Single Agent. These narrow gains motivate replication, not causal claims about difficulty. Coordination remains substantially more token-intensive per passed solution in the pooled descriptive table.','',
              'One R2 response reached max_tokens=4096: Lite feedback on v3_13 evaluate_expression. It is preserved with finish_reason=length; the final evaluation status is candidate_timeout. The existing three-iteration feedback policy ran normally, with no transport retry or extra task evaluation. Co-occurrence alone does not establish that truncation caused the timeout.','']
    report[report.index('## Budget, approval and preserved artifacts'):report.index('## Budget, approval and preserved artifacts')]=findings
    report_path.write_text('\n'.join(report)+'\n',encoding='utf-8')
    shutil.copyfile(Path(__file__),out/'comparison-source.py')
    shutil.copyfile(ROOT/'analyze_benchmark_v3.py',out/'single-analysis-dependency.py')
    print(json.dumps(audit,indent=2))
    db.close()


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('first',type=Path);parser.add_argument('second',type=Path)
    args=parser.parse_args();compare(args.first,args.second)
