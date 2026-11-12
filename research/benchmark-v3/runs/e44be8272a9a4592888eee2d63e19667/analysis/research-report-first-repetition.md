# Benchmark v3: capability, task difficulty and multi-agent coordination

Run start (UTC): 2026-11-11T17:03:36.455568+00:00; completion (UTC): 2026-11-11T17:22:37.566344+00:00. Client reporting timezone: Asia/Barnaul (12 November 2026).

## Research question and preregistered hypotheses

Does multi-agent coordination provide measurable benefits over a single LLM as programming-task difficulty increases? H1 predicts a larger coordination advantage on harder tasks; H2 predicts a smaller advantage for the stronger model. These are hypotheses, not assumptions. This report describes one balanced repetition and does not support causal or population-level claims.

## Evidence lineage: historical data, v2 and v3

Older publication-era files are archived under historical_unverified, without reconstructing missing records or asserting their provenance. Completed v2 Lite/Ultra runs and pilots, original CSVs, manifests, sources and limitations are preserved in research_archive/benchmark-v2-originals.zip. V2 used nine tasks and six architectures: Lite 26/54, Ultra 51/54 in the previously measured full runs. These are historical measurements on a different task suite, not a controlled comparison with v3.

V3 run `e44be8272a9a4592888eee2d63e19667` contains 20 new preregistered tasks, 2 models, 3 architectures and exactly one repeat: 120 evaluations. The initial main attempt `d682d606a0ee4fc69d0e6b3cee054efb` stopped after seven completed evaluations and an unknown-billing request. The user explicitly authorized a fresh complete main run. None of the seven prior results or pilot outcomes replaces a cell in this dataset. All prior costs and the unknown request's full 69,632-token reserve remain in the shared budget. This is a disclosed full restart, not selective retries of low-scoring solutions.

## Methodology and environment

Frozen v2 source: `multiagent_llm_experiment`, base commit `5e469e9cfcb185ae9650136dc5c539a9dad50256` with pre-existing dirty tracked files. All 19 Python files match the Lite source snapshot. V3 contracts, references and expected outputs match the preparation hashes. Exact runner/source hashes and snapshots accompany the run. The adapter reuses the original coordination and evaluation implementations; six architectures remain in the codebase, three selected here. API transport and budget controls are a separate adapter. No coordination prompt, task or expected output was tuned to model performance.

Both requested models used https://api.giga.chat/v1/. Max feedback iterations = 3. The user explicitly approved max_tokens=4096 for both models, one non-streaming choice, all other generation parameters at provider defaults. This differs from the initial provider-default plan and is disclosed. No seed control is available. Requests were serial with automatic SDK retries disabled. Sources, endpoint, requested/returned model versions, per-response usage and latency, task IDs and repetition are preserved.

Host Python 3.14.4, SDK gigachat 0.2.1, Windows; pinned Docker image python:3.12.8-alpine3.20@sha256:3b1df87fc50e7d47762aeb48673736079aa22e7c98c8851f5453dd49fc03ad1b. Candidate timeout remains 5 seconds. Development and held-out tests are separate; only development diagnostics can enter model context. Final scoring uses the held-out set. Candidate and infrastructure failures are never counted as passed.

The calibration pilot crossed one preselected easy/medium/hard task with both models and all selected architectures. Weighting pilot usage by 4/8/8, adding a 50% margin and one request reserve led to one balanced repetition. After explicit restart approval, the same planning check included all abandoned-attempt costs and the retained unknown reserve.

## Task difficulty definitions

Easy (4 tasks): single-pass or simple indexing/state transformations. Medium (8): several interacting boundary/state rules or one standard graph/data-structure algorithm. Hard (8): recursive grammars, dynamic programming, global graph algorithms, transactional state or patch semantics. Difficulty is an a-priori judgement and has not been calibrated on a human sample. Size limits do not enforce asymptotic complexity. Exact contracts, visible examples, rationales and split cases are in the frozen task inventory. References passed 70 development cases, 121 held-out cases, 1,285 additional oracle/property checks and Docker validation before API experiments.

## Model and architecture results

| Model | Architecture | Passed / 20 | Success | Input usage | Cached input | Output | Provider total | Combined incl. cache | Calls | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GigaChat-2 | single_agent | 5/20 | 25.0% | 5227 | 0 | 4063 | 9290 | 9290 | 20 | 3.10 |
| GigaChat-2 | feedback_graph | 4/20 | 20.0% | 46672 | 7167 | 16160 | 62832 | 69999 | 124 | 12.78 |
| GigaChat-2 | parallel_consensus | 3/20 | 15.0% | 37475 | 9229 | 18488 | 55963 | 65192 | 120 | 15.35 |
| GigaChat-3-Ultra | single_agent | 18/20 | 90.0% | 5087 | 0 | 3823 | 8910 | 8910 | 20 | 2.80 |
| GigaChat-3-Ultra | feedback_graph | 17/20 | 85.0% | 33448 | 768 | 11653 | 45101 | 45869 | 85 | 8.24 |
| GigaChat-3-Ultra | parallel_consensus | 18/20 | 90.0% | 44193 | 3264 | 20186 | 64379 | 67643 | 120 | 13.72 |

Overall measured model totals:

| Model | Success | Input usage | Cached input | Output | Provider total | Combined incl. cache | Calls | Elapsed seconds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GigaChat-2 | 12/60 (20.0%) | 89374 | 16396 | 38711 | 128085 | 144481 | 264 | 624.61 |
| GigaChat-3-Ultra | 53/60 (88.3%) | 82728 | 4032 | 35662 | 118390 | 122422 | 225 | 495.24 |

Provider prompt_tokens/total_tokens exclude cached input in these responses. The conservative combined measure is prompt_tokens + precached_prompt_tokens + completion_tokens. All raw usage fields are retained. These are token counts, not monetary costs.

Main-run total: 246,475 provider-total tokens; 266,903 including cached input, 489 calls and 1119.85 summed evaluation seconds. Failure categories: {"failed_tests": 53, "candidate_timeout": 1, "invalid_code": 1}. Finish reasons: {'stop': 489}. No missing usage is present in this completed run. The earlier abandoned attempt's usage remains partly unknown and is not silently replaced by zero.

Provider-returned identifiers: `GigaChat-2` → `GigaChat-2:2.0.30.01`, `GigaChat-3-Ultra` → `GigaChat-3-Ultra:32.9.16.9`.

## Results by predefined difficulty

| Model | Architecture | Difficulty | Passed / tasks | Success | Combined tokens | Calls | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GigaChat-2 | single_agent | easy | 2/4 | 50.0% | 1357 | 4 | 2.52 |
| GigaChat-2 | single_agent | medium | 2/8 | 25.0% | 4162 | 8 | 3.37 |
| GigaChat-2 | single_agent | hard | 1/8 | 12.5% | 3771 | 8 | 3.12 |
| GigaChat-2 | feedback_graph | easy | 1/4 | 25.0% | 10171 | 24 | 9.53 |
| GigaChat-2 | feedback_graph | medium | 2/8 | 25.0% | 29159 | 49 | 13.48 |
| GigaChat-2 | feedback_graph | hard | 1/8 | 12.5% | 30669 | 51 | 13.70 |
| GigaChat-2 | parallel_consensus | easy | 1/4 | 25.0% | 10605 | 24 | 13.43 |
| GigaChat-2 | parallel_consensus | medium | 1/8 | 12.5% | 26374 | 48 | 17.94 |
| GigaChat-2 | parallel_consensus | hard | 1/8 | 12.5% | 28213 | 48 | 13.72 |
| GigaChat-3-Ultra | single_agent | easy | 4/4 | 100.0% | 1258 | 4 | 2.24 |
| GigaChat-3-Ultra | single_agent | medium | 8/8 | 100.0% | 3528 | 8 | 2.70 |
| GigaChat-3-Ultra | single_agent | hard | 6/8 | 75.0% | 4124 | 8 | 3.19 |
| GigaChat-3-Ultra | feedback_graph | easy | 4/4 | 100.0% | 5940 | 16 | 6.17 |
| GigaChat-3-Ultra | feedback_graph | medium | 6/8 | 75.0% | 18891 | 35 | 8.78 |
| GigaChat-3-Ultra | feedback_graph | hard | 7/8 | 87.5% | 21038 | 34 | 8.75 |
| GigaChat-3-Ultra | parallel_consensus | easy | 4/4 | 100.0% | 9585 | 24 | 10.78 |
| GigaChat-3-Ultra | parallel_consensus | medium | 8/8 | 100.0% | 26653 | 48 | 13.29 |
| GigaChat-3-Ultra | parallel_consensus | hard | 6/8 | 75.0% | 31405 | 48 | 15.62 |

![Held-out correctness by difficulty](research_v3/main-runs/e44be8272a9a4592888eee2d63e19667/analysis/success_by_difficulty.svg)

Figure: descriptive counts from one repetition, denominators 4/8/8 per architecture and model; no inferential error bars. Repeated uses of the same tasks across architectures are not independent task samples.

## Token efficiency relative to Single Agent

Tokens per passed solution include the complete token use of unsuccessful attempts in the numerator. The relative ratio divides this measure by the same model’s Single Agent value; values above 1 mean more tokens per observed passed solution. The ratio is descriptive and unstable when few solutions pass.

| Model | Architecture | Combined tokens per pass | Ratio to Single Agent |
| --- | --- | --- | --- |
| GigaChat-2 | single_agent | 1858.0 | 1.00 |
| GigaChat-2 | feedback_graph | 17499.8 | 9.42 |
| GigaChat-2 | parallel_consensus | 21730.7 | 11.70 |
| GigaChat-3-Ultra | single_agent | 495.0 | 1.00 |
| GigaChat-3-Ultra | feedback_graph | 2698.2 | 5.45 |
| GigaChat-3-Ultra | parallel_consensus | 3757.9 | 7.59 |

![Measured token use](research_v3/main-runs/e44be8272a9a4592888eee2d63e19667/analysis/tokens_by_architecture.svg)

## Coordination and stronger capability

Observed coordination gains in passed-task counts relative to the same model’s Single Agent baseline:

| Model | Difficulty | Feedback minus Single | Consensus minus Single |
| --- | --- | --- | --- |
| GigaChat-2 | easy | -1 | -1 |
| GigaChat-2 | medium | 0 | -1 |
| GigaChat-2 | hard | 0 | 0 |
| GigaChat-3-Ultra | easy | 0 | 0 |
| GigaChat-3-Ultra | medium | -2 | 0 |
| GigaChat-3-Ultra | hard | 1 | 0 |

Across the 60 matched task–architecture cells, Ultra passed where Lite did not in 41 cells; Lite passed where Ultra did not in 0. Complete task-level status pairs are in paired_task_results.csv. These paired cells reuse 20 tasks and must not be treated as 60 independent tasks.

The tables show the direction and magnitude observed in this sample. They do not establish that task difficulty or stronger capability caused a change in coordination benefit. Differences in generated code, development-test selection, truncation and local test behavior can contribute; no internal model reasoning is observed. An apparent gain concentrated in one task is not evidence of a robust difficulty interaction.

## Descriptive answers to the hypotheses

For feedback_graph, the observed coordination difference is -5.0 percentage points for Lite and -5.0 for Ultra. Ultra's difference is equal in this sample. This describes the model-by-architecture contrast for these tasks, not a capability-induced causal effect.

GigaChat-2, feedback_graph: easy/medium/hard differences are -25.0 pp, +0.0 pp, +0.0 pp. These are differences in observed proportions, with only 4/8/8 task denominators.
GigaChat-3-Ultra, feedback_graph: easy/medium/hard differences are +0.0 pp, -25.0 pp, +12.5 pp. These are differences in observed proportions, with only 4/8/8 task denominators.

For parallel_consensus, the observed coordination difference is -10.0 percentage points for Lite and +0.0 for Ultra. Ultra's difference is larger in this sample. This describes the model-by-architecture contrast for these tasks, not a capability-induced causal effect.

GigaChat-2, parallel_consensus: easy/medium/hard differences are -25.0 pp, -12.5 pp, +0.0 pp. These are differences in observed proportions, with only 4/8/8 task denominators.
GigaChat-3-Ultra, parallel_consensus: easy/medium/hard differences are +0.0 pp, +0.0 pp, +0.0 pp. These are differences in observed proportions, with only 4/8/8 task denominators.

Observed generation behavior (not internal reasoning):

- GigaChat-2: feedback iteration counts {1: 5, 2: 2, 3: 13}; mean feedback LLM calls 6.20.
- GigaChat-3-Ultra: feedback iteration counts {1: 18, 2: 1, 3: 1}; mean feedback LLM calls 4.25.

The observed call/iteration distributions and output-token totals can help explain cost differences. They do not establish why a model changed an answer. Held-out correctness may differ even after development tests pass, because the final tests are distinct.

Task-specific coordination changes relative to Single Agent:

- GigaChat-2, feedback_graph: additional passes: none; lost passes: v3_04 merge_records.
- GigaChat-2, parallel_consensus: additional passes: none; lost passes: v3_04 merge_records, v3_07 window_minima.
- GigaChat-3-Ultra, feedback_graph: additional passes: v3_13 evaluate_expression; lost passes: v3_08 build_layers, v3_11 subtract_intervals.
- GigaChat-3-Ultra, parallel_consensus: additional passes: none; lost passes: none.

There is no overall coordination improvement over Single Agent for either model in this measured run. Ultra feedback improves the hard subset by one task (7/8 versus 6/8), but loses two medium tasks. The overall feedback difference is the same for both models (-5 percentage points); the consensus difference is -10 points for Lite and 0 for Ultra. Thus the broad claim that stronger capability reduces coordination benefit is not supported by these overall contrasts. The hard-task feedback observation is a narrow signal for future preregistered replication, not a confirmed difficulty interaction.

## Uncertainty and limitations

There is exactly one main repetition. Between-repetition variance, standard errors over repetitions and repeat-level confidence intervals cannot be estimated; they are unavailable, not zero. Difficulty groups have only 4/8/8 tasks, and tasks are reused across architectures/models. No significance test, causal claim or population-level conclusion is made. The small calibration sample and token forecasts have substantial uncertainty. Tasks were authored and dynamically validated, not formally verified, and difficulty labels remain subjective. Provider versions/defaults may drift. Execution order was model then architecture then task, so temporal/provider effects are not randomized away.

The prior aborted run and full restart are disclosed; their token costs are included in the budget, their scores are excluded from the balanced main analysis. Unknown billing remains unresolved under a full reserved allowance. The known adversarial RPC integrity limitation remains: Docker test passage does not establish security against intentionally malicious generated code.

Future work should use independently reviewed and more numerous tasks, balanced preregistered repetitions where budget permits, randomized/counterbalanced ordering, version-pinned providers and stronger isolation before considering untrusted adversarial code. Do not tune this suite’s expected outputs after observing outcomes.

## Total v3 budget and artifacts

Across pilot, abandoned attempt and this main run, known usage including cached input is 313,152 tokens. There are 1 unknown-billing requests, retaining 69,632 tokens. Known usage plus reservations: 382,784; remaining after reservations: 617,216 to the 1,000,000 ceiling and 467,216 to the 850,000 target. The exact aggregate actual consumption is unknown until the prior request is reconciled; the reserve is an allowance, not measured consumption. No additional repetitions were run.

- Main run: `$ORIGINAL_WORKSPACE\research_v3\main-runs\e44be8272a9a4592888eee2d63e19667`
- Shared ledger: `$ORIGINAL_WORKSPACE\research_v3\shared-budget.sqlite3`
- Analysis tables and SVGs: `$ORIGINAL_WORKSPACE\research_v3\main-runs\e44be8272a9a4592888eee2d63e19667\analysis`
- Analysis script: `$ORIGINAL_WORKSPACE\analyze_benchmark_v3.py`
- Reproduce offline: `python analyze_benchmark_v3.py $ORIGINAL_WORKSPACE\research_v3\main-runs\e44be8272a9a4592888eee2d63e19667`

All original CSV, summaries, manifests, returned JSON and generated solutions are preserved. The main manifest and source snapshots identify the exact measured revision. This analysis script performs no API requests.
