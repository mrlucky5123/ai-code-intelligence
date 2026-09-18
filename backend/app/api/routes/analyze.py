from fastapi import APIRouter 
from pydantic import BaseModel

from backend.app.services.analyze_service import analyze_code as run_analysis

router = APIRouter()


class AnalyzeRequest(BaseModel):
    code: str
    language: str


@router.post("/analyze")
def analyze_code(request: AnalyzeRequest):
    return run_analysis(request.code, request.language)