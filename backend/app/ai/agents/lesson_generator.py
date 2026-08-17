import json

from app.ai.client import generate_structured_json
from app.config import settings
from app.schemas.ai_outputs import (
    ContentAnalysis,
    CurriculumDecision,
    LearnerProfile,
    PersonalizedLesson,
)


def mock_lesson(profile: LearnerProfile, decision: CurriculumDecision) -> PersonalizedLesson:
    if profile.level == "A1":
        return PersonalizedLesson(
            title="Understanding the Basic Meaning",
            learner_level=profile.level,
            focus_concepts=decision.selected_focus,
            explanation=(
                "This sentence means: 'I don't know what your gaze has, "
                "but it makes me remember something I never lived.' "
                "For a beginner, the most important goal is to understand the main "
                "words and the basic sentence structure."
            ),
            examples=[
                "No sé = I don't know",
                "Tu mirada = your gaze / your look",
                "Me hace recordar = it makes me remember",
            ],
            cultural_context=(
                "This sounds like a romantic lyric. Spanish often uses emotional "
                "phrases like 'tu mirada' to describe attraction or memory."
            ),
        )

    return PersonalizedLesson(
        title="Emotional Nuance in Lyric-Style Spanish",
        learner_level=profile.level,
        focus_concepts=decision.selected_focus,
        explanation=(
            "For an intermediate learner, the key is not just literal translation. "
            "'Qué tiene tu mirada' literally means 'what your gaze has,' but "
            "naturally suggests 'there is something about your gaze.' The phrase "
            "'me hace recordar' uses hacer + infinitive to mean that something "
            "causes an emotion or memory."
        ),
        examples=[
            "Hay algo en tu mirada = There is something in your gaze",
            "Me hace pensar = It makes me think",
            "Me hace sentir = It makes me feel",
        ],
        cultural_context=(
            "This line uses a poetic style common in romantic Spanish music and "
            "dialogue. The speaker is describing an emotional reaction, not just "
            "a literal memory."
        ),
    )


def generate_lesson(
    profile: LearnerProfile,
    analysis: ContentAnalysis,
    decision: CurriculumDecision,
) -> PersonalizedLesson:
    if not settings.use_openai:
        return mock_lesson(profile=profile, decision=decision)

    try:
        raw = generate_structured_json(
            system_prompt=(
                "You are the personalized lesson generation agent for FluentVerse, "
                "an AI-native Spanish learning app for English-speaking learners. "
                "Generate a lesson that matches the learner profile, uses the provided "
                "content analysis, and follows the curriculum decision. Keep the lesson "
                "clear, useful, and appropriate for the learner level."
            ),
            user_prompt=(
                "Create a personalized Spanish lesson using these inputs.\n\n"
                f"Learner profile:\n{json.dumps(profile.model_dump(), ensure_ascii=False, indent=2)}\n\n"
                f"Content analysis:\n{json.dumps(analysis.model_dump(), ensure_ascii=False, indent=2)}\n\n"
                f"Curriculum decision:\n{json.dumps(decision.model_dump(), ensure_ascii=False, indent=2)}\n\n"
                "Rules:\n"
                "- The lesson must match the learner level.\n"
                "- The explanation must teach the actual input content, not a different sentence.\n"
                "- Beginner lessons should be simple and concrete.\n"
                "- Intermediate lessons should include nuance, natural meaning, and grammar patterns.\n"
                "- Examples should be short and useful.\n"
                "- Do not include exercise questions here.\n"
            ),
            schema_name="personalized_lesson",
            json_schema=PersonalizedLesson.model_json_schema(),
        )

        return PersonalizedLesson(**raw)

    except Exception as error:
        print(f"OpenAI lesson generation failed. Falling back to mock. Error: {error}")
        return mock_lesson(profile=profile, decision=decision)