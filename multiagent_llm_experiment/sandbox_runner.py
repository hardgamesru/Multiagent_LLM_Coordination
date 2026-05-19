from __future__ import annotations

import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path


@dataclass
class SandboxResult:
    success: bool
    stdout: str
    stderr: str
    error_message: str
    elapsed_seconds: float


def run_code_in_sandbox(code: str, tests: str, timeout: int = 5) -> SandboxResult:
    start = time.perf_counter()
    with tempfile.TemporaryDirectory() as temp_dir:
        script_path = Path(temp_dir) / "candidate_test.py"
        script_path.write_text(
            f"{code.strip()}\n\n{tests.strip()}\n\nprint('SANDBOX_OK')\n",
            encoding="utf-8",
        )
        try:
            completed = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=temp_dir,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            return SandboxResult(
                success=False,
                stdout=exc.stdout or "",
                stderr=exc.stderr or "",
                error_message="Timeout",
                elapsed_seconds=time.perf_counter() - start,
            )

    elapsed = time.perf_counter() - start
    success = completed.returncode == 0
    error_message = "" if success else _compact_error(completed.stderr or completed.stdout)
    return SandboxResult(
        success=success,
        stdout=completed.stdout,
        stderr=completed.stderr,
        error_message=error_message,
        elapsed_seconds=elapsed,
    )


def _compact_error(output: str) -> str:
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    if not lines:
        return "Unknown sandbox error"
    return " | ".join(lines[-4:])
