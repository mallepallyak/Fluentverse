import json
from uuid import uuid4

from app.ai.client import generate_structured_json
from app.config import settings
from app.schemas.ai_outputs import (
    ContentAnalysis,
    CurriculumDecision,
    Exercise,
    ExerciseGenerationResult,
    GeneratedExerciseAnswer,
    LearnerProfile,
)
from app.seed.demo_exercise_bank import register_generated_answers


def mock_exercise_generation(profile: LearnerProfile) -> ExerciseGenerationResult:
    if profile.level == "A1":
        return ExerciseGenerationResult(
            exercises=[
                Exercise(
                    id="beginner_vocab_1",
                    type="fill_in_blank",
                    prompt="No ___ qué tiene tu mirada.",
                    choices=["sé", "soy", "estoy", "tengo"],
                    target_concept="basic vocabulary",
                ),
                Exercise(
                    id="beginner_vocab_2",
                    type="multiple_choice",
                    prompt="What does 'tu mirada' mean?",
                    choices=["your house", "your gaze", "your song", "your memory"],
                    target_concept="vocabulary",
                ),
            ],
            answer_key=[
                GeneratedExerciseAnswer(
                    id="beginner_vocab_1",
                    correct_answer="sé",
                    target_concept="basic vocabulary",
                ),
                GeneratedExerciseAnswer(
                    id="beginner_vocab_2",
                    correct_answer="your gaze",
                    target_concept="vocabulary",
                ),
            ],
        )

    return ExerciseGenerationResult(
        exercises=[
            Exercise(
                id="intermediate_idiom_1",
                type="interpretation",
                prompt=(
                    "In natural English, how would you translate "
                    "'qué tiene tu mirada'?"
                ),
                choices=None,
                target_concept="idiomatic expression",
            ),
            Exercise(
                id="intermediate_grammar_1",
                type="short_response",
                prompt="Create a new sentence using 'me hace + infinitive'.",
                choices=None,
                target_concept="hacer + infinitive",
            ),
        ],
        answer_key=[
            GeneratedExerciseAnswer(
                id="intermediate_idiom_1",
                correct_answer="There is something about your gaze.",
                target_concept="idiomatic expression",
            ),
            GeneratedExerciseAnswer(
                id="intermediate_grammar_1",
                correct_answer="Example: Tu voz me hace sentir tranquilo.",
                target_concept="hacer + infinitive",
            ),
        ],
    )


def add_unique_ids(
    result: ExerciseGenerationResult,
    profile: LearnerProfile,
) -> ExerciseGenerationResult:
    """
    Prevent generated IDs from colliding across repeated demo generations.
    """

    id_map: dict[str, str] = {}

    for exercise in result.exercises:
        new_id = f"{profile.id}_{uuid4().hex[:8]}"
        id_map[exercise.id] = new_id
        exercise.id = new_id

    for answer in result.answer_key:
        if answer.id in id_map:
            answer.id = id_map[answer.id]

    return result


def generate_exercise_result(
    profile: LearnerProfile,
    analysis: ContentAnalysis,
    decision: CurriculumDecision,
) -> ExerciseGenerationResult:
    if not settings.use_openai:
        result = mock_exercise_generation(profile)
        register_generated_answers(profile_id=profile.id, answer_key=result.answer_key)
        return result

    try:
        raw = generate_structured_json(
            system_prompt=(
                "You are the exercise generation agent for FluentVerse, an AI-native "
                "Spanish learning app for English-speaking learners. Generate short, "
                "useful exercises based only on the provided content analysis and "
                "curriculum decision. Return public exercises and a private answer key."
            ),
            user_prompt=(
                "Generate personalized Spanish exercises using these inputs.\n\n"
                f"Learner profile:\n{json.dumps(profile.model_dump(), ensure_ascii=False, indent=2)}\n\n"
                f"Content analysis:\n{json.dumps(analysis.model_dump(), ensure_ascii=False, indent=2)}\n\n"
                f"Curriculum decision:\n{json.dumps(decision.model_dump(), ensure_ascii=False, indent=2)}\n\n"
                "Rules:\n"
                "- Generate exactly 2 exercises.\n"
                "- Each exercise id can be simple for now, like ex_1 and ex_2.\n"
                "- The exercises must teach the actual input content.\n"
                "- Do not generate exercises about words or phrases absent from the content analysis.\n"
                "- For A1 learners, prefer multiple_choice or fill_in_blank.\n"
                "- For B1 learners, prefer interpretation, short_response, or transformation.\n"
                "- Public exercises must not reveal the correct answer.\n"
                "- The answer_key must include the correct answer for each exercise id.\n"
                "- Every answer_key id must match one public exercise id.\n"
                "- target_concept must match between the public exercise and its answer key.\n"
                "- Every exercise must include choices. Use null for open-ended exercises.\n"
            ),
            schema_name="exercise_generation_result",
            json_schema=ExerciseGenerationResult.model_json_schema(),
        )

        result = ExerciseGenerationResult(**raw)
        result = add_unique_ids(result=result, profile=profile)

        register_generated_answers(
            profile_id=profile.id,
            answer_key=result.answer_key,
        )

        return result

    except Exception as error:
        print(f"OpenAI exercise generation failed. Falling back to mock. Error: {error}")
        result = mock_exercise_generation(profile)
        register_generated_answers(profile_id=profile.id, answer_key=result.answer_key)
        return result


def generate_exercises(
    profile: LearnerProfile,
    analysis: ContentAnalysis,
    decision: CurriculumDecision,
) -> list[Exercise]:
    result = generate_exercise_result(
        profile=profile,
        analysis=analysis,
        decision=decision,
    )

    return result.exercises