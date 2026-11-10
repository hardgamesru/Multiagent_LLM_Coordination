from __future__ import annotations

import ast
import json
import queue
import secrets
import subprocess
import threading
import time
from dataclasses import dataclass
from pathlib import Path

IMAGE = "python:3.12.8-alpine3.20@sha256:3b1df87fc50e7d47762aeb48673736079aa22e7c98c8851f5453dd49fc03ad1b"
MAX_INPUT = 128 * 1024
MAX_OUTPUT = 16 * 1024
MAX_RPC = 64 * 1024
_DIR = Path(__file__).resolve().parent


@dataclass
class SandboxResult:
    success: bool
    stdout: str
    stderr: str
    error_message: str
    elapsed_seconds: float
    status: str = "sandbox_error"


def _drain(stream, limit: int, chunks: list[bytes], keep_tail: bool = False,
           ready=None, ready_marker: bytes = b"", initialized=None,
           initialized_marker: bytes = b"") -> None:
    remaining = limit
    pending = b""
    while True:
        block = stream.read1(4096) if hasattr(stream, "read1") else stream.read(4096)
        if not block:
            break
        if (ready is not None and not ready.is_set()) or (initialized is not None and not initialized.is_set()):
            combined = pending + block
            if ready is not None and ready_marker in combined:
                ready.set()
            if initialized is not None and initialized_marker in combined:
                initialized.set()
            pending = combined[-max(len(ready_marker), len(initialized_marker), 256):]
        if keep_tail:
            chunks[:] = [(b"".join(chunks) + block)[-limit:]]
        elif remaining:
            chunks.append(block[:remaining])
            remaining -= min(remaining, len(block))


def _command(name: str, script: str) -> list[str]:
    return ["docker", "run", "--rm", "-i", "--name", name, "--pull=never",
            "--network=none", "--read-only", "--user=65534:65534", "--cap-drop=ALL",
            "--security-opt=no-new-privileges", "--pids-limit=64", "--memory=256m",
            "--cpus=1", "--tmpfs", "/tmp:rw,noexec,nosuid,size=16m",
            IMAGE, "python", "-I", "-c", script]


def run_code_in_sandbox(code: str, tests: str, timeout: int = 5,
                        *, diagnostics: bool = False, startup_timeout: int = 20) -> SandboxResult:
    """Run candidate and trusted assertions in separate, unconnected containers.

    The host relays bounded JSON calls and never executes either source string.
    Candidate output is only a function response, never an evaluator verdict.
    """
    start = time.monotonic()

    def result(status: str, message: str) -> SandboxResult:
        return SandboxResult(status == "passed", "", "", message, time.monotonic() - start, status)

    if timeout <= 0 or startup_timeout <= 0 or len(code.encode("utf-8")) + len(tests.encode("utf-8")) > MAX_INPUT:
        return result("invalid_code", "Invalid timeout or input too large")
    try:
        tree = ast.parse(code)
        ast.parse(tests)
    except SyntaxError:
        return result("invalid_code", "invalid_code")
    functions = [node.name for node in tree.body if isinstance(node, ast.FunctionDef)]
    processes = []
    names = []
    threads = []
    worker_lines = queue.Queue(maxsize=4)
    outcome = queue.Queue(maxsize=1)
    ready_events = []
    worker_initialized = threading.Event()

    def spawn(role: str, script_name: str, payload: dict):
        name = "llm-benchmark-" + secrets.token_hex(12)
        marker = "ready-" + secrets.token_hex(24)
        initialized_marker = "initialized-" + secrets.token_hex(24)
        script = (_DIR / script_name).read_text(encoding="utf-8")
        proc = subprocess.Popen(_command(name, script), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        names.append(name)
        processes.append(proc)
        event = threading.Event()
        ready_events.append(event)
        thread = threading.Thread(target=_drain, args=(proc.stderr, MAX_OUTPUT, [], True,
                                                       event, (marker + "\n").encode(),
                                                       worker_initialized if role == "worker" else None,
                                                       (initialized_marker + "\n").encode()), daemon=True)
        thread.start()
        threads.append(thread)
        payload["ready"] = marker
        if role == "worker":
            payload["initialized"] = initialized_marker
        data = (json.dumps(payload, ensure_ascii=True) + "\n").encode()

        def feed():
            try:
                proc.stdin.write(data)
                proc.stdin.flush()
            except (BrokenPipeError, OSError, ValueError):
                pass
        thread = threading.Thread(target=feed, daemon=True)
        thread.start()
        threads.append(thread)
        return proc

    def read_worker(proc):
        try:
            while True:
                line = proc.stdout.readline(MAX_RPC + 1)
                if not line or len(line) > MAX_RPC or not line.endswith(b"\n"):
                    worker_lines.put(None)
                    return
                worker_lines.put(line)
        except (OSError, ValueError):
            worker_lines.put(None)

    def relay(evaluator, worker):
        try:
            while True:
                line = evaluator.stdout.readline(MAX_RPC + 1)
                if not line or len(line) > MAX_RPC or not line.endswith(b"\n"):
                    outcome.put(("sandbox_error", "Evaluator protocol failed"))
                    return
                message = json.loads(line)
                if not isinstance(message, dict):
                    raise ValueError("invalid message")
                if message.get("type") == "final":
                    status = message.get("status")
                    detail = message.get("diagnostic")
                    if status not in {"passed", "failed_tests"} or not isinstance(detail, str):
                        raise ValueError("invalid verdict")
                    # A candidate that died before returning a response cannot pass.
                    if status == "passed" and worker.poll() is not None:
                        status, detail = "failed_tests", ""
                    text = "" if status == "passed" else status
                    if diagnostics and status == "failed_tests" and detail:
                        text += ": " + detail[:512]
                    outcome.put((status, text))
                    return
                if message.get("type") != "call":
                    raise ValueError("invalid request")
                try:
                    worker.stdin.write(line)
                    worker.stdin.flush()
                    response = worker_lines.get(timeout=timeout + 1)
                except (BrokenPipeError, OSError, ValueError, queue.Empty):
                    response = None
                if response is None:
                    response = b'{"ok":false,"exception":"RuntimeError"}\n'
                evaluator.stdin.write(response)
                evaluator.stdin.flush()
        except (ValueError, TypeError, json.JSONDecodeError, BrokenPipeError, OSError):
            outcome.put(("sandbox_error", "Evaluator protocol failed"))

    try:
        worker = spawn("worker", "sandbox_worker.py", {"code": code})
        thread = threading.Thread(target=read_worker, args=(worker,), daemon=True)
        thread.start()
        threads.append(thread)
        evaluator = spawn("evaluator", "sandbox_evaluator.py",
                          {"tests": tests, "functions": functions, "diagnostics": diagnostics})
        deadline = time.monotonic() + startup_timeout
        for proc, event in zip(processes, ready_events):
            while not event.wait(0.05):
                if proc.poll() is not None:
                    return result("sandbox_error", "Container failed before test execution")
                if time.monotonic() >= deadline:
                    return result("sandbox_error", "Container startup timed out")
        execution_deadline = time.monotonic() + timeout
        while not worker_initialized.wait(0.05):
            if worker.poll() is not None:
                return result("failed_tests", "Candidate exited during initialization")
            if time.monotonic() >= execution_deadline:
                return result("candidate_timeout", "Candidate exceeded the execution time limit")
        thread = threading.Thread(target=relay, args=(evaluator, worker), daemon=True)
        thread.start()
        threads.append(thread)
        try:
            status, message = outcome.get(timeout=max(0, execution_deadline - time.monotonic()))
        except queue.Empty:
            return result("candidate_timeout", "Candidate or tests exceeded the execution time limit")
        return result(status, message)
    except FileNotFoundError:
        return result("sandbox_unavailable", "Docker is not installed or unavailable")
    except OSError:
        return result("sandbox_error", "Could not start sandbox")
    finally:
        for name in names:
            try:
                subprocess.run(["docker", "rm", "-f", name], stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL, timeout=5, check=False)
            except (OSError, subprocess.SubprocessError):
                pass
        for proc in processes:
            if proc.poll() is None:
                proc.kill()
            try:
                proc.wait(timeout=2)
            except subprocess.SubprocessError:
                pass
        for thread in threads:
            thread.join(timeout=0.5)
        for proc in processes:
            for stream in (proc.stdin, proc.stdout, proc.stderr):
                if stream is not None and not stream.closed:
                    stream.close()
