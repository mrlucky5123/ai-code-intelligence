from engine.validation.code_validator import validate_code
from engine.execution.docker_executor import DockerCodeExecutor


def analyze_code(code: str, language: str):
    is_valid, message = validate_code(code, language)

    if not is_valid:
        return {
            "success": False,
            "status": "validation_error",
            "message": message,
            "language": language
        }

    executor = DockerCodeExecutor()
    execution_result = executor.execute(code, language)

    if execution_result.stage == "timeout":
        status = "timeout"
        success = False

    elif execution_result.stage == "compile":
        status = "compile_error"
        success = False

    elif execution_result.stage == "runtime":
        status = "runtime_error"
        success = False

    else:
        status = "success"
        success = True

    return {
        "success": success,
        "status": status,
        "language": language,
        "stdout": execution_result.stdout,
        "stderr": execution_result.stderr,
        "exit_code": execution_result.exit_code,
        "timed_out": execution_result.timed_out
    }