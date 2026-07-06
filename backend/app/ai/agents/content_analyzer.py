from app.schemas.ai_outputs import ContentAnalysis, VocabularyItem


def analyze_content(content: str) -> ContentAnalysis:
    """
    Mock content analyzer.

    Later this will call an LLM and return structured content analysis.
    For now, it returns a stable analysis for our demo sentence.
    """

    return ContentAnalysis(
        language="Spanish",
        difficulty="A2-B1",
        vocabulary=[
            VocabularyItem(
                term="no sé",
                meaning="I don't know",
                difficulty="beginner",
            ),
            VocabularyItem(
                term="mirada",
                meaning="look, gaze",
                difficulty="intermediate",
            ),
            VocabularyItem(
                term="recordar",
                meaning="to remember",
                difficulty="beginner",
            ),
            VocabularyItem(
                term="viví",
                meaning="I lived",
                difficulty="intermediate",
            ),
        ],
        grammar_concepts=[
            "present tense",
            "hacer + infinitive",
            "preterite tense",
            "relative phrase with que",
        ],
        idioms=[
            "qué tiene tu mirada",
        ],
        slang=[],
        cultural_notes=[
            "The sentence has a romantic, lyric-like emotional tone.",
        ],
    )