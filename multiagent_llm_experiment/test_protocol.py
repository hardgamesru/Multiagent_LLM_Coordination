"""Verify that held-out results cannot influence any model call or selection."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from coordinators import COORDINATORS
from llm_client import MockLLMClient
from sandbox_runner import SandboxResult
from tasks import get_tasks


class RecordingClient(MockLLMClient):
    def __init__(self, events):
        super().__init__()
        self.events = events

    def generate(self, system_prompt, user_prompt):
        self.events.append(("model", system_prompt + user_prompt))
        return super().generate(system_prompt, user_prompt)


class ProtocolTests(unittest.TestCase):
    def test_all_architectures_keep_held_out_last(self):
        task = get_tasks()[0]
        for architecture, coordinator in COORDINATORS.items():
            for dev_status, eval_status in (("passed", "failed_tests"),
                                            ("failed_tests", "passed"),
                                            ("passed", "sandbox_error")):
                with self.subTest(architecture=architecture, dev=dev_status, evaluation=eval_status):
                    events = []

                    def runner(code, tests, *, diagnostics=False):
                        kind = "eval" if tests == task.hidden_tests else "dev"
                        self.assertIn(tests, (task.hidden_tests, task.development_tests))
                        self.assertEqual(diagnostics, kind == "dev")
                        events.append((kind, code))
                        status = eval_status if kind == "eval" else dev_status
                        return SandboxResult(status == "passed", "", "", status, 0.0, status)

                    with tempfile.TemporaryDirectory() as directory, patch("coordinators.run_code_in_sandbox", runner):
                        result = coordinator(RecordingClient(events), Path(directory), 2).run(task, "test")
                    self.assertEqual([event[0] for event in events].count("eval"), 1, result)
                    self.assertEqual(events[-1][0], "eval")
                    for kind, prompt in events:
                        if kind == "model":
                            self.assertNotIn(task.hidden_tests, prompt)
                    self.assertEqual(result.success, eval_status == "passed")
                    self.assertEqual(result.status, eval_status)
                    self.assertEqual(result.evaluation_test_calls, 1)

    def test_development_infrastructure_failure_is_not_sent_to_model(self):
        task = get_tasks()[0]
        for name in ("feedback_graph", "parallel_consensus"):
            events = []
            def runner(code, tests, *, diagnostics=False):
                events.append(("dev", code))
                return SandboxResult(False, "", "", "sandbox_error", 0.0, "sandbox_error")
            with self.subTest(architecture=name), tempfile.TemporaryDirectory() as directory, patch("coordinators.run_code_in_sandbox", runner):
                result = COORDINATORS[name](RecordingClient(events), Path(directory), 2).run(task, "test")
            self.assertEqual(result.status, "sandbox_error")
            self.assertEqual(result.evaluation_test_calls, 0)
            self.assertEqual(events[-1][0], "dev")

    def test_all_tasks_have_distinct_development_tests(self):
        for task in get_tasks():
            self.assertTrue(task.development_tests.strip())
            self.assertNotIn(task.development_tests.strip(), task.hidden_tests)

    def test_feedback_includes_only_development_diagnostic(self):
        task = get_tasks()[0]
        events = []
        diagnostic = 'AssertionError at development test line 1: assert example == expected'
        def runner(code, tests, *, diagnostics=False):
            events.append(("eval" if tests == task.hidden_tests else "dev", code))
            if tests == task.hidden_tests:
                self.assertFalse(diagnostics)
                return SandboxResult(False, "", "", "failed_tests", 0, "failed_tests")
            self.assertTrue(diagnostics)
            return SandboxResult(False, "", "", diagnostic, 0, "failed_tests")
        with tempfile.TemporaryDirectory() as directory, patch("coordinators.run_code_in_sandbox", runner):
            COORDINATORS["feedback_graph"](RecordingClient(events), Path(directory), 2).run(task, "test")
        prompts = [text for kind, text in events if kind == "model"]
        self.assertTrue(any(diagnostic in prompt for prompt in prompts))
        self.assertTrue(all(task.hidden_tests not in prompt for prompt in prompts))


if __name__ == "__main__":
    unittest.main()
