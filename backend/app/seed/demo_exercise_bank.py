DEMO_EXERCISE_BANK = {
    "beginner_vocab_1": {
        "profile_id": "beginner_demo",
        "correct_answer": "sé",
        "target_concept": "basic vocabulary",
    },
    "beginner_vocab_2": {
        "profile_id": "beginner_demo",
        "correct_answer": "your gaze",
        "target_concept": "vocabulary",
    },
    "intermediate_idiom_1": {
        "profile_id": "intermediate_demo",
        "correct_answer": "There is something about your gaze.",
        "target_concept": "idiomatic expression",
    },
    "intermediate_grammar_1": {
        "profile_id": "intermediate_demo",
        "correct_answer": "Example: Tu voz me hace sentir tranquilo.",
        "target_concept": "hacer + infinitive",
    },
}


def register_generated_answers(
    *,
    profile_id: str,
    answer_key: list,
) -> None:
    """
    Store generated answer keys in memory for the current backend process.

    This is fine for the MVP demo. Soon, this should move into SQLite.
    """

    for answer in answer_key:
        DEMO_EXERCISE_BANK[answer.id] = {
            "profile_id": profile_id,
            "correct_answer": answer.correct_answer,
            "target_concept": answer.target_concept,
        }