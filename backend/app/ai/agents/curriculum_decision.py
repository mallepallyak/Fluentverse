from app.schemas.ai_outputs import ContentAnalysis, CurriculumDecision, LearnerProfile


def decide_curriculum(
    profile: LearnerProfile,
    analysis: ContentAnalysis,
) -> CurriculumDecision:
    """
    Mock curriculum decision agent.

    This chooses what the learner should focus on based on their level,
    known vocabulary, goals, and weak concepts.
    """

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