import unittest
import csv
import tempfile
from argparse import Namespace
from dataclasses import dataclass
from pathlib import Path
from unittest.mock import patch

import main
from metrics import summarize
from llm_client import MockLLMClient
from sandbox_runner import SandboxResult
from tasks import get_tasks
from utils import extract_python_code, valid_function


class RecordingTests(unittest.TestCase):
    def test_status_denominator_and_repeat_variation(self):
        rows = [dict(architecture="x", model="mock", repeat_index=repeat, status=status, llm_calls="1")
                for repeat, status in ((1, "passed"), (1, "sandbox_error"), (2, "failed_tests"))]
        result = summarize(rows)[0]
        self.assertEqual((result["eligible"], result["passed"]), (2, 1))
        self.assertEqual(result["infrastructure_failures"], 1)
        self.assertEqual(result["success_rate"], 0.5)
        self.assertGreater(result["repeat_success_rate_stddev"], 0)

    def test_candidate_timeout_counts_as_failure(self):
        rows = [dict(architecture="x", model="mock", repeat_index=1, status=status, llm_calls="1")
                for status in ("passed", "candidate_timeout", "sandbox_error")]
        result = summarize(rows)[0]
        self.assertEqual((result["eligible"], result["passed"]), (2, 1))
        self.assertEqual(result["infrastructure_failures"], 1)
        self.assertEqual(result["success_rate"], 0.5)

    def test_preflight_failure_precedes_client_creation(self):
        args = Namespace(output_dir="runs", list_models=False, mock=False)
        result = SandboxResult(False, "", "", "error", 0, "sandbox_error")
        with patch.object(main, "parse_args", return_value=args), patch.object(main, "load_dotenv"), \
                patch.object(main, "run_code_in_sandbox", return_value=result), \
                patch.object(main, "create_llm_client") as client:
            with self.assertRaisesRegex(RuntimeError, "preflight"):
                main.main()
            client.assert_not_called()

    def test_completed_row_survives_interruption(self):
        @dataclass
        class Row:
            architecture: str = "single_agent"
            model: str = "mock"
            repeat_index: int = 1
            status: str = "passed"
            llm_calls: int = 1
            usage_available: bool = False
            iterations: int = 1
            experiment_id: str = ""

        class Coordinator:
            def __init__(self, **kwargs):
                self.calls = 0

            def run(self, task, run_id):
                self.calls += 1
                if self.calls == 2:
                    raise KeyboardInterrupt
                return Row()

        with tempfile.TemporaryDirectory() as directory:
            args = Namespace(output_dir=directory, list_models=False, mock=True, architectures=["single_agent"],
                             tasks_limit=2, repeats=1, max_iterations=1)
            preflight = SandboxResult(True, "", "", "", 0, "passed")
            with patch.object(main, "parse_args", return_value=args), patch.object(main, "load_dotenv"), \
                    patch.object(main, "run_code_in_sandbox", return_value=preflight), \
                    patch.object(main, "create_llm_client", return_value=MockLLMClient()), \
                    patch.object(main, "COORDINATORS", {"single_agent": Coordinator}):
                with self.assertRaises(KeyboardInterrupt):
                    main.main()
            run = next(Path(directory).iterdir())
            with (run / "raw_results.csv").open(newline="", encoding="utf-8") as stream:
                rows = list(csv.DictReader(stream))
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["status"], "passed")
            with (run / "summary_results.csv").open(newline="", encoding="utf-8") as stream:
                self.assertEqual(next(csv.DictReader(stream))["passed"], "1")

    def test_extraction_and_signature_validation(self):
        task = get_tasks()[0]
        response = 'Example:\n```python\nimport re\ndef normalize_email(email):\n    return email\n```'
        code = extract_python_code(response)
        self.assertTrue(code.startswith("import re"))
        self.assertTrue(valid_function(code, task.function_name, task.description))
        self.assertFalse(valid_function('x = "def normalize_email(email):"', task.function_name, task.description))
        self.assertFalse(valid_function('def normalize_email(x): pass', task.function_name, task.description))
        self.assertFalse(valid_function('def normalize_email(: pass', task.function_name, task.description))
