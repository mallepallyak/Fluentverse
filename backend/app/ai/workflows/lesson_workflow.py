from app.ai.agents.content_analyzer import analyze_content
from app.ai.agents.curriculum_decision import decide_curriculum
from app.ai.agents.exercise_generator import generate_exercises
from app.ai.agents.lesson_generator import generate_lesson
from app.ai.agents.personalization_explainer import explain_personalization
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
        analysis=content_analysis,
        decision=beginner_decision,
    )

    intermediate_exercises = generate_exercises(
        profile=intermediate_profile,
        analysis=content_analysis,
        decision=intermediate_decision,
    )

    personalization_explanation = explain_personalization(
        content_analysis=content_analysis,
        beginner_profile=beginner_profile,
        intermediate_profile=intermediate_profile,
        beginner_decision=beginner_decision,
        intermediate_decision=intermediate_decision,
        beginner_lesson=beginner_lesson,
        intermediate_lesson=intermediate_lesson,
    )

    return DemoCompareResponse(
        content=content,
        content_analysis=content_analysis,
        beginner_lesson=beginner_lesson,
        intermediate_lesson=intermediate_lesson,
        beginner_exercises=beginner_exercises,
        intermediate_exercises=intermediate_exercises,
        personalization_differences=personalization_explanation.key_differences,
        personalization_explanation=personalization_explanation,
    )