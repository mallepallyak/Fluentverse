import json

from app.ai.client import generate_structured_json
from app.config import settings
from app.schemas.ai_outputs import (
    ContentAnalysis,
    CurriculumDecision,
    LearnerProfile,
    PersonalizationExplanation,
    PersonalizedLesson,
)


def fallback_personalization_explanation(
    beginner_decision: CurriculumDecision,
    intermediate_decision: CurriculumDecision,
) -> PersonalizationExplanation:
    return PersonalizationExplanation(
        beginner_reason=beginner_decision.reason,
        intermediate_reason=intermediate_decision.reason,
        key_differences=[
            "The beginner path focuses on basic vocabulary and simple meaning.",
            "The intermediate path focuses on idioms, grammar patterns, and natural phrasing.",
            "The two learners receive different lessons because their goals, levels, and weak concepts are different.",
        ],
    )


def explain_personalization(
    *,
    content_analysis: ContentAnalysis,
    beginner_profile: LearnerProfile,
    intermediate_profile: LearnerProfile,
    beginner_decision: CurriculumDecision,
    intermediate_decision: CurriculumDecision,
    beginner_lesson: PersonalizedLesson,
    intermediate_lesson: PersonalizedLesson,
) -> PersonalizationExplanation:
    """
    AI explanation agent for why the two generated lesson paths differ.
    """

    if not settings.use_openai:
        return fallback_personalization_explanation(
            beginner_decision=beginner_decision,
            intermediate_decision=intermediate_decision,
        )

    try:
        raw = generate_structured_json(
            system_prompt=(
                "You are the personalization explanation agent for FluentVerse. "
                "Explain why two learners received different lesson paths from the "
                "same Spanish content. Be clear, concise, and product-demo friendly."
            ),
            user_prompt=(
                "Explain the personalization differences.\n\n"
                f"Content analysis:\n{json.dumps(content_analysis.model_dump(), ensure_ascii=False, indent=2)}\n\n"
                f"Beginner profile:\n{json.dumps(beginner_profile.model_dump(), ensure_ascii=False, indent=2)}\n\n"
                f"Intermediate profile:\n{json.dumps(intermediate_profile.model_dump(), ensure_ascii=False, indent=2)}\n\n"
                f"Beginner curriculum decision:\n{json.dumps(beginner_decision.model_dump(), ensure_ascii=False, indent=2)}\n\n"
                f"Intermediate curriculum decision:\n{json.dumps(intermediate_decision.model_dump(), ensure_ascii=False, indent=2)}\n\n"
                f"Beginner lesson:\n{json.dumps(beginner_lesson.model_dump(), ensure_ascii=False, indent=2)}\n\n"
                f"Intermediate lesson:\n{json.dumps(intermediate_lesson.model_dump(), ensure_ascii=False, indent=2)}\n\n"
                "Rules:\n"
                "- beginner_reason should explain the beginner lesson choice.\n"
                "- intermediate_reason should explain the intermediate lesson choice.\n"
                "- key_differences should contain 3 to 5 short concrete differences.\n"
                "- Do not mention internal implementation details.\n"
                "- Do not invent user data not present in the profiles.\n"
            ),
            schema_name="personalization_explanation",
            json_schema=PersonalizationExplanation.model_json_schema(),
        )

        return PersonalizationExplanation(**raw)

    except Exception as error:
        print(f"OpenAI personalization explanation failed. Falling back to mock. Error: {error}")
        return fallback_personalization_explanation(
            beginner_decision=beginner_decision,
            intermediate_decision=intermediate_decision,
        )