from fastapi import APIRouter, HTTPException

from app.ai.workflows.answer_workflow import process_answer_submission
from app.ai.workflows.lesson_workflow import generate_demo_compare
from app.database import list_mastery_for_profile
from app.schemas.ai_outputs import (
    ConceptMasteryState,
    DemoCompareRequest,
    DemoCompareResponse,
    LearnerStateResponse,
    SubmitAnswerRequest,
    SubmitAnswerResponse,
)
from app.seed.demo_profiles import BEGINNER_PROFILE, INTERMEDIATE_PROFILE


router = APIRouter(prefix="/demo", tags=["Demo"])

VALID_PROFILE_IDS = {
    BEGINNER_PROFILE["id"],
    INTERMEDIATE_PROFILE["id"],
}


@router.post("/compare", response_model=DemoCompareResponse)
def compare_lessons(request: DemoCompareRequest):
    return generate_demo_compare(request.content)


@router.post("/submit-answer", response_model=SubmitAnswerResponse)
def submit_answer(request: SubmitAnswerRequest):
    return process_answer_submission(request)


@router.get("/profiles/{profile_id}/state", response_model=LearnerStateResponse)
def get_learner_state(profile_id: str):
    if profile_id not in VALID_PROFILE_IDS:
        raise HTTPException(
            status_code=404,
            detail=f"Unknown demo profile_id: {profile_id}",
        )

    mastery_rows = list_mastery_for_profile(profile_id)

    return LearnerStateResponse(
        profile_id=profile_id,
        mastery=[ConceptMasteryState(**row) for row in mastery_rows],
    )