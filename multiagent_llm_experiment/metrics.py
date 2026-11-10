"""CSV recording and deterministic summaries for protocol v2."""
import csv
import os
import statistics
import tempfile
from dataclasses import asdict
from pathlib import Path

RAW_COLUMNS = ["experiment_id", "run_id", "repeat_index", "timestamp", "task_id", "task_name",
               "architecture", "model", "protocol_version", "status", "success", "iterations",
               "llm_calls", "usage_available", "input_tokens", "output_tokens", "total_tokens",
               "generation_seconds", "test_seconds", "elapsed_seconds", "development_test_calls",
               "evaluation_test_calls", "final_code_path", "error_message"]
SUMMARY_COLUMNS = ["architecture", "model", "runs", "eligible", "passed", "success_rate",
                   "repeat_success_rate_stddev", "infrastructure_failures", "infrastructure_failure_rate",
                   "generation_or_provider_failures", "avg_llm_calls"]
ELIGIBLE = {"passed", "failed_tests", "invalid_code", "candidate_timeout"}
INFRA = {"sandbox_timeout", "sandbox_error", "sandbox_unavailable"}


def initialize_raw_results(output_path: Path) -> None:
    with output_path.open("x", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=RAW_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        stream.flush()
        os.fsync(stream.fileno())


def append_raw_result(result, output_path: Path) -> None:
    row = asdict(result)
    if not row["usage_available"]:
        for field in ("input_tokens", "output_tokens", "total_tokens"):
            row[field] = ""
    with output_path.open("a", newline="", encoding="utf-8") as stream:
        csv.DictWriter(stream, fieldnames=RAW_COLUMNS, extrasaction="ignore").writerow(row)
        stream.flush()
        os.fsync(stream.fileno())


def write_raw_results(results, output_path: Path) -> None:
    initialize_raw_results(output_path)
    for result in results:
        append_raw_result(result, output_path)


def summarize(rows):
    grouped = {}
    for row in rows:
        grouped.setdefault((row["architecture"], row["model"]), []).append(row)
    output = []
    for (architecture, model), group in sorted(grouped.items()):
        eligible = sum(row["status"] in ELIGIBLE for row in group)
        passed = sum(row["status"] == "passed" for row in group)
        infra = sum(row["status"] in INFRA for row in group)
        repeats = sorted({str(row["repeat_index"]) for row in group})
        rates = []
        for repeat in repeats:
            subset = [row for row in group if str(row["repeat_index"]) == repeat and row["status"] in ELIGIBLE]
            if subset:
                rates.append(sum(row["status"] == "passed" for row in subset) / len(subset))
        output.append({"architecture": architecture, "model": model, "runs": len(group),
                       "eligible": eligible, "passed": passed,
                       "success_rate": passed / eligible if eligible else "",
                       "repeat_success_rate_stddev": statistics.stdev(rates) if len(rates) > 1 else "",
                       "infrastructure_failures": infra,
                       "infrastructure_failure_rate": infra / len(group),
                       "generation_or_provider_failures": sum(row["status"] in {"provider_error", "generation_error"} for row in group),
                       "avg_llm_calls": sum(int(row["llm_calls"]) for row in group) / len(group)})
    return output


def write_summary_from_raw(raw_path: Path, output_path: Path, *, replace: bool = False) -> None:
    with raw_path.open(newline="", encoding="utf-8") as stream:
        rows = summarize(list(csv.DictReader(stream)))
    if not replace:
        with output_path.open("x", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=SUMMARY_COLUMNS)
            writer.writeheader()
            writer.writerows(rows)
        return
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", newline="", encoding="utf-8", dir=output_path.parent,
                                         prefix=".summary-", suffix=".tmp", delete=False) as stream:
            temporary = Path(stream.name)
            writer = csv.DictWriter(stream, fieldnames=SUMMARY_COLUMNS)
            writer.writeheader()
            writer.writerows(rows)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, output_path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def write_summary_results(results, output_path: Path) -> None:
    # Kept for callers that already have rows in memory.
    rows = summarize([asdict(result) for result in results])
    with output_path.open("x", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=SUMMARY_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
