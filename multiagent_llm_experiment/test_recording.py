import unittest

from metrics import summarize
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

    def test_extraction_and_signature_validation(self):
        task = get_tasks()[0]
        response = 'Example:\n```python\nimport re\ndef normalize_email(email):\n    return email\n```'
        code = extract_python_code(response)
        self.assertTrue(code.startswith("import re"))
        self.assertTrue(valid_function(code, task.function_name, task.description))
        self.assertFalse(valid_function('x = "def normalize_email(email):"', task.function_name, task.description))
        self.assertFalse(valid_function('def normalize_email(x): pass', task.function_name, task.description))
        self.assertFalse(valid_function('def normalize_email(: pass', task.function_name, task.description))
