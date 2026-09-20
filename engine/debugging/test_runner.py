from dataclasses import dataclass

from engine.execution.docker_executor import DockerCodeExecutor


@dataclass
class DebugTestResult:
    passed: bool
    expected_output: str
    actual_output: str
    status: str
    stderr: str = ""


class DebugTestRunner:

    def __init__(self):
        self.executor = DockerCodeExecutor()

    def run_test(
        self,
        code: str,
        language: str,
        input_data: str,
        expected_output: str
    ) -> DebugTestResult:

        execution_result = self.executor.execute(
            code=code,
            language=language,
            input_data=input_data
        )

        if execution_result.stage == "compile":

            return DebugTestResult(
                passed=False,
                expected_output=expected_output,
                actual_output="",
                status="compile_error",
                stderr=execution_result.stderr
            )

        if execution_result.stage == "timeout":

            return DebugTestResult(
                passed=False,
                expected_output=expected_output,
                actual_output="",
                status="timeout",
                stderr=""
            )

        if execution_result.stage == "runtime":

            return DebugTestResult(
                passed=False,
                expected_output=expected_output,
                actual_output=execution_result.stdout,
                status="runtime_error",
                stderr=execution_result.stderr
            )

        actual_output = execution_result.stdout.strip()
        expected_output = expected_output.strip()

        passed = actual_output == expected_output

        return DebugTestResult(
            passed=passed,
            expected_output=expected_output,
            actual_output=actual_output,
            status="passed" if passed else "wrong_answer",
            stderr=execution_result.stderr
        )