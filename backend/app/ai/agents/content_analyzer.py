from app.ai.client import generate_structured_json
from app.config import settings
from app.schemas.ai_outputs import ContentAnalysis, VocabularyItem


def mock_content_analysis() -> ContentAnalysis:
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


def analyze_content(content: str) -> ContentAnalysis:
    if not settings.use_openai:
        return mock_content_analysis()

    try:
        raw = generate_structured_json(
            system_prompt=(
                "You are a Spanish language-learning content analyzer for "
                "FluentVerse. Analyze short Spanish lyric-style or dialogue-style "
                "content for a personalized language-learning app. Return only "
                "information useful for teaching Spanish to English-speaking learners."
            ),
            user_prompt=(
                "Analyze this Spanish content:\n\n"
                f"{content}\n\n"
                "Identify vocabulary, grammar concepts, idioms, slang, and cultural notes."
            ),
            schema_name="content_analysis",
            json_schema=ContentAnalysis.model_json_schema(),
        )

        return ContentAnalysis(**raw)

    except Exception as error:
        print(f"OpenAI content analysis failed. Falling back to mock. Error: {error}")
        return mock_content_analysis()