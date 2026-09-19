from fastapi import APIRouter
from pydantic import BaseModel

from engine.debugging.test_runner import DebugTestRunner
from engine.validation.code_validator import validate_code


router = APIRouter()


class AnalyzeRequest(BaseModel):
    code: str
    language: str
    input: str = ""
    expected_output: str = ""


@router.post("/analyze")
def analyze_code(request: AnalyzeRequest):

    is_valid, message = validate_code(
        request.code,
        request.language
    )

    if not is_valid:
        return {
            "success": False,
            "status": "validation_error",
            "message": message
        }

    test_runner = DebugTestRunner()

    result = test_runner.run_test(
        code=request.code,
        language=request.language,
        input_data=request.input,
        expected_output=request.expected_output
    )

    return {
        "success": result.passed,
        "status": result.status,
        "expected_output": result.expected_output,
        "actual_output": result.actual_output
    }