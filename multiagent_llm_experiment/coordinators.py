from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path

from agents import AnalystAgent, DeveloperAgent, ManagerAgent, ReviewerAgent, TesterAgent
from llm_client import BaseLLMClient
from sandbox_runner import run_code_in_sandbox
from tasks import Task
from utils import build_task_prompt, current_timestamp, extract_python_code, safe_filename_part


@dataclass
class ExperimentResult:
    run_id: str
    timestamp: str
    task_id: str
    task_name: str
    architecture: str
    model: str
    success: bool
    iterations: int
    messages: int
    estimated_cost: float
    input_tokens: int
    output_tokens: int
    total_tokens: int
    elapsed_seconds: float
    final_code_path: str
    error_message: str


class BaseCoordinator:
    architecture_name = "base"

    def __init__(
        self,
        llm_client: BaseLLMClient,
        solutions_dir: Path,
        max_iterations: int = 3,
    ) -> None:
        self.llm_client = llm_client
        self.solutions_dir = solutions_dir
        self.max_iterations = max_iterations

    def run(self, task: Task, run_id: str) -> ExperimentResult:
        raise NotImplementedError

    def _save_code(self, run_id: str, task: Task, iteration: int, code: str) -> Path:
        self.solutions_dir.mkdir(parents=True, exist_ok=True)
        filename = (
            f"{safe_filename_part(run_id)}_"
            f"{safe_filename_part(self.architecture_name)}_"
            f"{safe_filename_part(task.task_id)}_iter{iteration}.py"
        )
        path = self.solutions_dir / filename
        path.write_text(code.strip() + "\n", encoding="utf-8")
        return path

    def _result(
        self,
        *,
        run_id: str,
        task: Task,
        success: bool,
        iterations: int,
        messages: int,
        elapsed_seconds: float,
        final_code_path: Path | None,
        error_message: str,
        usage_start: tuple[int, int, int] | None = None,
    ) -> ExperimentResult:
        if usage_start is None:
            usage_start = getattr(self, "_usage_start", None)
        input_tokens, output_tokens, total_tokens = (0, 0, 0)
        if usage_start is not None:
            input_tokens, output_tokens, total_tokens = self.llm_client.get_usage_delta(usage_start)
        return ExperimentResult(
            run_id=run_id,
            timestamp=current_timestamp(),
            task_id=task.task_id,
            task_name=task.name,
            architecture=self.architecture_name,
            model=self.llm_client.model_name,
            success=success,
            iterations=iterations,
            messages=messages,
            estimated_cost=float(messages),
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            elapsed_seconds=round(elapsed_seconds, 4),
            final_code_path=str(final_code_path) if final_code_path else "",
            error_message=error_message,
        )


class SingleAgentCoordinator(BaseCoordinator):
    architecture_name = "single_agent"

    def run(self, task: Task, run_id: str) -> ExperimentResult:
        start = time.perf_counter()
        self._usage_start = self.llm_client.get_usage_totals()
        messages = 0
        final_path: Path | None = None
        try:
            developer = DeveloperAgent(self.llm_client)
            response = developer.run(
                build_task_prompt(task.description, task.function_name, task.visible_examples)
            )
            messages += response.messages_used
            code = extract_python_code(response.content)
            final_path = self._save_code(run_id, task, 1, code)
            sandbox = run_code_in_sandbox(code, task.hidden_tests)
            return self._result(
                run_id=run_id,
                task=task,
                success=sandbox.success,
                iterations=1,
                messages=messages,
                elapsed_seconds=time.perf_counter() - start,
                final_code_path=final_path,
                error_message=sandbox.error_message,
            )
        except Exception as exc:
            return self._result(
                run_id=run_id,
                task=task,
                success=False,
                iterations=1,
                messages=messages,
                elapsed_seconds=time.perf_counter() - start,
                final_code_path=final_path,
                error_message=str(exc),
            )


class ChainCoordinator(BaseCoordinator):
    architecture_name = "chain"

    def run(self, task: Task, run_id: str) -> ExperimentResult:
        start = time.perf_counter()
        self._usage_start = self.llm_client.get_usage_totals()
        messages = 0
        final_path: Path | None = None
        try:
            analyst = AnalystAgent(self.llm_client)
            developer = DeveloperAgent(self.llm_client)
            tester = TesterAgent(self.llm_client)
            reviewer = ReviewerAgent(self.llm_client)

            task_prompt = build_task_prompt(task.description, task.function_name, task.visible_examples)
            analysis = analyst.run(task_prompt)
            messages += analysis.messages_used

            dev_input = f"{task_prompt}\n\nАнализ:\n{analysis.content}"
            developer_response = developer.run(dev_input)
            messages += developer_response.messages_used
            developer_code = extract_python_code(developer_response.content)

            tester_input = f"{task_prompt}\n\nКод:\n{developer_code}"
            tester_response = tester.run(tester_input)
            messages += tester_response.messages_used

            reviewer_input = (
                f"{task_prompt}\n\nКод:\n{developer_code}\n\n"
                f"Ответ тестировщика:\n{tester_response.content}"
            )
            reviewer_response = reviewer.run(reviewer_input)
            messages += reviewer_response.messages_used
            reviewed_code = extract_python_code(reviewer_response.content)
            final_code = reviewed_code if f"def {task.function_name}" in reviewed_code else developer_code

            final_path = self._save_code(run_id, task, 1, final_code)
            sandbox = run_code_in_sandbox(final_code, task.hidden_tests)
            return self._result(
                run_id=run_id,
                task=task,
                success=sandbox.success,
                iterations=1,
                messages=messages,
                elapsed_seconds=time.perf_counter() - start,
                final_code_path=final_path,
                error_message=sandbox.error_message,
            )
        except Exception as exc:
            return self._result(
                run_id=run_id,
                task=task,
                success=False,
                iterations=1,
                messages=messages,
                elapsed_seconds=time.perf_counter() - start,
                final_code_path=final_path,
                error_message=str(exc),
            )


class CentralizedCoordinator(BaseCoordinator):
    architecture_name = "centralized"

    def run(self, task: Task, run_id: str) -> ExperimentResult:
        start = time.perf_counter()
        self._usage_start = self.llm_client.get_usage_totals()
        messages = 0
        final_path: Path | None = None
        try:
            manager = ManagerAgent(self.llm_client)
            analyst = AnalystAgent(self.llm_client)
            developer = DeveloperAgent(self.llm_client)
            tester = TesterAgent(self.llm_client)
            reviewer = ReviewerAgent(self.llm_client)

            task_prompt = build_task_prompt(task.description, task.function_name, task.visible_examples)
            manager_plan = manager.run(f"Подготовь краткое распределение работы.\n\n{task_prompt}")
            messages += manager_plan.messages_used

            analysis = analyst.run(f"{task_prompt}\n\nИнструкция менеджера:\n{manager_plan.content}")
            messages += analysis.messages_used

            developer_response = developer.run(
                f"{task_prompt}\n\nАнализ:\n{analysis.content}\n\nИнструкция менеджера:\n{manager_plan.content}"
            )
            messages += developer_response.messages_used
            developer_code = extract_python_code(developer_response.content)

            tester_response = tester.run(f"{task_prompt}\n\nКод:\n{developer_code}")
            messages += tester_response.messages_used

            reviewer_response = reviewer.run(
                f"{task_prompt}\n\nКод:\n{developer_code}\n\nОтвет тестировщика:\n{tester_response.content}"
            )
            messages += reviewer_response.messages_used

            manager_final = manager.run(
                f"{task_prompt}\n\nКод программиста:\n{developer_code}\n\n"
                f"Ответ тестировщика:\n{tester_response.content}\n\n"
                f"Ответ ревьюера:\n{reviewer_response.content}\n\n"
                "Верни итоговый код функции."
            )
            messages += manager_final.messages_used
            manager_code = extract_python_code(manager_final.content)
            final_code = manager_code if f"def {task.function_name}" in manager_code else developer_code

            final_path = self._save_code(run_id, task, 1, final_code)
            sandbox = run_code_in_sandbox(final_code, task.hidden_tests)
            return self._result(
                run_id=run_id,
                task=task,
                success=sandbox.success,
                iterations=1,
                messages=messages,
                elapsed_seconds=time.perf_counter() - start,
                final_code_path=final_path,
                error_message=sandbox.error_message,
            )
        except Exception as exc:
            return self._result(
                run_id=run_id,
                task=task,
                success=False,
                iterations=1,
                messages=messages,
                elapsed_seconds=time.perf_counter() - start,
                final_code_path=final_path,
                error_message=str(exc),
            )


class FeedbackGraphCoordinator(BaseCoordinator):
    architecture_name = "feedback_graph"

    def run(self, task: Task, run_id: str) -> ExperimentResult:
        start = time.perf_counter()
        self._usage_start = self.llm_client.get_usage_totals()
        messages = 0
        final_path: Path | None = None
        last_error = ""
        try:
            analyst = AnalystAgent(self.llm_client)
            developer = DeveloperAgent(self.llm_client)
            tester = TesterAgent(self.llm_client)
            reviewer = ReviewerAgent(self.llm_client)

            task_prompt = build_task_prompt(task.description, task.function_name, task.visible_examples)
            analysis = analyst.run(task_prompt)
            messages += analysis.messages_used
            feedback = ""

            for iteration in range(1, self.max_iterations + 1):
                developer_input = f"{task_prompt}\n\nАнализ:\n{analysis.content}"
                if feedback:
                    developer_input += f"\n\nИсправь код с учетом ошибки:\n{feedback}"
                developer_response = developer.run(developer_input)
                messages += developer_response.messages_used
                code = extract_python_code(developer_response.content)
                final_path = self._save_code(run_id, task, iteration, code)

                sandbox = run_code_in_sandbox(code, task.hidden_tests)
                tester_response = tester.run(
                    f"{task_prompt}\n\nКод:\n{code}\n\nРезультат запуска тестов:\n"
                    f"success={sandbox.success}\nerror={sandbox.error_message}"
                )
                messages += tester_response.messages_used

                if not sandbox.success:
                    last_error = sandbox.error_message
                    feedback = f"Тесты не пройдены: {sandbox.error_message}"
                    continue

                reviewer_response = reviewer.run(
                    f"{task_prompt}\n\nКод:\n{code}\n\nОтвет тестировщика:\n{tester_response.content}"
                )
                messages += reviewer_response.messages_used
                reviewed_code = extract_python_code(reviewer_response.content)
                final_code = reviewed_code if f"def {task.function_name}" in reviewed_code else code
                final_path = self._save_code(run_id, task, iteration, final_code)
                final_sandbox = run_code_in_sandbox(final_code, task.hidden_tests)
                if final_sandbox.success:
                    return self._result(
                        run_id=run_id,
                        task=task,
                        success=True,
                        iterations=iteration,
                        messages=messages,
                        elapsed_seconds=time.perf_counter() - start,
                        final_code_path=final_path,
                        error_message="",
                    )

                last_error = final_sandbox.error_message
                feedback = f"Ревью или итоговые тесты выявили ошибку: {last_error}"

            return self._result(
                run_id=run_id,
                task=task,
                success=False,
                iterations=self.max_iterations,
                messages=messages,
                elapsed_seconds=time.perf_counter() - start,
                final_code_path=final_path,
                error_message=last_error or "Max iterations reached",
            )
        except Exception as exc:
            return self._result(
                run_id=run_id,
                task=task,
                success=False,
                iterations=self.max_iterations,
                messages=messages,
                elapsed_seconds=time.perf_counter() - start,
                final_code_path=final_path,
                error_message=str(exc),
            )


class FullyConnectedCoordinator(BaseCoordinator):
    architecture_name = "fully_connected"

    def run(self, task: Task, run_id: str) -> ExperimentResult:
        start = time.perf_counter()
        self._usage_start = self.llm_client.get_usage_totals()
        messages = 0
        final_path: Path | None = None
        try:
            analyst = AnalystAgent(self.llm_client)
            developer = DeveloperAgent(self.llm_client)
            tester = TesterAgent(self.llm_client)
            reviewer = ReviewerAgent(self.llm_client)

            task_prompt = build_task_prompt(task.description, task.function_name, task.visible_examples)
            analysis = analyst.run(task_prompt)
            messages += analysis.messages_used

            initial_response = developer.run(
                f"{task_prompt}\n\nRequirements from analyst:\n{analysis.content}"
            )
            messages += initial_response.messages_used
            initial_code = extract_python_code(initial_response.content)

            tester_feedback = tester.run(
                f"{task_prompt}\n\nAnalyst context:\n{analysis.content}\n\nCode:\n{initial_code}"
            )
            messages += tester_feedback.messages_used

            reviewer_feedback = reviewer.run(
                f"{task_prompt}\n\nAnalyst context:\n{analysis.content}\n\n"
                f"Tester feedback:\n{tester_feedback.content}\n\nCode:\n{initial_code}"
            )
            messages += reviewer_feedback.messages_used

            final_response = developer.run(
                f"{task_prompt}\n\nAnalyst context:\n{analysis.content}\n\n"
                f"Tester feedback:\n{tester_feedback.content}\n\n"
                f"Reviewer feedback:\n{reviewer_feedback.content}\n\n"
                f"Initial code:\n{initial_code}\n\n"
                "Return the final function code only."
            )
            messages += final_response.messages_used
            final_code = extract_python_code(final_response.content)
            if f"def {task.function_name}" not in final_code:
                final_code = initial_code

            final_path = self._save_code(run_id, task, 1, final_code)
            sandbox = run_code_in_sandbox(final_code, task.hidden_tests)
            return self._result(
                run_id=run_id,
                task=task,
                success=sandbox.success,
                iterations=1,
                messages=messages,
                elapsed_seconds=time.perf_counter() - start,
                final_code_path=final_path,
                error_message=sandbox.error_message,
            )
        except Exception as exc:
            return self._result(
                run_id=run_id,
                task=task,
                success=False,
                iterations=1,
                messages=messages,
                elapsed_seconds=time.perf_counter() - start,
                final_code_path=final_path,
                error_message=str(exc),
            )


class ParallelConsensusCoordinator(BaseCoordinator):
    architecture_name = "parallel_consensus"

    def run(self, task: Task, run_id: str) -> ExperimentResult:
        start = time.perf_counter()
        self._usage_start = self.llm_client.get_usage_totals()
        messages = 0
        final_path: Path | None = None
        try:
            analyst = AnalystAgent(self.llm_client)
            developers = [
                DeveloperAgent(self.llm_client, name="developer_1"),
                DeveloperAgent(self.llm_client, name="developer_2"),
                DeveloperAgent(self.llm_client, name="developer_3"),
            ]
            tester = TesterAgent(self.llm_client)
            reviewer = ReviewerAgent(self.llm_client)

            task_prompt = build_task_prompt(task.description, task.function_name, task.visible_examples)
            analysis = analyst.run(task_prompt)
            messages += analysis.messages_used

            candidates: list[dict[str, object]] = []
            for index, developer in enumerate(developers, start=1):
                response = developer.run(
                    f"{task_prompt}\n\nTechnical description:\n{analysis.content}\n\n"
                    f"Generate independent solution variant {index}."
                )
                messages += response.messages_used
                code = extract_python_code(response.content)
                path = self._save_code(run_id, task, index, code)
                sandbox = run_code_in_sandbox(code, task.hidden_tests)
                candidates.append(
                    {
                        "index": index,
                        "code": code,
                        "path": path,
                        "success": sandbox.success,
                        "error": sandbox.error_message,
                    }
                )

            candidate_report = self._format_candidate_report(candidates)
            tester_response = tester.run(
                f"{task_prompt}\n\nCandidate test results:\n{candidate_report}\n\n"
                "Return OK if at least one candidate is acceptable, otherwise list errors."
            )
            messages += tester_response.messages_used

            passing = [candidate for candidate in candidates if bool(candidate["success"])]
            if passing:
                best_candidate = min(passing, key=lambda candidate: len(str(candidate["code"])))
                reviewer_response = reviewer.run(
                    f"{task_prompt}\n\nTester feedback:\n{tester_response.content}\n\n"
                    f"Candidate test results:\n{candidate_report}\n\n"
                    f"Selected shortest passing candidate #{best_candidate['index']}:\n"
                    f"{best_candidate['code']}\n\nReturn the final function code only."
                )
                messages += reviewer_response.messages_used
                reviewed_code = extract_python_code(reviewer_response.content)
                final_code = (
                    reviewed_code
                    if f"def {task.function_name}" in reviewed_code
                    else str(best_candidate["code"])
                )
                final_path = self._save_code(run_id, task, 4, final_code)
                final_sandbox = run_code_in_sandbox(final_code, task.hidden_tests)
                if final_sandbox.success:
                    return self._result(
                        run_id=run_id,
                        task=task,
                        success=True,
                        iterations=1,
                        messages=messages,
                        elapsed_seconds=time.perf_counter() - start,
                        final_code_path=final_path,
                        error_message="",
                    )
                return self._result(
                    run_id=run_id,
                    task=task,
                    success=False,
                    iterations=1,
                    messages=messages,
                    elapsed_seconds=time.perf_counter() - start,
                    final_code_path=final_path,
                    error_message=final_sandbox.error_message,
                )

            reviewer_response = reviewer.run(
                f"{task_prompt}\n\nTester feedback:\n{tester_response.content}\n\n"
                f"Candidate test results:\n{candidate_report}\n\n"
                "No candidate passed the sandbox tests. Return brief review notes."
            )
            messages += reviewer_response.messages_used
            first_candidate = candidates[0] if candidates else None
            final_path = first_candidate["path"] if first_candidate else None
            return self._result(
                run_id=run_id,
                task=task,
                success=False,
                iterations=1,
                messages=messages,
                elapsed_seconds=time.perf_counter() - start,
                final_code_path=final_path if isinstance(final_path, Path) else None,
                error_message=(
                    "No candidate passed sandbox tests. "
                    f"Reviewer notes: {reviewer_response.content[:200]}"
                ),
            )
        except Exception as exc:
            return self._result(
                run_id=run_id,
                task=task,
                success=False,
                iterations=1,
                messages=messages,
                elapsed_seconds=time.perf_counter() - start,
                final_code_path=final_path,
                error_message=str(exc),
            )

    @staticmethod
    def _format_candidate_report(candidates: list[dict[str, object]]) -> str:
        lines = []
        for candidate in candidates:
            status = "passed" if candidate["success"] else "failed"
            error = candidate["error"] or ""
            code = str(candidate["code"])
            lines.append(
                f"candidate #{candidate['index']}: {status}; "
                f"length={len(code)}; error={error}"
            )
        return "\n".join(lines)


COORDINATORS = {
    "single_agent": SingleAgentCoordinator,
    "chain": ChainCoordinator,
    "centralized": CentralizedCoordinator,
    "feedback_graph": FeedbackGraphCoordinator,
    "fully_connected": FullyConnectedCoordinator,
    "parallel_consensus": ParallelConsensusCoordinator,
}
