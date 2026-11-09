"""Optional Docker integration checks; set RUN_DOCKER_TESTS=1 to enable."""
import os
import tempfile
import unittest
from unittest.mock import patch

from sandbox_runner import MAX_OUTPUT, run_code_in_sandbox


@unittest.skipUnless(os.environ.get("RUN_DOCKER_TESTS") == "1", "Docker integration is opt-in")
class DockerSandboxTests(unittest.TestCase):
    def run_case(self, code, tests="assert f() == 42", timeout=20):
        return run_code_in_sandbox(code, tests, timeout=timeout)

    def test_pass_and_failed_assertion(self):
        self.assertEqual(self.run_case("def f(): return 42").status, "passed")
        self.assertEqual(self.run_case("def f(): return 0").status, "failed_tests")

    def test_syntax_and_early_exit(self):
        self.assertEqual(self.run_case("def f(: pass").status, "invalid_code")
        self.assertEqual(self.run_case("import sys; sys.exit(0)").status, "failed_tests")

    def test_timeout_and_bounded_output(self):
        self.assertEqual(self.run_case("while True: pass", timeout=4).status, "sandbox_timeout")
        result = self.run_case("import sys\nprint('x' * 100000)\nsys.stderr.write('y' * 100000)\ndef f(): return 42")
        self.assertEqual(result.status, "passed")
        self.assertLessEqual(len(result.stdout.encode()), MAX_OUTPUT)

    def test_parent_secret_and_network_unavailable(self):
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, {"BENCHMARK_HOST_ONLY_SECRET": "private-test-value"}):
            secret = os.path.join(directory, "host-secret.txt")
            with open(secret, "w", encoding="utf-8") as stream:
                stream.write("private-test-value")
            code = '''import os, socket
assert "BENCHMARK_HOST_ONLY_SECRET" not in os.environ
assert not os.path.exists(%r)
s = socket.socket()
s.settimeout(2)
try:
    s.connect(("1.1.1.1", 53))
except OSError:
    pass
else:
    raise AssertionError("network unexpectedly available")
finally:
    s.close()
def f(): return 42
''' % secret
            self.assertEqual(self.run_case(code).status, "passed")


if __name__ == "__main__":
    unittest.main()
