from __future__ import annotations

import argparse
import os
import uuid
import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(env_path: Path) -> None:
        if not env_path.exists():
            return
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())

from coordinators import COORDINATORS, ExperimentResult
from llm_client import BaseLLMClient, GigaChatClient, MockLLMClient
from metrics import append_raw_result, initialize_raw_results, write_summary_from_raw
from sandbox_runner import run_code_in_sandbox
from tasks import get_tasks
from utils import ensure_directories, make_run_id


DEFAULT_ARCHITECTURES = [
    "single_agent",
    "chain",
    "centralized",
    "feedback_graph",
    "fully_connected",
    "parallel_consensus",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Experiment with coordination graphs in multi-agent LLM systems."
    )
    parser.add_argument(
        "--architectures",
        nargs="+",
        default=DEFAULT_ARCHITECTURES,
        choices=sorted(COORDINATORS.keys()),
        help="Architectures to run.",
    )
    parser.add_argument("--max-iterations", type=int, default=3, help="Max feedback iterations.")
    parser.add_argument("--repeats", type=int, default=1, help="Repeats for each task and architecture.")
    parser.add_argument("--model", type=str, default=None, help="GigaChat model name.")
    parser.add_argument("--list-models", action="store_true", help="List available GigaChat models and exit.")
    parser.add_argument("--output-dir", type=str, default="runs", help="Parent directory for experiment runs.")
    parser.add_argument("--tasks-limit", type=int, default=None, help="Limit number of tasks.")
    parser.add_argument("--mock", action="store_true", help="Force MockLLMClient.")
    args = parser.parse_args()
    if args.max_iterations <= 0 or args.repeats <= 0 or (args.tasks_limit is not None and args.tasks_limit <= 0):
        parser.error("--max-iterations, --repeats and --tasks-limit must be positive")
    return args


def create_llm_client(args: argparse.Namespace) -> BaseLLMClient:
    if args.mock:
        return MockLLMClient()

    gigachat_client = GigaChatClient.from_env(model=args.model)
    if gigachat_client is None:
        raise RuntimeError("GIGACHAT_AUTH_KEY is not set; configure it or explicitly use --mock.")
    return gigachat_client


def main() -> None:
    project_dir = Path(__file__).resolve().parent
    load_dotenv(project_dir / ".env")
    args = parse_args()
    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = project_dir / output_dir
    if args.list_models:
        llm_client = create_llm_client(args)
        if isinstance(llm_client, GigaChatClient):
            print("Available GigaChat models:")
            for model_name in llm_client.get_available_models():
                print(f"- {model_name}")
        else:
            print("GigaChat key is not configured; available client is model=mock.")
        return

    preflight = run_code_in_sandbox("def _preflight(): return 1", "assert _preflight() == 1", timeout=10)
    if not preflight.success:
        raise RuntimeError(f"Docker sandbox preflight failed ({preflight.status}); start Docker and install the pinned image before running the benchmark.")
    llm_client = create_llm_client(args)

    experiment_id = uuid.uuid4().hex
    output_dir = output_dir / experiment_id
    output_dir.mkdir(parents=True, exist_ok=False)
    solutions_dir = output_dir / "generated_solutions"
    ensure_directories(output_dir, solutions_dir)

    tasks = get_tasks()
    if args.tasks_limit is not None:
        tasks = tasks[: args.tasks_limit]

    try:
        commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=project_dir,
                                text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                timeout=3, check=True).stdout.strip()
        dirty = bool(subprocess.run(["git", "status", "--porcelain", "--untracked-files=no"],
                                    cwd=project_dir, text=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.DEVNULL, timeout=3, check=True).stdout.strip())
    except (OSError, subprocess.SubprocessError):
        commit = None
        dirty = None
    revisions = {name: hashlib.sha256((project_dir / name).read_bytes()).hexdigest()
                 for name in ("tasks.py", "prompts.py", "sandbox_runner.py", "sandbox_worker.py", "sandbox_evaluator.py")}
    try:
        gigachat_version = metadata.version("gigachat")
    except metadata.PackageNotFoundError:
        gigachat_version = None
    manifest = {"experiment_id": experiment_id, "protocol_version": "v2", "model": llm_client.model_name,
                "mock": args.mock, "started_utc": datetime.now(timezone.utc).isoformat(),
                "architectures": args.architectures, "tasks": [task.task_id for task in tasks],
                "repeats": args.repeats, "max_iterations": args.max_iterations,
                "python": platform.python_version(), "platform": platform.system(),
                "gigachat_version": gigachat_version, "git_commit": commit,
                "git_tracked_files_dirty": dirty, "model_parameters": "provider defaults; not exposed",
                "revisions_sha256": revisions, "seed_control": "not supported by this client",
                "sandbox_image": __import__("sandbox_runner").IMAGE,
                "sandbox_executor": "two-container-rpc-v1",
                "sandbox_limits": {"timeout_seconds": 5, "containers": 2, "memory_per_container": "256m", "cpus_per_container": 1, "pids_per_container": 64}}
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    raw_path = output_dir / "raw_results.csv"
    summary_path = output_dir / "summary_results.csv"
    initialize_raw_results(raw_path)
    for architecture in args.architectures:
        coordinator_cls = COORDINATORS[architecture]
        coordinator = coordinator_cls(
            llm_client=llm_client,
            solutions_dir=solutions_dir,
            max_iterations=args.max_iterations,
        )
        for repeat in range(1, args.repeats + 1):
            for task in tasks:
                run_id = make_run_id()
                print(f"Running {architecture} on {task.task_id} ({task.name}) with model={llm_client.model_name}")
                result = coordinator.run(task, run_id)
                result.experiment_id = experiment_id
                result.repeat_index = repeat
                append_raw_result(result, raw_path)
                write_summary_from_raw(raw_path, summary_path, replace=True)
                print(f"  {result.status}: iterations={result.iterations}, llm_calls={result.llm_calls}")

    print(f"Raw results: {raw_path}")
    print(f"Summary results: {summary_path}")


if __name__ == "__main__":
    main()
