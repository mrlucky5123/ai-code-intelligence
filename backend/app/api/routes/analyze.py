from fastapi import APIRouter
from pydantic import BaseModel, Field

from engine.ai.debugger import AIDebugger
from engine.ai.groq_provider import GroqProvider
from engine.ai.models import DebugContext
from engine.validation.code_validator import validate_code
from engine.debugging.test_runner import DebugTestRunner


router = APIRouter()


class AnalyzeRequest(BaseModel):
    code: str
    language: str
    input: str = ""
    expected_output: str = Field(min_lenght=1)


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

    explanation = None

    if not result.passed:

        context = DebugContext(
            code=request.code,
            language=request.language,
            input_data=request.input,
            expected_output=result.expected_output,
            actual_output=result.actual_output,
            status=result.status,
            stderr=result.stderr
        )

        provider = GroqProvider()

        debugger = AIDebugger(provider)

        explanation_result = debugger.explain_failure(context)

        explanation = explanation_result.explanation

    return {
        "success": result.passed,
        "status": result.status,
        "expected_output": result.expected_output,
        "actual_output": result.actual_output,
        "explanation": explanation
    }