from dataclasses import dataclass
import subprocess
import tempfile
from pathlib import Path


@dataclass
class DockerExecutionResult:
    stdout: str
    stderr: str
    exit_code: int
    timed_out: bool
    stage: str


class DockerCodeExecutor:

    def execute(
        self,
        code: str,
        language: str,
        input_data: str = ""
    ) -> DockerExecutionResult:

        language = language.lower()

        if language not in {"cpp", "python"}:
            return DockerExecutionResult(
                stdout="",
                stderr=f"Unsupported language: {language}",
                exit_code=-1,
                timed_out=False,
                stage="validation"
            )

        with tempfile.TemporaryDirectory() as temp_dir:

            temp_path = Path(temp_dir)

            if language == "cpp":
                source_file = temp_path / "main.cpp"

            else:
                source_file = temp_path / "main.py"

            source_file.write_text(code)

            container_id = None

            try:
                create_result = subprocess.run(
                    [
                        "docker",
                        "create",
                        "--network",
                        "none",
                        "--cpus",
                        "1",
                        "--memory",
                        "256m",
                        "--pids-limit",
                        "64",
                        "--cap-drop",
                        "ALL",
                        "--security-opt",
                        "no-new-privileges:true",
                        "--read-only",
                        "--tmpfs",
                        "/tmp:rw,nosuid,exec,size=64m",
                        "--label",
                        "ai-code-intelligence.executor=true",
                        "-v",
                        f"{temp_path}:/workspace:ro",
                        "cpp-execution-image",
                        "sleep",
                        "300"
                    ],
                    capture_output=True,
                    text=True,
                    check=True
                )

                container_id = create_result.stdout.strip()

                subprocess.run(
                    [
                        "docker",
                        "start",
                        container_id
                    ],
                    capture_output=True,
                    text=True,
                    check=True
                )

                # Compile C++ code
                if language == "cpp":

                    compile_result = subprocess.run(
                        [
                            "docker",
                            "exec",
                            "-i",
                            container_id,
                            "g++",
                            "/workspace/main.cpp",
                            "-o",
                            "/tmp/main"
                        ],
                        capture_output=True,
                        text=True
                    )

                    if compile_result.returncode != 0:
                        return DockerExecutionResult(
                            stdout=compile_result.stdout,
                            stderr=compile_result.stderr,
                            exit_code=compile_result.returncode,
                            timed_out=False,
                            stage="compile"
                        )

                    run_command = [
                        "docker",
                        "exec",
                        "-i",
                        container_id,
                        "/tmp/main"
                    ]

                # Execute Python directly
                else:

                    run_command = [
                        "docker",
                        "exec",
                        "-i",
                        container_id,
                        "python3",
                        "/workspace/main.py"
                    ]

                try:
                    run_result = subprocess.run(
                        run_command,
                        input=input_data,
                        capture_output=True,
                        text=True,
                        timeout=5
                    )

                except subprocess.TimeoutExpired as error:

                    return DockerExecutionResult(
                        stdout=error.stdout or "",
                        stderr=error.stderr or "",
                        exit_code=-1,
                        timed_out=True,
                        stage="timeout"
                    )

                if run_result.returncode == 0:
                    stage = "success"
                else:
                    stage = "runtime"

                return DockerExecutionResult(
                    stdout=run_result.stdout,
                    stderr=run_result.stderr,
                    exit_code=run_result.returncode,
                    timed_out=False,
                    stage=stage
                )

            finally:

                if container_id is not None:

                    subprocess.run(
                        [
                            "docker",
                            "rm",
                            "-f",
                            container_id
                        ],
                        capture_output=True,
                        text=True
                    )