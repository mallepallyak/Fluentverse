from app.schemas.ai_outputs import (
    DemoCompareResponse,
    ContentAnalysis,
    VocabularyItem,
    PersonalizedLesson,
    Exercise,
)

from app.seed.demo_profiles import BEGINNER_PROFILE, INTERMEDIATE_PROFILE


def generate_demo_compare(content: str) -> DemoCompareResponse:
    content_analysis = ContentAnalysis(
        language="Spanish",
        difficulty="A2-B1",
        vocabulary=[
            VocabularyItem(
                term="no sé",
                meaning="I don't know",
                difficulty="beginner"
            ),
            VocabularyItem(
                term="mirada",
                meaning="look, gaze",
                difficulty="intermediate"
            ),
            VocabularyItem(
                term="recordar",
                meaning="to remember",
                difficulty="beginner"
            ),
            VocabularyItem(
                term="viví",
                meaning="I lived",
                difficulty="intermediate"
            ),
        ],
        grammar_concepts=[
            "present tense",
            "hacer + infinitive",
            "preterite tense",
            "relative phrase with que"
        ],
        idioms=[
            "qué tiene tu mirada"
        ],
        slang=[],
        cultural_notes=[
            "The sentence has a romantic, lyric-like emotional tone."
        ],
    )

    beginner_lesson = PersonalizedLesson(
        title="Understanding the Basic Meaning",
        learner_level=BEGINNER_PROFILE["level"],
        focus_concepts=[
            "no sé",
            "tiene",
            "mirada",
            "recordar",
            "basic sentence meaning"
        ],
        explanation=(
            "This sentence means: 'I don't know what your gaze has, "
            "but it makes me remember something I never lived.' "
            "For a beginner, the most important goal is to understand the main words "
            "and the basic sentence structure."
        ),
        examples=[
            "No sé = I don't know",
            "Tu mirada = your gaze / your look",
            "Me hace recordar = it makes me remember"
        ],
        cultural_context=(
            "This sounds like a romantic lyric. Spanish often uses emotional phrases "
            "like 'tu mirada' to describe attraction or memory."
        ),
    )

    intermediate_lesson = PersonalizedLesson(
        title="Emotional Nuance in Lyric-Style Spanish",
        learner_level=INTERMEDIATE_PROFILE["level"],
        focus_concepts=[
            "qué tiene as idiomatic phrasing",
            "hacer + infinitive",
            "emotional meaning of mirada",
            "preterite form viví",
            "poetic interpretation"
        ],
        explanation=(
            "For an intermediate learner, the key is not just literal translation. "
            "'Qué tiene tu mirada' literally means 'what your gaze has,' but naturally "
            "suggests 'there is something about your gaze.' The phrase 'me hace recordar' "
            "uses hacer + infinitive to mean that something causes an emotion or memory."
        ),
        examples=[
            "Hay algo en tu mirada = There is something in your gaze",
            "Me hace pensar = It makes me think",
            "Me hace sentir = It makes me feel"
        ],
        cultural_context=(
            "This line uses a poetic style common in romantic Spanish music and dialogue. "
            "The speaker is describing an emotional reaction, not just a literal memory."
        ),
    )

    beginner_exercises = [
        Exercise(
            type="fill_in_blank",
            prompt="No ___ qué tiene tu mirada.",
            choices=["sé", "soy", "estoy", "tengo"],
            correct_answer="sé",
            target_concept="basic vocabulary"
        ),
        Exercise(
            type="multiple_choice",
            prompt="What does 'tu mirada' mean?",
            choices=["your house", "your gaze", "your song", "your memory"],
            correct_answer="your gaze",
            target_concept="vocabulary"
        ),
    ]

    intermediate_exercises = [
        Exercise(
            type="interpretation",
            prompt=(
                "In natural English, how would you translate "
                "'qué tiene tu mirada'?"
            ),
            choices=None,
            correct_answer="There is something about your gaze.",
            target_concept="idiomatic expression"
        ),
        Exercise(
            type="short_response",
            prompt="Create a new sentence using 'me hace + infinitive'.",
            choices=None,
            correct_answer="Example: Tu voz me hace sentir tranquilo.",
            target_concept="hacer + infinitive"
        ),
    ]

    personalization_differences = [
        "The beginner lesson focuses on basic vocabulary and literal meaning.",
        "The intermediate lesson focuses on idiomatic meaning, emotional nuance, and poetic interpretation.",
        "The beginner exercises use recognition and multiple choice.",
        "The intermediate exercises require interpretation and sentence production.",
        "The same content produces different learning paths because each learner has different goals, known vocabulary, and weak concepts."
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