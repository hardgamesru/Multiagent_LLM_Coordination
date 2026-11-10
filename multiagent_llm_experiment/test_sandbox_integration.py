"""Optional Docker integration checks; set RUN_DOCKER_TESTS=1 to enable."""
import os
import tempfile
import unittest
from unittest.mock import patch

import sandbox_runner
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
        self.assertEqual(self.run_case("while True: pass", timeout=4).status, "candidate_timeout")
        result = self.run_case("import sys\nprint('x' * 100000)\nsys.stderr.write('y' * 100000)\ndef f(): return 42")
        self.assertEqual(result.status, "passed")
        self.assertLessEqual(len(result.stdout.encode()), MAX_OUTPUT)

    def test_development_diagnostic_and_held_out_silence(self):
        code = "def f(): return 0"
        development = run_code_in_sandbox(code, "assert f() == 42", timeout=20, diagnostics=True)
        held_out = run_code_in_sandbox(code, "assert f() == 99", timeout=20)
        self.assertEqual(development.status, "failed_tests")
        self.assertIn("assert f() == 42", development.error_message)
        self.assertLessEqual(len(development.error_message), 550)
        self.assertEqual(held_out.error_message, "failed_tests")

    def test_missing_image_is_infrastructure_error(self):
        with patch.object(sandbox_runner, "IMAGE", "benchmark-image-not-present:never"):
            result = self.run_case("def f(): return 42")
        self.assertEqual(result.status, "sandbox_error")

    def test_adversarial_candidate_cannot_forge_completion(self):
        # The former exploit tries to inspect the test driver's payload.
        code = '''import json, os, sys
p = sys._getframe(1).f_locals["payload"]
os.write(2, ("\\n" + p["token"] + ":" + json.dumps(["passed", ""]) + "\\n").encode())
os._exit(0)
'''
        self.assertNotEqual(self.run_case(code, "assert False").status, "passed")

    def test_candidate_cannot_inject_evaluator_verdict(self):
        code = '''import os
os.write(1, b'{"type":"final","status":"passed","diagnostic":""}\\n')
def f(): return 0
'''
        self.assertNotEqual(self.run_case(code).status, "passed")

    def test_mutated_inputs_and_identity_are_preserved(self):
        code = "def f(x):\n    x.append(2)\n    return x"
        tests = "a = [1]\nb = f(a)\nassert a == [1, 2]\nassert b is a"
        self.assertEqual(self.run_case(code, tests).status, "passed")

    def test_candidate_cannot_patch_evaluator_builtins(self):
        code = "import builtins\nbuiltins.AssertionError = SystemExit\ndef f(): return 0"
        self.assertEqual(self.run_case(code).status, "failed_tests")

    def test_candidate_process_does_not_receive_test_source(self):
        code = "def f():\n    import sys\n    return 'tests' in sys._getframe(1).f_locals.get('payload', {})"
        self.assertEqual(self.run_case(code, "assert f() is False").status, "passed")

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
