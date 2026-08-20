from fastapi import HTTPException
from app.ai.agents.answer_evaluator import evaluate_answer
from app.ai.agents.learner_state_updater import update_persistent_mastery
from app.ai.agents.next_lesson_planner import plan_next_lesson
from app.schemas.ai_outputs import SubmitAnswerRequest, SubmitAnswerResponse
from app.seed.demo_exercise_bank import DEMO_EXERCISE_BANK
from app.seed.demo_profiles import BEGINNER_PROFILE, INTERMEDIATE_PROFILE

from typing import TypedDict

from app.schemas.ai_outputs import (
    AnswerEvaluation,
    MasteryUpdate,
    NextLessonPlan,
)


class AnswerWorkflowState(TypedDict, total=False):
    profile_id: str
    exercise_id: str
    user_answer: str

    correct_answer: str
    target_concept: str

    evaluation: AnswerEvaluation
    updated_mastery: MasteryUpdate
    next_lesson_plan: NextLessonPlan

VALID_PROFILE_IDS = {
    BEGINNER_PROFILE["id"],
    INTERMEDIATE_PROFILE["id"],
}


def process_answer_submission(
    request: SubmitAnswerRequest,
) -> SubmitAnswerResponse:
    if request.profile_id not in VALID_PROFILE_IDS:
        raise HTTPException(
            status_code=404,
            detail=f"Unknown demo profile_id: {request.profile_id}",
        )

    exercise = DEMO_EXERCISE_BANK.get(request.exercise_id)

    if exercise is None:
        raise HTTPException(
            status_code=404,
            detail=f"Unknown exercise_id: {request.exercise_id}",
        )

    if exercise["profile_id"] != request.profile_id:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Exercise {request.exercise_id} does not belong to "
                f"profile {request.profile_id}"
            ),
        )

    correct_answer = exercise["correct_answer"]
    target_concept = exercise["target_concept"]

    evaluation = evaluate_answer(
        user_answer=request.user_answer,
        correct_answer=correct_answer,
        target_concept=target_concept,
    )

    updated_mastery = update_persistent_mastery(
        profile_id=request.profile_id,
        target_concept=target_concept,
        evaluation=evaluation,
    )

    next_lesson_plan = plan_next_lesson(
        profile_id=request.profile_id,
        target_concept=target_concept,
        user_answer=request.user_answer,
        correct_answer=correct_answer,
        evaluation=evaluation,
        updated_mastery=updated_mastery,
    )

    next_recommendation = (
        f"{next_lesson_plan.title}: {next_lesson_plan.recommended_activity}"
    )

    return SubmitAnswerResponse(
        profile_id=request.profile_id,
        exercise_id=request.exercise_id,
        user_answer=request.user_answer,
        correct_answer=correct_answer,
        evaluation=evaluation,
        updated_mastery=updated_mastery,
        next_recommendation=next_recommendation,
        next_lesson_plan=next_lesson_plan,
    )