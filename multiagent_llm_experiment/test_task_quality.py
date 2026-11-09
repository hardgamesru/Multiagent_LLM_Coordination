"""Run fixture quality checks only in the Docker sandbox."""
import os
import unittest

from llm_client import MockLLMClient
from sandbox_runner import run_code_in_sandbox
from tasks import get_tasks


@unittest.skipUnless(os.environ.get("RUN_DOCKER_TESTS") == "1", "Docker integration is opt-in")
class TaskQualityTests(unittest.TestCase):
    def test_good_and_bad_fixtures(self):
        client = MockLLMClient()
        for task in get_tasks():
            code = client._solution_for_prompt(task.description)
            for kind, tests in (("development", task.development_tests), ("evaluation", task.hidden_tests)):
                with self.subTest(task=task.task_id, tests=kind, fixture="good"):
                    result = run_code_in_sandbox(code, tests, timeout=20)
                    self.assertEqual(result.status, "passed")
                with self.subTest(task=task.task_id, tests=kind, fixture="bad"):
                    broken = code + "\n" + task.function_name + " = lambda *args, **kwargs: None\n"
                    result = run_code_in_sandbox(broken, tests, timeout=20)
                    self.assertEqual(result.status, "failed_tests")
