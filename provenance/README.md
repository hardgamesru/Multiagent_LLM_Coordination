# Provenance and publication transformations

The implementation baseline is sandbox-integrity commit
`5e469e9cfcb185ae9650136dc5c539a9dad50256` with the locally measured dirty changes.
`publication-freeze.json` pins every measured v2 Python file and immutable v3 task
source. `preparation-manifest.json` is the original preparation record: its hashes
refer to the private original preparation snapshot, not modified publication docs.

Raw/summary CSV and generated solutions are preserved byte-for-byte. Public metadata
and source-snapshot copies may redact personal filesystem paths; they are explicitly
derived, not presented as original bytes. `artifact-lineage.json` records original
and public SHA-256 and the transformation for each imported artifact. Hash references
inside experiment CSV/manifests retain their original meaning and are not rewritten
to pretend the publication adaptation was the measured implementation.

The portable adapter, explicit paid opt-in, and CSV-only analysis are publication
adaptations. They do not change frozen tasks, expected outputs, coordination prompts
or the measured backend. Read-only measurement source snapshots are distinct from
the portable runtime. Source-snapshot originals with personal paths remain private;
their original SHA-256 remains public.

The full original data, private SQLite ledgers/raw responses, original reports and
source snapshots are preserved in a local ZIP outside the publication checkout.
`local-archive.json` identifies that archive by filename, size and SHA-256, without
publishing its personal location. No archive or SQLite file is committed.

The public request audit exports usage, latency, model IDs, request keys and reserves
only. It excludes response text, headers, access tokens, API keys and user paths.
The one unknown request remains unknown; the full reserve is kept in budget totals.

Line endings in measured source are intentionally preserved to match measurement
SHA-256, even where this makes the Git diff noisier. No coordinator refactor is
introduced. `inherited-baseline-files.json` pins inherited Git bytes, including
legacy results and generated solutions, so pre-existing evidence cannot silently
change. The inherited legacy raw CSV contains pre-existing filesystem strings;
it is retained byte-identically as data, not copied into new documentation. This
narrow inherited exception is explicitly reported by the privacy scanner.
