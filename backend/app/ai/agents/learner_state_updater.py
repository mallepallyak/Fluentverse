from app.database import update_mastery_score
from app.schemas.ai_outputs import AnswerEvaluation, MasteryUpdate


def update_persistent_mastery(
    profile_id: str,
    target_concept: str,
    evaluation: AnswerEvaluation,
) -> MasteryUpdate:
    """
    Deterministic learner-state updater.

    AI decides correctness and mistake type.
    Backend deterministically updates mastery.
    """

    result = update_mastery_score(
        profile_id=profile_id,
        concept=target_concept,
        is_correct=evaluation.is_correct,
    )

    if evaluation.is_correct:
        explanation = (
            f"Mastery increased because the learner answered correctly on "
            f"{target_concept} with score {evaluation.score:.2f}."
        )
    else:
        explanation = (
            f"Mastery decreased because the learner made a "
            f"{evaluation.mistake_type} mistake on {target_concept} "
            f"with score {evaluation.score:.2f}."
        )

    return MasteryUpdate(
        concept=target_concept,
        score_before=result["score_before"],
        score_after=result["score_after"],
        explanation=explanation,
    )