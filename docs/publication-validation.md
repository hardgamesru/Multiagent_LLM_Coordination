# Publication validation record

Publication branch: research-v3. Base: sandbox-integrity commit
5e469e9cfcb185ae9650136dc5c539a9dad50256 plus the exact locally measured source
bytes pinned in provenance/publication-freeze.json.

- Offline v3, runner/ledger and publication tests passed (25 tests).
- Full existing backend suite with RUN_DOCKER_TESTS=1 passed (39 tests).
- An earlier Docker attempt failed because the Linux engine was stopped. Its
  infrastructure-error outcomes, including incidental adversarial non-pass checks,
  were not counted as successful validation. Docker was restored, the exact pinned
  image digest checked, and the entire suite rerun without test or backend edits.
- All 240 complete main records and 965 model calls reconcile with the public
  request audit; combined main input including cache plus output is 548,141 tokens.
- All imported CSV and generated solutions retain original bytes; SHA-256 lineage
  records distinguish path-redacted metadata from original private artifacts.
- Inherited baseline files, including historical result CSV and generated solutions,
  are byte-identical to their original Git blobs.
- CSV-only reproduction regenerated the English report and SVG figures and verified
  existing research tables numerically without overwriting their original bytes.
- Privacy scan found no configured API credential, known token pattern, private
  SQLite database, archive, oversized artifact or newly introduced personal path.
  One pre-existing legacy raw CSV path exception is explicitly documented and
  unchanged from the already-published baseline; it is not copied into documentation.
- Private raw API responses, headers and full ledgers are retained in the documented
  local archive only. Unknown usage remains unknown with a full 69,632-token reserve.
- No model generation calls were made during packaging or validation.

The publication repair additionally verifies that report regeneration preserves
all captured CSV, JSON, Markdown, SVG and source evidence, emits canonical UTF-8/LF
English report text, and does not replace captured analysis scripts. The existing
audit JSON is compared semantically and kept byte-identical across platforms.
New SVG renderings go to `reproduced/benchmark-v3/figures/` by default instead of
overwriting captured figures. Font/rendering differences across operating systems
can change SVG bytes without changing the measured values used to plot them.

The known adversarial RPC integrity limitation remains; these test results do not
establish security against deliberately malicious generated code.
