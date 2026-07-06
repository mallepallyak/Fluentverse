from fastapi import APIRouter

from app.schemas.ai_outputs import DemoCompareRequest, DemoCompareResponse
from app.ai.workflows.lesson_workflow import generate_demo_compare


router = APIRouter(prefix="/demo", tags=["Demo"])


@router.post("/compare", response_model=DemoCompareResponse)
def compare_lessons(request: DemoCompareRequest):
    return generate_demo_compare(request.content)