from __future__ import annotations

import csv
from dataclasses import asdict
from pathlib import Path

from coordinators import ExperimentResult


RAW_COLUMNS = [
    "run_id",
    "timestamp",
    "task_id",
    "task_name",
    "architecture",
    "model",
    "success",
    "iterations",
    "messages",
    "estimated_cost",
    "elapsed_seconds",
    "final_code_path",
    "error_message",
]

SUMMARY_COLUMNS = [
    "architecture",
    "model",
    "tasks_total",
    "tasks_success",
    "success_rate",
    "avg_iterations",
    "avg_messages",
    "avg_estimated_cost",
    "avg_elapsed_seconds",
]


def write_raw_results(results: list[ExperimentResult], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=RAW_COLUMNS)
        writer.writeheader()
        for result in results:
            row = asdict(result)
            writer.writerow({column: row.get(column, "") for column in RAW_COLUMNS})


def write_summary_results(results: list[ExperimentResult], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    grouped: dict[tuple[str, str], list[ExperimentResult]] = {}
    for result in results:
        grouped.setdefault((result.architecture, result.model), []).append(result)

    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=SUMMARY_COLUMNS)
        writer.writeheader()
        for (architecture, model), group in sorted(grouped.items()):
            tasks_total = len(group)
            tasks_success = sum(1 for result in group if result.success)
            writer.writerow(
                {
                    "architecture": architecture,
                    "model": model,
                    "tasks_total": tasks_total,
                    "tasks_success": tasks_success,
                    "success_rate": tasks_success / tasks_total if tasks_total else 0,
                    "avg_iterations": _average(result.iterations for result in group),
                    "avg_messages": _average(result.messages for result in group),
                    "avg_estimated_cost": _average(result.estimated_cost for result in group),
                    "avg_elapsed_seconds": _average(result.elapsed_seconds for result in group),
                }
            )


def _average(values: object) -> float:
    items = list(values)
    if not items:
        return 0.0
    return sum(items) / len(items)
