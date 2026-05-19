from __future__ import annotations

import argparse
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv() -> None:
        env_path = Path(".env")
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
from metrics import write_raw_results, write_summary_results
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
    parser.add_argument("--model", type=str, default=None, help="GigaChat model name.")
    parser.add_argument("--list-models", action="store_true", help="List available GigaChat models and exit.")
    parser.add_argument("--output-dir", type=str, default="results", help="Directory for CSV files.")
    parser.add_argument("--tasks-limit", type=int, default=None, help="Limit number of tasks.")
    parser.add_argument("--mock", action="store_true", help="Force MockLLMClient.")
    return parser.parse_args()


def create_llm_client(args: argparse.Namespace) -> BaseLLMClient:
    if args.mock:
        return MockLLMClient()

    gigachat_client = GigaChatClient.from_env(model=args.model)
    if gigachat_client is None:
        print("GIGACHAT_AUTH_KEY is not set. Using MockLLMClient with model=mock.")
        return MockLLMClient()
    return gigachat_client


def main() -> None:
    load_dotenv()
    args = parse_args()
    project_dir = Path(__file__).resolve().parent
    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = project_dir / output_dir
    solutions_dir = project_dir / "generated_solutions"
    ensure_directories(output_dir, solutions_dir)

    llm_client = create_llm_client(args)
    if args.list_models:
        if isinstance(llm_client, GigaChatClient):
            print("Available GigaChat models:")
            for model_name in llm_client.get_available_models():
                print(f"- {model_name}")
        else:
            print("GigaChat key is not configured; available client is model=mock.")
        return

    tasks = get_tasks()
    if args.tasks_limit is not None:
        tasks = tasks[: args.tasks_limit]

    results: list[ExperimentResult] = []
    for architecture in args.architectures:
        coordinator_cls = COORDINATORS[architecture]
        coordinator = coordinator_cls(
            llm_client=llm_client,
            solutions_dir=solutions_dir,
            max_iterations=args.max_iterations,
        )
        for task in tasks:
            run_id = make_run_id()
            print(f"Running {architecture} on {task.task_id} ({task.name}) with model={llm_client.model_name}")
            result = coordinator.run(task, run_id)
            results.append(result)
            status = "OK" if result.success else "FAIL"
            print(f"  {status}: iterations={result.iterations}, messages={result.messages}")

    raw_path = output_dir / "raw_results.csv"
    summary_path = output_dir / "summary_results.csv"
    write_raw_results(results, raw_path)
    write_summary_results(results, summary_path)
    print(f"Raw results: {raw_path}")
    print(f"Summary results: {summary_path}")


if __name__ == "__main__":
    main()
