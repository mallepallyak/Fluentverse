import json

from app.ai.client import generate_structured_json
from app.config import settings
from app.schemas.ai_outputs import (
    ContentAnalysis,
    CurriculumDecision,
    LearnerProfile,
)


def mock_curriculum_decision(profile: LearnerProfile) -> CurriculumDecision:
    if profile.level == "A1":
        return CurriculumDecision(
            learner_level=profile.level,
            selected_focus=[
                "no sé",
                "tiene",
                "mirada",
                "recordar",
                "basic sentence meaning",
            ],
            skipped_items=[
                "poetic interpretation",
                "advanced idiomatic nuance",
                "preterite nuance of viví",
            ],
            reason=(
                "This learner is a beginner, so the lesson should focus on core "
                "vocabulary, literal meaning, and simple sentence structure."
            ),
            target_difficulty="A1-A2",
        )

    return CurriculumDecision(
        learner_level=profile.level,
        selected_focus=[
            "qué tiene as idiomatic phrasing",
            "hacer + infinitive",
            "emotional meaning of mirada",
            "preterite form viví",
            "poetic interpretation",
        ],
        skipped_items=[
            "basic meaning of no sé",
            "basic meaning of tu",
            "simple vocabulary drilling",
        ],
        reason=(
            "This learner already knows some key vocabulary, so the lesson should "
            "focus on idiomatic meaning, emotional nuance, and production."
        ),
        target_difficulty="B1",
    )


def decide_curriculum(
    profile: LearnerProfile,
    analysis: ContentAnalysis,
) -> CurriculumDecision:
    if not settings.use_openai:
        return mock_curriculum_decision(profile)

    try:
        raw = generate_structured_json(
            system_prompt=(
                "You are the curriculum decision agent for FluentVerse, an AI-native "
                "Spanish learning app for English-speaking learners. Your job is to "
                "choose what this specific learner should focus on from the provided "
                "content analysis. Do not create a full lesson. Only decide the "
                "learning focus."
            ),
            user_prompt=(
                "Choose a personalized curriculum focus using these inputs.\n\n"
                f"Learner profile:\n{json.dumps(profile.model_dump(), ensure_ascii=False, indent=2)}\n\n"
                f"Content analysis:\n{json.dumps(analysis.model_dump(), ensure_ascii=False, indent=2)}\n\n"
                "Rules:\n"
                "- selected_focus must come from the actual content analysis.\n"
                "- Do not include concepts, words, or phrases that are not present in the content analysis.\n"
                "- For A1 learners, prioritize concrete vocabulary, basic meaning, and one simple grammar idea.\n"
                "- For B1 learners, prioritize idioms, grammar patterns, natural phrasing, nuance, and production value.\n"
                "- skipped_items should explain what you intentionally avoided for this learner.\n"
                "- reason should clearly explain why this focus matches the learner profile.\n"
                "- target_difficulty should be CEFR-like, such as A1, A1-A2, A2, B1, or B1-B2.\n"
            ),
            schema_name="curriculum_decision",
            json_schema=CurriculumDecision.model_json_schema(),
        )

        return CurriculumDecision(**raw)

    except Exception as error:
        print(f"OpenAI curriculum decision failed. Falling back to mock. Error: {error}")
        return mock_curriculum_decision(profile)