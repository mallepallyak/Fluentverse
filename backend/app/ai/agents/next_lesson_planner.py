import json

from app.ai.client import generate_structured_json
from app.config import settings
from app.schemas.ai_outputs import AnswerEvaluation, MasteryUpdate, NextLessonPlan


def fallback_next_lesson_plan(
    target_concept: str,
    evaluation: AnswerEvaluation,
    updated_mastery: MasteryUpdate,
) -> NextLessonPlan:
    if evaluation.is_correct:
        return NextLessonPlan(
            title=f"Level up: {target_concept}",
            reason=(
                f"The learner answered correctly, so they are ready for a slightly "
                f"harder activity on {target_concept}."
            ),
            focus_concepts=[target_concept],
            recommended_activity="Try one more production-style exercise using the same concept.",
        )

    return NextLessonPlan(
        title=f"Review: {target_concept}",
        reason=(
            f"The learner missed this item with mistake type "
            f"{evaluation.mistake_type}, so the next step should reinforce the concept."
        ),
        focus_concepts=[target_concept, evaluation.mistake_type],
        recommended_activity="Review a simpler explanation, then complete two guided practice examples.",
    )


def plan_next_lesson(
    *,
    profile_id: str,
    target_concept: str,
    user_answer: str,
    correct_answer: str,
    evaluation: AnswerEvaluation,
    updated_mastery: MasteryUpdate,
) -> NextLessonPlan:
    """
    AI next lesson planner.

    It recommends the next learning step based on the latest answer,
    mistake type, and mastery update.
    """

    if not settings.use_openai:
        return fallback_next_lesson_plan(
            target_concept=target_concept,
            evaluation=evaluation,
            updated_mastery=updated_mastery,
        )

    try:
        raw = generate_structured_json(
            system_prompt=(
                "You are the next lesson planner agent for FluentVerse, an "
                "AI-native Spanish learning app. Recommend the next learning step "
                "based on the learner's latest answer evaluation and mastery update. "
                "Be specific, practical, and aligned with the learner's mistake."
            ),
            user_prompt=(
                "Plan the learner's next step.\n\n"
                f"Profile ID:\n{profile_id}\n\n"
                f"Target concept:\n{target_concept}\n\n"
                f"User answer:\n{user_answer}\n\n"
                f"Correct answer:\n{correct_answer}\n\n"
                f"Answer evaluation:\n{json.dumps(evaluation.model_dump(), ensure_ascii=False, indent=2)}\n\n"
                f"Updated mastery:\n{json.dumps(updated_mastery.model_dump(), ensure_ascii=False, indent=2)}\n\n"
                "Rules:\n"
                "- The title should be short and lesson-like.\n"
                "- The reason should explain why this is the right next step.\n"
                "- focus_concepts should include 1 to 4 concepts.\n"
                "- recommended_activity should be concrete and doable in one short practice block.\n"
                "- If the answer was correct, recommend a slightly harder next step.\n"
                "- If the answer was incorrect, recommend targeted repair practice.\n"
            ),
            schema_name="next_lesson_plan",
            json_schema=NextLessonPlan.model_json_schema(),
        )

        return NextLessonPlan(**raw)

    except Exception as error:
        print(f"OpenAI next lesson planning failed. Falling back to mock planner. Error: {error}")
        return fallback_next_lesson_plan(
            target_concept=target_concept,
            evaluation=evaluation,
            updated_mastery=updated_mastery,
        )