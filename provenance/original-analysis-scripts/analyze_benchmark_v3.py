"""Reproduce Benchmark v3 tables, SVG figures and English report offline.

Use python analyze_benchmark_v3.py RUN_FOLDER
No model API calls; requires matplotlib for figures.
"""
import argparse
from collections import Counter
import csv
import hashlib
import json
import math
from pathlib import Path
import sqlite3
import statistics

ROOT=Path(__file__).resolve().parent
ARCHS=['single_agent','feedback_graph','parallel_consensus']
MODELS=['GigaChat-2','GigaChat-3-Ultra']
DIFFICULTIES=['easy','medium','hard']


def save_table(path,rows):
    with path.open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)


def aggregate(rows):
    passed=sum(r['status']=='passed' for r in rows)
    total=sum(r['budget_tokens'] for r in rows)
    return {'evaluations':len(rows),'passed':passed,'success_rate':passed/len(rows),
            'input_usage_tokens':sum(int(r['input_tokens']) for r in rows),
            'cached_input_tokens':sum(r['cached_tokens'] for r in rows),
            'output_tokens':sum(int(r['output_tokens']) for r in rows),
            'provider_total_tokens':sum(int(r['total_tokens']) for r in rows),
            'combined_tokens_including_cache':total,
            'llm_calls':sum(int(r['llm_calls']) for r in rows),
            'elapsed_seconds':sum(float(r['elapsed_seconds']) for r in rows),
            'mean_seconds':statistics.mean(float(r['elapsed_seconds']) for r in rows),
            'mean_api_seconds':statistics.mean(r['api_seconds'] for r in rows),
            'tokens_per_pass':total/passed if passed else None,
            'failures':dict(Counter(r['status'] for r in rows if r['status']!='passed'))}


def md_table(headers,rows):
    return ['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(map(str,row))+' |' for row in rows]


def analyze(folder):
    folder=Path(folder).resolve()
    manifest=json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
    if manifest['status']!='complete':
        raise SystemExit('Run incomplete: preserve it, do not synthesize a complete research comparison.')
    for name,expected in manifest['runner_sha256'].items():
        assert hashlib.sha256((folder/'runner-source-snapshot'/name).read_bytes()).hexdigest()==expected,name
    with (folder/'raw_results.csv').open(encoding='utf-8',newline='') as f:
        rows=list(csv.DictReader(f))
    assert len(rows)==120
    assert len({(r['model'],r['architecture'],r['task_id'],r['repeat_index']) for r in rows})==120
    ledger_snapshot=folder/'ledger-snapshot.sqlite3'
    db=sqlite3.connect(ledger_snapshot if ledger_snapshot.exists() else ROOT/'research_v3/shared-budget.sqlite3');db.row_factory=sqlite3.Row
    requests=list(db.execute('SELECT * FROM requests WHERE experiment=? ORDER BY created',(folder.name,)))
    assert requests and all(r['state']=='complete' for r in requests)
    assert sum(int(r['llm_calls']) for r in rows)==len(requests)
    assert all(r['input_tokens']+r['output_tokens']==r['total_tokens'] for r in requests)
    for row in rows:
        key=f"{folder.name}:{row['model']}:{row['architecture']}:{row['task_id']}:1"
        group=[r for r in requests if r['evaluation']==key]
        assert sum(r['total_tokens'] for r in group)==int(row['total_tokens'])
        row['cached_tokens']=sum(json.loads(r['response'])['usage'].get('precached_prompt_tokens') or 0 for r in group)
        row['budget_tokens']=int(row['total_tokens'])+row['cached_tokens']
        row['api_seconds']=sum(r['latency'] for r in group)
        if row['final_code_path']:
            assert (folder/row['final_code_path']).is_file()
    out=folder/'analysis';out.mkdir(exist_ok=True)
    save_table(out/'evaluations.csv',rows)
    groups=[];difficulty=[];overall=[]
    for model in MODELS:
        overall.append({'model':model,**aggregate([r for r in rows if r['model']==model])})
        baseline=aggregate([r for r in rows if r['model']==model and r['architecture']=='single_agent'])
        for arch in ARCHS:
            a=aggregate([r for r in rows if r['model']==model and r['architecture']==arch])
            ratio=a['tokens_per_pass']/baseline['tokens_per_pass'] if a['tokens_per_pass'] is not None and baseline['tokens_per_pass'] else None
            groups.append({'model':model,'architecture':arch,**a,'tokens_per_pass_relative_to_single':ratio})
            for level in DIFFICULTIES:
                difficulty.append({'model':model,'architecture':arch,'difficulty':level,
                                   **aggregate([r for r in rows if r['model']==model and r['architecture']==arch and r['difficulty']==level])})
    save_table(out/'model_architecture.csv',groups)
    save_table(out/'difficulty.csv',difficulty)
    save_table(out/'overall.csv',overall)
    lookup={(r['model'],r['architecture'],r['task_id']):r for r in rows}
    differences=[]
    for task in sorted({r['task_id'] for r in rows}):
        for arch in ARCHS:
            l=lookup[MODELS[0],arch,task];u=lookup[MODELS[1],arch,task]
            differences.append({'task_id':task,'task_name':l['task_name'],'difficulty':l['difficulty'],
                                'architecture':arch,'lite_status':l['status'],'ultra_status':u['status']})
    save_table(out/'paired_task_results.csv',differences)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'svg.hashsalt':'benchmark-v3','font.family':'DejaVu Sans','font.size':10})
    colors=['#336699','#e68a2e','#41955d']
    fig,axes=plt.subplots(1,2,figsize=(11,4),sharey=True)
    for ax,model in zip(axes,MODELS):
        for index,arch in enumerate(ARCHS):
            selected=[next(d for d in difficulty if d['model']==model and d['architecture']==arch and d['difficulty']==level) for level in DIFFICULTIES]
            positions=[i+(index-1)*0.24 for i in range(3)]
            bars=ax.bar(positions,[100*d['success_rate'] for d in selected],width=.23,color=colors[index],label=arch)
            for bar,d in zip(bars,selected):
                ax.text(bar.get_x()+bar.get_width()/2,bar.get_height()+1,f"{d['passed']}/{d['evaluations']}",ha='center',fontsize=8)
        ax.set_title(model);ax.set_xticks(range(3),['Easy (4)','Medium (8)','Hard (8)']);ax.set_ylim(0,113)
        ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
    axes[0].set_ylabel('Held-out success (%)')
    axes[1].legend(loc='upper center',bbox_to_anchor=(.5,-.15),ncol=1,frameon=False)
    fig.suptitle('Benchmark v3: one repetition; descriptive task counts')
    fig.tight_layout();fig.savefig(out/'success_by_difficulty.svg',metadata={'Date':None});fig.savefig(out/'success_by_difficulty.png',dpi=140);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(11,4),sharey=True)
    for ax,model in zip(axes,MODELS):
        selected=[g for g in groups if g['model']==model]
        bars=ax.bar(range(3),[g['combined_tokens_including_cache'] for g in selected],color=colors)
        ax.set_xticks(range(3),['Single','Feedback','Consensus']);ax.set_title(model)
        for bar,g in zip(bars,selected):
            ax.text(bar.get_x()+bar.get_width()/2,bar.get_height(),f"{g['combined_tokens_including_cache']:,}",ha='center',va='bottom')
        ax.margins(y=.15);ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
    axes[0].set_ylabel('Input including cache + output tokens')
    fig.suptitle('Measured main-run token use; failures included')
    fig.tight_layout();fig.savefig(out/'tokens_by_architecture.svg',metadata={'Date':None});fig.savefig(out/'tokens_by_architecture.png',dpi=140);plt.close(fig)
    budget=list(db.execute('SELECT * FROM requests'))
    known=sum((r['total_tokens'] or 0)+(json.loads(r['response'])['usage'].get('precached_prompt_tokens') or 0 if r['response'] else 0) for r in budget)
    held=sum(r['input_reserve']+r['output_reserve'] for r in budget if r['state']!='complete')
    unknown=sum(r['state']!='complete' for r in budget)
    versions=sorted({(r['model'],r['returned_model']) for r in requests})
    finish=Counter(r['finish_reason'] for r in requests)
    main=aggregate(rows)
    audit={'main':main,'all_v3_known_including_cache':known,'unknown_billing_requests':unknown,
           'retained_reservations':held,'known_plus_reservations':known+held,
           'remaining_hard_after_reservations':1000000-known-held,'remaining_target_after_reservations':850000-known-held,
           'returned_models':versions,'finish_reasons':dict(finish)}
    (out/'audit.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
    source=json.loads((folder/'source-manifest.json').read_text(encoding='utf-8'))
    report=['# Benchmark v3: capability, task difficulty and multi-agent coordination','',
      f"Run start (UTC): {manifest['started_utc']}; completion (UTC): {manifest['updated_utc']}. Client reporting timezone: Asia/Barnaul (12 November 2026).",'',
      '## Research question and preregistered hypotheses','',
      'Does multi-agent coordination provide measurable benefits over a single LLM as programming-task difficulty increases? H1 predicts a larger coordination advantage on harder tasks; H2 predicts a smaller advantage for the stronger model. These are hypotheses, not assumptions. This report describes one balanced repetition and does not support causal or population-level claims.','',
      '## Evidence lineage: historical data, v2 and v3','',
      'Older publication-era files are archived under historical_unverified, without reconstructing missing records or asserting their provenance. Completed v2 Lite/Ultra runs and pilots, original CSVs, manifests, sources and limitations are preserved in research_archive/benchmark-v2-originals.zip. V2 used nine tasks and six architectures: Lite 26/54, Ultra 51/54 in the previously measured full runs. These are historical measurements on a different task suite, not a controlled comparison with v3.','',
      f"V3 run `{folder.name}` contains 20 new preregistered tasks, 2 models, 3 architectures and exactly one repeat: 120 evaluations. The initial main attempt `d682d606a0ee4fc69d0e6b3cee054efb` stopped after seven completed evaluations and an unknown-billing request. The user explicitly authorized a fresh complete main run. None of the seven prior results or pilot outcomes replaces a cell in this dataset. All prior costs and the unknown request's full 69,632-token reserve remain in the shared budget. This is a disclosed full restart, not selective retries of low-scoring solutions.",'',
      '## Methodology and environment','',
      f"Frozen v2 source: `{source['v2_path']}`, base commit `{source['git_revision']}` with pre-existing dirty tracked files. All 19 Python files match the Lite source snapshot. V3 contracts, references and expected outputs match the preparation hashes. Exact runner/source hashes and snapshots accompany the run. The adapter reuses the original coordination and evaluation implementations; six architectures remain in the codebase, three selected here. API transport and budget controls are a separate adapter. No coordination prompt, task or expected output was tuned to model performance.",'',
      'Both requested models used https://api.giga.chat/v1/. Max feedback iterations = 3. The user explicitly approved max_tokens=4096 for both models, one non-streaming choice, all other generation parameters at provider defaults. This differs from the initial provider-default plan and is disclosed. No seed control is available. Requests were serial with automatic SDK retries disabled. Sources, endpoint, requested/returned model versions, per-response usage and latency, task IDs and repetition are preserved.','',
      f"Host Python {manifest['python']}, SDK gigachat {manifest['sdk_version']}, Windows; pinned Docker image python:3.12.8-alpine3.20@sha256:3b1df87fc50e7d47762aeb48673736079aa22e7c98c8851f5453dd49fc03ad1b. Candidate timeout remains 5 seconds. Development and held-out tests are separate; only development diagnostics can enter model context. Final scoring uses the held-out set. Candidate and infrastructure failures are never counted as passed.",'',
      'The calibration pilot crossed one preselected easy/medium/hard task with both models and all selected architectures. Weighting pilot usage by 4/8/8, adding a 50% margin and one request reserve led to one balanced repetition. After explicit restart approval, the same planning check included all abandoned-attempt costs and the retained unknown reserve.','',
      '## Task difficulty definitions','',
      'Easy (4 tasks): single-pass or simple indexing/state transformations. Medium (8): several interacting boundary/state rules or one standard graph/data-structure algorithm. Hard (8): recursive grammars, dynamic programming, global graph algorithms, transactional state or patch semantics. Difficulty is an a-priori judgement and has not been calibrated on a human sample. Size limits do not enforce asymptotic complexity. Exact contracts, visible examples, rationales and split cases are in the frozen task inventory. References passed 70 development cases, 121 held-out cases, 1,285 additional oracle/property checks and Docker validation before API experiments.','',
      '## Model and architecture results','']
    report+=md_table(['Model','Architecture','Passed / 20','Success','Input usage','Cached input','Output','Provider total','Combined incl. cache','Calls','Mean seconds'],
        [[g['model'],g['architecture'],f"{g['passed']}/20",f"{100*g['success_rate']:.1f}%",g['input_usage_tokens'],g['cached_input_tokens'],g['output_tokens'],g['provider_total_tokens'],g['combined_tokens_including_cache'],g['llm_calls'],f"{g['mean_seconds']:.2f}"] for g in groups])
    report+=['','Overall measured model totals:','']
    report+=md_table(['Model','Success','Input usage','Cached input','Output','Provider total','Combined incl. cache','Calls','Elapsed seconds'],
      [[g['model'],f"{g['passed']}/60 ({100*g['success_rate']:.1f}%)",g['input_usage_tokens'],g['cached_input_tokens'],g['output_tokens'],g['provider_total_tokens'],g['combined_tokens_including_cache'],g['llm_calls'],f"{g['elapsed_seconds']:.2f}"] for g in overall])
    report+=['','Provider prompt_tokens/total_tokens exclude cached input in these responses. The conservative combined measure is prompt_tokens + precached_prompt_tokens + completion_tokens. All raw usage fields are retained. These are token counts, not monetary costs.','',
      f"Main-run total: {main['provider_total_tokens']:,} provider-total tokens; {main['combined_tokens_including_cache']:,} including cached input, {main['llm_calls']} calls and {main['elapsed_seconds']:.2f} summed evaluation seconds. Failure categories: {json.dumps(main['failures'])}. Finish reasons: {dict(finish)}. No missing usage is present in this completed run. The earlier abandoned attempt's usage remains partly unknown and is not silently replaced by zero.",'',
      'Provider-returned identifiers: '+', '.join(f'`{a}` → `{b}`' for a,b in versions)+'.','',
      '## Results by predefined difficulty','']
    report+=md_table(['Model','Architecture','Difficulty','Passed / tasks','Success','Combined tokens','Calls','Mean seconds'],
      [[d['model'],d['architecture'],d['difficulty'],f"{d['passed']}/{d['evaluations']}",f"{100*d['success_rate']:.1f}%",d['combined_tokens_including_cache'],d['llm_calls'],f"{d['mean_seconds']:.2f}"] for d in difficulty])
    report+=['','![Held-out correctness by difficulty](research_v3/main-runs/'+folder.name+'/analysis/success_by_difficulty.svg)','',
      'Figure: descriptive counts from one repetition, denominators 4/8/8 per architecture and model; no inferential error bars. Repeated uses of the same tasks across architectures are not independent task samples.','',
      '## Token efficiency relative to Single Agent','',
      'Tokens per passed solution include the complete token use of unsuccessful attempts in the numerator. The relative ratio divides this measure by the same model’s Single Agent value; values above 1 mean more tokens per observed passed solution. The ratio is descriptive and unstable when few solutions pass.','']
    report+=md_table(['Model','Architecture','Combined tokens per pass','Ratio to Single Agent'],
      [[g['model'],g['architecture'],f"{g['tokens_per_pass']:.1f}" if g['tokens_per_pass'] is not None else 'undefined',f"{g['tokens_per_pass_relative_to_single']:.2f}" if g['tokens_per_pass_relative_to_single'] is not None else 'undefined'] for g in groups])
    report+=['','![Measured token use](research_v3/main-runs/'+folder.name+'/analysis/tokens_by_architecture.svg)','',
      '## Coordination and stronger capability','',
      'Observed coordination gains in passed-task counts relative to the same model’s Single Agent baseline:','']
    report+=md_table(['Model','Difficulty','Feedback minus Single','Consensus minus Single'],
      [[model,level,
        next(d['passed'] for d in difficulty if d['model']==model and d['architecture']=='feedback_graph' and d['difficulty']==level)-next(d['passed'] for d in difficulty if d['model']==model and d['architecture']=='single_agent' and d['difficulty']==level),
        next(d['passed'] for d in difficulty if d['model']==model and d['architecture']=='parallel_consensus' and d['difficulty']==level)-next(d['passed'] for d in difficulty if d['model']==model and d['architecture']=='single_agent' and d['difficulty']==level)] for model in MODELS for level in DIFFICULTIES])
    wins=sum(d['lite_status']!='passed' and d['ultra_status']=='passed' for d in differences)
    losses=sum(d['lite_status']=='passed' and d['ultra_status']!='passed' for d in differences)
    report+=['',f'Across the 60 matched task–architecture cells, Ultra passed where Lite did not in {wins} cells; Lite passed where Ultra did not in {losses}. Complete task-level status pairs are in paired_task_results.csv. These paired cells reuse 20 tasks and must not be treated as 60 independent tasks.','',
      'The tables show the direction and magnitude observed in this sample. They do not establish that task difficulty or stronger capability caused a change in coordination benefit. Differences in generated code, development-test selection, truncation and local test behavior can contribute; no internal model reasoning is observed. An apparent gain concentrated in one task is not evidence of a robust difficulty interaction.','',
      '## Uncertainty and limitations','',
      'There is exactly one main repetition. Between-repetition variance, standard errors over repetitions and repeat-level confidence intervals cannot be estimated; they are unavailable, not zero. Difficulty groups have only 4/8/8 tasks, and tasks are reused across architectures/models. No significance test, causal claim or population-level conclusion is made. The small calibration sample and token forecasts have substantial uncertainty. Tasks were authored and dynamically validated, not formally verified, and difficulty labels remain subjective. Provider versions/defaults may drift. Execution order was model then architecture then task, so temporal/provider effects are not randomized away.','',
      'The prior aborted run and full restart are disclosed; their token costs are included in the budget, their scores are excluded from the balanced main analysis. Unknown billing remains unresolved under a full reserved allowance. The known adversarial RPC integrity limitation remains: Docker test passage does not establish security against intentionally malicious generated code.','',
      'Future work should use independently reviewed and more numerous tasks, balanced preregistered repetitions where budget permits, randomized/counterbalanced ordering, version-pinned providers and stronger isolation before considering untrusted adversarial code. Do not tune this suite’s expected outputs after observing outcomes.','',
      '## Total v3 budget and artifacts','',
      f'Across pilot, abandoned attempt and this main run, known usage including cached input is {known:,} tokens. There are {unknown} unknown-billing requests, retaining {held:,} tokens. Known usage plus reservations: {known+held:,}; remaining after reservations: {1000000-known-held:,} to the 1,000,000 ceiling and {850000-known-held:,} to the 850,000 target. The exact aggregate actual consumption is unknown until the prior request is reconciled; the reserve is an allowance, not measured consumption. No additional repetitions were run.','',
      f'- Main run: `{folder}`',f'- Shared ledger: `{ROOT / "research_v3/shared-budget.sqlite3"}`',
      f'- Analysis tables and SVGs: `{out}`',f'- Analysis script: `{Path(__file__).resolve()}`',
      '- Reproduce offline: `python analyze_benchmark_v3.py '+str(folder)+'`','',
      'All original CSV, summaries, manifests, returned JSON and generated solutions are preserved. The main manifest and source snapshots identify the exact measured revision. This analysis script performs no API requests.']
    discussion=['## Descriptive answers to the hypotheses','']
    for arch in ARCHS[1:]:
        gains={}
        for model in MODELS:
            baseline=next(g for g in groups if g['model']==model and g['architecture']=='single_agent')
            coordinated=next(g for g in groups if g['model']==model and g['architecture']==arch)
            gains[model]=100*(coordinated['success_rate']-baseline['success_rate'])
        direction='equal' if math.isclose(gains[MODELS[1]],gains[MODELS[0]],abs_tol=1e-8) else ('smaller' if gains[MODELS[1]]<gains[MODELS[0]] else 'larger')
        discussion.append(f"For {arch}, the observed coordination difference is {gains[MODELS[0]]:+.1f} percentage points for Lite and {gains[MODELS[1]]:+.1f} for Ultra. Ultra's difference is {direction} in this sample. This describes the model-by-architecture contrast for these tasks, not a capability-induced causal effect.")
        discussion.append('')
        for model in MODELS:
            gaps=[]
            for level in DIFFICULTIES:
                b=next(d for d in difficulty if d['model']==model and d['architecture']=='single_agent' and d['difficulty']==level)
                a=next(d for d in difficulty if d['model']==model and d['architecture']==arch and d['difficulty']==level)
                gaps.append(100*(a['success_rate']-b['success_rate']))
            discussion.append(f"{model}, {arch}: easy/medium/hard differences are "+', '.join(f'{n:+.1f} pp' for n in gaps)+'. These are differences in observed proportions, with only 4/8/8 task denominators.')
        discussion.append('')
    discussion+=['Observed generation behavior (not internal reasoning):','']
    for model in MODELS:
        feedback=[r for r in rows if r['model']==model and r['architecture']=='feedback_graph']
        discussion.append(f"- {model}: feedback iteration counts {dict(sorted(Counter(int(r['iterations']) for r in feedback).items()))}; mean feedback LLM calls {statistics.mean(int(r['llm_calls']) for r in feedback):.2f}.")
    discussion+=['','The observed call/iteration distributions and output-token totals can help explain cost differences. They do not establish why a model changed an answer. Held-out correctness may differ even after development tests pass, because the final tests are distinct.','']
    discussion+=['Task-specific coordination changes relative to Single Agent:','']
    for model in MODELS:
        baseline={r['task_id']:r for r in rows if r['model']==model and r['architecture']=='single_agent'}
        for arch in ARCHS[1:]:
            selected=[r for r in rows if r['model']==model and r['architecture']==arch]
            added=[r['task_id']+' '+r['task_name'] for r in selected if r['status']=='passed' and baseline[r['task_id']]['status']!='passed']
            lost=[r['task_id']+' '+r['task_name'] for r in selected if r['status']!='passed' and baseline[r['task_id']]['status']=='passed']
            discussion.append(f"- {model}, {arch}: additional passes: {', '.join(added) or 'none'}; lost passes: {', '.join(lost) or 'none'}.")
    discussion+=['','There is no overall coordination improvement over Single Agent for either model in this measured run. Ultra feedback improves the hard subset by one task (7/8 versus 6/8), but loses two medium tasks. The overall feedback difference is the same for both models (-5 percentage points); the consensus difference is -10 points for Lite and 0 for Ultra. Thus the broad claim that stronger capability reduces coordination benefit is not supported by these overall contrasts. The hard-task feedback observation is a narrow signal for future preregistered replication, not a confirmed difficulty interaction.','']
    insertion=report.index('## Uncertainty and limitations')
    report[insertion:insertion]=discussion
    (ROOT/'benchmark-v3-research-report.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
    print(json.dumps(audit,indent=2))
    db.close()


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('folder',type=Path)
    analyze(parser.parse_args().folder)
