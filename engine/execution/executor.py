from dataclasses import dataclass
import subprocess
import tempfile
from pathlib import Path


@dataclass
class ExecutionResult:
    stdout: str
    stderr: str
    exit_code: int
    timed_out: bool
    stage: str


class CodeExecutor:

    def execute(self, code: str, language: str) -> ExecutionResult:
        if language.lower() != "cpp":
            return ExecutionResult(
                stdout="",
                stderr=f"Unsupported language: {language}",
                exit_code=-1,
                timed_out=False,
                stage="validation"
            )

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            source_file = temp_path / "main.cpp"
            executable_file = temp_path / "main.exe"

            source_file.write_text(code)

            compile_result = subprocess.run(
                [
                    "g++",
                    str(source_file),
                    "-o",
                    str(executable_file)
                ],
                capture_output=True,
                text=True
            )

            if compile_result.returncode != 0:
                return ExecutionResult(
                    stdout=compile_result.stdout,
                    stderr=compile_result.stderr,
                    exit_code=compile_result.returncode,
                    timed_out=False,
                    stage="compile"
                )

            try:
                run_result = subprocess.run(
                    [str(executable_file)],
                    capture_output=True,
                    text=True,
                    timeout=5
                )

                return ExecutionResult(
                    stdout=run_result.stdout,
                    stderr=run_result.stderr,
                    exit_code=run_result.returncode,
                    timed_out=False,
                    stage="success" if run_result.returncode == 0 else "runtime"
                )

            except subprocess.TimeoutExpired as error:
                return ExecutionResult(
                    stdout=error.stdout or "",
                    stderr=error.stderr or "",
                    exit_code=-1,
                    timed_out=True,
                    stage="timeout"
                )