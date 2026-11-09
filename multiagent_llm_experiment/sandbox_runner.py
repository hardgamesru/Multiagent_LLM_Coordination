from __future__ import annotations

import json
import secrets
import subprocess
import threading
import time
from dataclasses import dataclass

# Install explicitly before a run; --pull=never prevents implicit downloads.
IMAGE = "python:3.12.8-alpine3.20@sha256:3b1df87fc50e7d47762aeb48673736079aa22e7c98c8851f5453dd49fc03ad1b"
MAX_INPUT = 128 * 1024
MAX_OUTPUT = 16 * 1024

# This driver runs *inside* the container. The random completion token detects
# accidental early exits, not a malicious candidate able to inspect its process.
_DRIVER = r'''
import json, sys
payload = json.load(sys.stdin)
namespace = {"__name__": "__candidate__"}
try:
    exec(compile(payload["code"], "<candidate>", "exec"), namespace)
    exec(compile(payload["tests"], "<tests>", "exec"), namespace)
except SyntaxError:
    result = "invalid_code"
except SystemExit:
    result = "failed_tests"
except BaseException:
    result = "failed_tests"
else:
    result = "passed"
sys.stderr.write("\n" + payload["token"] + ":" + result + "\n")
'''


@dataclass
class SandboxResult:
    success: bool
    stdout: str
    stderr: str
    error_message: str
    elapsed_seconds: float
    status: str = "sandbox_error"


def _drain(stream, limit: int, chunks: list[bytes], keep_tail: bool = False) -> None:
    remaining = limit
    while True:
        block = stream.read(4096)
        if not block:
            break
        if keep_tail:
            # Keep the final bytes so noisy candidates cannot accidentally hide
            # the driver's completion record behind earlier stderr output.
            chunks[:] = [(b"".join(chunks) + block)[-limit:]]
        elif remaining:
            chunks.append(block[:remaining])
            remaining -= min(remaining, len(block))


def run_code_in_sandbox(code: str, tests: str, timeout: int = 5) -> SandboxResult:
    start = time.monotonic()

    def result(status: str, message: str, stdout: str = "", stderr: str = "") -> SandboxResult:
        return SandboxResult(status == "passed", stdout, stderr, message,
                             time.monotonic() - start, status)

    if timeout <= 0 or len(code.encode("utf-8")) + len(tests.encode("utf-8")) > MAX_INPUT:
        return result("invalid_code", "Invalid timeout or input too large")
    token = secrets.token_hex(24)
    name = "llm-benchmark-" + secrets.token_hex(12)
    payload = json.dumps({"code": code, "tests": tests, "token": token}).encode("utf-8")
    command = ["docker", "run", "--rm", "-i", "--name", name,
               "--pull=never", "--network=none", "--read-only", "--user=65534:65534",
               "--cap-drop=ALL", "--security-opt=no-new-privileges", "--pids-limit=64",
               "--memory=256m", "--cpus=1", "--tmpfs", "/tmp:rw,noexec,nosuid,size=16m",
               IMAGE, "python", "-I", "-c", _DRIVER]
    proc = None
    out, err = [], []
    threads = []
    try:
        proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        for stream, chunks, keep_tail in ((proc.stdout, out, False), (proc.stderr, err, True)):
            thread = threading.Thread(target=_drain, args=(stream, MAX_OUTPUT, chunks, keep_tail), daemon=True)
            thread.start()
            threads.append(thread)

        def feed() -> None:
            try:
                proc.stdin.write(payload)
                proc.stdin.close()
            except (BrokenPipeError, OSError, ValueError):
                pass

        threading.Thread(target=feed, daemon=True).start()
        proc.wait(timeout=timeout)
        for thread in threads:
            thread.join(timeout=1)
        stdout = b"".join(out).decode("utf-8", "replace")
        stderr = b"".join(err).decode("utf-8", "replace")
        marker = token + ":"
        # The completion message is checked in addition to the Docker exit status.
        matches = [line[len(marker):] for line in stderr.splitlines() if line.startswith(marker)]
        if proc.returncode == 0 and len(matches) == 1 and matches[0] in {"passed", "failed_tests", "invalid_code"}:
            status = matches[0]
            return result(status, "" if status == "passed" else status, stdout, "")
        return result("sandbox_error", "Container or test driver failed")
    except FileNotFoundError:
        return result("sandbox_unavailable", "Docker is not installed or unavailable")
    except subprocess.TimeoutExpired:
        return result("sandbox_timeout", "Sandbox execution timed out")
    except OSError:
        return result("sandbox_error", "Could not start sandbox")
    finally:
        if proc is not None:
            # Kill the named container as well as the CLI, even on interruption.
            try:
                subprocess.run(["docker", "rm", "-f", name], stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL, timeout=5, check=False)
            except (OSError, subprocess.SubprocessError):
                pass
            if proc.poll() is None:
                proc.kill()
            try:
                proc.wait(timeout=2)
            except subprocess.SubprocessError:
                pass
            for thread in threads:
                thread.join(timeout=1)
            for stream in (proc.stdin, proc.stdout, proc.stderr):
                if stream is not None and not stream.closed:
                    stream.close()
