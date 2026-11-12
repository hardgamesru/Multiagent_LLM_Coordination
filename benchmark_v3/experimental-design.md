# Preregistered design proposal (preparation; no API measurements)

Research question: Does coordination improve programming-task correctness as
predefined difficulty increases, and does this relationship differ by model?

H1: the advantage of feedback/consensus over a single agent increases with
difficulty. H2: the coordination advantage is smaller for Ultra than Lite.
Neither hypothesis is assumed true. Primary outcome is held-out correctness;
secondary outcomes are input/output/total tokens, calls, latency, and failure types.

Models: requested `GigaChat-2`, `GigaChat-3-Ultra`. Architectures: `single_agent`,
`feedback_graph`, `parallel_consensus`. Retain all other architecture source code.
Candidate design: 20 tasks × 2 models × 3 architectures × 3 repeats = 360
evaluations. Maximum feedback iterations: 3. Keep prompt policy and provider
generation defaults identical between models. Use `https://api.giga.chat/v1/`
for both if access is confirmed; do not mix endpoints without documenting a deviation.

Pilot, only after preparation review: one preselected representative of each
difficulty, v3_03 range_sums, v3_10 lru_trace, v3_17 transaction_trace, crossed with
both models and all three architectures, one repeat = 18 evaluations. Selection
precedes model outcomes. Pilot results remain a separate calibration dataset;
they do not substitute for any main-run cell. No individual retries for scores.
Freeze task/test hashes before the pilot. A task defect discovered later requires
a new suite revision and explicit disclosure, never silent retrospective tuning.

Estimate per-evaluation cost for each model/architecture/difficulty pilot cell.
Weight by the suite's 4/8/8 difficulty counts. For r repeats, let E(r) be the sum
of these weighted costs over both models and three architectures, times r.
Use at least a 50% uncertainty margin: pilot_actual + 1.5 E(r) <= 850,000.
Choose the largest common r in {3,2,1} meeting this condition and a conservative
maximum-call reserve. If none fits, stop and review design rather than selecting
tasks or architectures by performance. One pilot observation per cell gives a weak
cost estimate; the margin is a policy assumption, not a statistical confidence bound.
Report this limitation and actual pilot usage for approval before the main run.

All new pilot/main API usage counts toward a shared 1,000,000-token ceiling;
target <=850,000. Before paid execution, implement a durable ledger updated after
every response, with requested AND provider-returned model IDs, endpoint, protocol
version, exact source/task hashes, request counts, usage completeness, and run IDs.
Pre-authorize each request against a conservative input/output/in-flight reserve;
use serial calls initially. Provider output may be unbounded under defaults: if a
defensible maximum reservation cannot be established, stop and seek an explicit
generation-limit/design decision before requests, rather than pretending a
post-response counter guarantees the hard ceiling. Unknown usage must block
further requests and must never be treated as zero. Record provider errors with
unknown billing separately. A ledger reservation is not itself actual usage.

Save every completed evaluation immediately. Preserve partial runs and their
usage; exclude incomplete/unbalanced cells from paired model claims. Report the
maximal common completed set across both models/architectures, plus all raw data.
Do not replace incomplete rows or silently launch additional paid experiments.

Analysis after an approved main run: report success proportions with descriptive
uncertainty across balanced repetitions; calls, token totals, latency and failure
categories by difficulty/model/architecture. Token-per-success includes all failed
attempts in the numerator. Compare coordination with the single-agent baseline
within model/difficulty, including ceiling effects. Tasks reused across cells and
repetitions are not independent observations. Avoid causal conclusions or treating
360 evaluations as 360 independent tasks. Figures should be reproducible SVGs
from saved CSV via an offline script, with source revision and balanced denominator
in captions. No figures of nonexistent v3 performance should be generated.
