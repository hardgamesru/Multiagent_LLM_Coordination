# Multiagent LLM Coordination — Benchmark v3

Research publication branch `research-v3`, based on `sandbox-integrity` commit
`5e469e9cfcb185ae9650136dc5c539a9dad50256` plus the measured local implementation.
No model API access is required to validate or reproduce the published analysis.

## Read the research

- [English research report](research/benchmark-v3/report.md)
- [R1 measured results](research/benchmark-v3/runs/e44be8272a9a4592888eee2d63e19667) — 120 evaluations
- [R2 measured results](research/benchmark-v3/runs/adbb87a0aa394be6a8319624686f12fd) — 120 new evaluations
- [Paired tables and SVG figures](research/benchmark-v3/runs/adbb87a0aa394be6a8319624686f12fd/analysis)
- [Provenance and privacy](provenance/README.md)

| Model / architecture | R1 passed / 20 | R2 passed / 20 |
|---|---:|---:|
| GigaChat-2 / single_agent | 5 | 7 |
| GigaChat-2 / feedback_graph | 4 | 9 |
| GigaChat-2 / parallel_consensus | 3 | 7 |
| GigaChat-3-Ultra / single_agent | 18 | 17 |
| GigaChat-3-Ultra / feedback_graph | 17 | 17 |
| GigaChat-3-Ultra / parallel_consensus | 18 | 19 |

There are 20 distinct tasks measured twice across six model–architecture conditions,
not 240 independent tasks. Outcomes depend on architecture and repetition; these
data do not establish a universal or causal coordination advantage. No seed control
is available. See the report for paired difficulty analyses and limitations.

## Reproduce offline

Python 3.12+ is supported. Install into a virtual environment:

```sh
python -m pip install -r requirements.txt
python -m unittest benchmark_v3.test_runner benchmark_v3.test_validation tests.test_publication -v
python tools/verify_publication.py
MPLBACKEND=Agg python tools/reproduce.py
```

On Windows, set `MPLBACKEND=Agg` in the shell or omit it (the script sets Agg).
Reproduction uses preserved CSV and privacy-minimized usage metadata, with an
in-memory SQLite adapter. It does not call a model or require credentials. Existing
CSV tables are verified numerically and kept byte-identical; SVGs/report regenerate.

## Evidence boundaries

| Area | Meaning |
|---|---|
| [Historical conference-era files](historical/conference/README.md) | Existing legacy artifacts, preserved without reconstructing missing provenance |
| [Benchmark v2](research/benchmark-v2/README.md) | Nine-task protocol and completed Lite/Ultra experiments |
| [Benchmark v3](research/benchmark-v3/report.md) | Frozen 20-task suite and two balanced main repetitions |
| `multiagent_llm_experiment/` | Exact measured backend; all six architectures retained; legacy results/solutions remain in place |
| `benchmark_v3/` | Immutable task definitions, trusted references, validation and portable publication runner |

Historical conference results are not directly compared with v3. The v3 pilot and
earlier aborted run are separate from the two completed main datasets. The older
unknown-billing request retains a 69,632-token reservation; it is never zero-filled.

## New API experiments

No further paid experiments are authorized by this release. The runner requires
`--enable-paid` for any generation command. It uses ignored private local state;
the original private ledger is not published. A future researcher must explicitly
authorize their own budget and configure credentials locally. Never mistake the
public metadata export for a recoverable private model-response cache.

## Sandbox limitation

Docker is used for normal generated solutions. The known adversarial RPC integrity
limitation remains: this benchmark does **not** establish security against malicious
generated code. Optional Docker tests can be run using the commands in
[validation documentation](docs/validation.md); adversarial tests are not represented
as passed when skipped in an offline-only run.
