"""Offline sandbox contract checks. These tests never execute candidate code."""
import unittest
from unittest.mock import patch

import sandbox_runner


class SandboxSecurityTests(unittest.TestCase):
    def test_missing_docker_fails_closed(self):
        with patch.object(sandbox_runner.subprocess, "Popen", side_effect=FileNotFoundError) as popen:
            result = sandbox_runner.run_code_in_sandbox("raise RuntimeError('never run')", "assert False")
        self.assertEqual(result.status, "sandbox_unavailable")
        self.assertFalse(result.success)
        self.assertEqual(popen.call_count, 1)
        command = popen.call_args.args[0]
        self.assertEqual(command[0:2], ["docker", "run"])
        for flag in ("--pull=never", "--network=none", "--read-only", "--user=65534:65534",
                     "--cap-drop=ALL", "--security-opt=no-new-privileges", "--pids-limit=64"):
            self.assertIn(flag, command)
        self.assertNotIn("-v", command)

    def test_input_limit_fails_before_starting_process(self):
        with patch.object(sandbox_runner.subprocess, "Popen") as popen:
            result = sandbox_runner.run_code_in_sandbox("x" * (sandbox_runner.MAX_INPUT + 1), "")
        self.assertEqual(result.status, "invalid_code")
        popen.assert_not_called()

    def test_bounded_output_reader(self):
        from io import BytesIO
        chunks = []
        sandbox_runner._drain(BytesIO(b"a" * 100000), 100, chunks)
        self.assertEqual(len(b"".join(chunks)), 100)


if __name__ == "__main__":
    unittest.main()
