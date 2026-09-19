from dataclasses import dataclass

from engine.execution.docker_executor import DockerCodeExecutor


@dataclass
class DebugTestResult:
    passed: bool
    expected_output: str
    actual_output: str
    status: str


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
                actual_output=execution_result.stderr,
                status="compile_error"
            )

        if execution_result.stage == "timeout":

            return DebugTestResult(
                passed=False,
                expected_output=expected_output,
                actual_output="",
                status="timeout"
            )

        if execution_result.stage == "runtime":

            return DebugTestResult(
                passed=False,
                expected_output=expected_output,
                actual_output=execution_result.stderr,
                status="runtime_error"
            )

        actual_output = execution_result.stdout.strip()
        expected_output = expected_output.strip()

        passed = actual_output == expected_output

        return DebugTestResult(
            passed=passed,
            expected_output=expected_output,
            actual_output=actual_output,
            status="passed" if passed else "wrong_answer"
        )