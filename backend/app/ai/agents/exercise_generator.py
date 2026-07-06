from app.schemas.ai_outputs import CurriculumDecision, Exercise, LearnerProfile


def generate_exercises(
    profile: LearnerProfile,
    decision: CurriculumDecision,
) -> list[Exercise]:
    """
    Mock exercise generator.

    Later this will generate exercises dynamically from the lesson focus.
    """

    if profile.level == "A1":
        return [
            Exercise(
                type="fill_in_blank",
                prompt="No ___ qué tiene tu mirada.",
                choices=["sé", "soy", "estoy", "tengo"],
                correct_answer="sé",
                target_concept="basic vocabulary",
            ),
            Exercise(
                type="multiple_choice",
                prompt="What does 'tu mirada' mean?",
                choices=["your house", "your gaze", "your song", "your memory"],
                correct_answer="your gaze",
                target_concept="vocabulary",
            ),
        ]

    return [
        Exercise(
            type="interpretation",
            prompt=(
                "In natural English, how would you translate "
                "'qué tiene tu mirada'?"
            ),
            choices=None,
            correct_answer="There is something about your gaze.",
            target_concept="idiomatic expression",
        ),
        Exercise(
            type="short_response",
            prompt="Create a new sentence using 'me hace + infinitive'.",
            choices=None,
            correct_answer="Example: Tu voz me hace sentir tranquilo.",
            target_concept="hacer + infinitive",
        ),
    ]