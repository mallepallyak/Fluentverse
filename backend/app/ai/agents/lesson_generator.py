from app.ai.agents.content_analyzer import analyze_content
from app.ai.agents.curriculum_decision import decide_curriculum
from app.ai.agents.lesson_generator import generate_lesson
from app.ai.agents.exercise_generator import generate_exercises
from app.schemas.ai_outputs import DemoCompareResponse, LearnerProfile
from app.seed.demo_profiles import BEGINNER_PROFILE, INTERMEDIATE_PROFILE


def generate_demo_compare(content: str) -> DemoCompareResponse:
    beginner_profile = LearnerProfile(**BEGINNER_PROFILE)
    intermediate_profile = LearnerProfile(**INTERMEDIATE_PROFILE)

    content_analysis = analyze_content(content)

    beginner_decision = decide_curriculum(
        profile=beginner_profile,
        analysis=content_analysis,
    )

    intermediate_decision = decide_curriculum(
        profile=intermediate_profile,
        analysis=content_analysis,
    )

    beginner_lesson = generate_lesson(
        profile=beginner_profile,
        analysis=content_analysis,
        decision=beginner_decision,
    )

    intermediate_lesson = generate_lesson(
        profile=intermediate_profile,
        analysis=content_analysis,
        decision=intermediate_decision,
    )

    beginner_exercises = generate_exercises(
        profile=beginner_profile,
        decision=beginner_decision,
    )

    intermediate_exercises = generate_exercises(
        profile=intermediate_profile,
        decision=intermediate_decision,
    )

    personalization_differences = [
        "The beginner curriculum decision selects basic vocabulary and sentence meaning.",
        "The intermediate curriculum decision selects idiomatic meaning, emotional nuance, and production.",
        "The beginner lesson skips advanced poetic interpretation.",
        "The intermediate lesson skips basic vocabulary that the learner likely already knows.",
        "The same content produces different learning paths because each learner has different goals, known vocabulary, and weak concepts.",
    ]

    return DemoCompareResponse(
        content=content,
        content_analysis=content_analysis,
        beginner_lesson=beginner_lesson,
        intermediate_lesson=intermediate_lesson,
        beginner_exercises=beginner_exercises,
        intermediate_exercises=intermediate_exercises,
        personalization_differences=personalization_differences,
    )