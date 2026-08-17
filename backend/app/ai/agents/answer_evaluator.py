import json

from app.ai.client import generate_structured_json
from app.config import settings
from app.schemas.ai_outputs import AnswerEvaluation


VALID_MISTAKE_TYPES = [
    "none",
    "vocabulary_unknown",
    "verb_conjugation",
    "gender_agreement",
    "tense_confusion",
    "pronoun_usage",
    "word_order",
    "idiom_misunderstanding",
    "literal_translation",
    "cultural_context_gap",
    "concept_gap",
]


def normalize_answer(answer: str) -> str:
    return answer.strip().lower()


def fallback_classify_mistake(target_concept: str, correct_answer: str) -> str:
    concept = target_concept.lower()
    answer = correct_answer.lower()

    if "vocabulary" in concept:
        return "vocabulary_unknown"

    if "idiom" in concept or "expression" in concept:
        return "idiom_misunderstanding"

    if "pronoun" in concept or "clitic" in concept or "te" in concept:
        return "pronoun_usage"

    if "preterite" in concept or "pretérito" in concept or "tense" in concept:
        return "tense_confusion"

    if "literal" in concept or "translation" in concept:
        return "literal_translation"

    if "sé" in answer or "saber" in answer:
        return "verb_conjugation"

    return "concept_gap"


def fallback_evaluate_answer(
    user_answer: str,
    correct_answer: str,
    target_concept: str,
) -> AnswerEvaluation:
    is_correct = normalize_answer(user_answer) == normalize_answer(correct_answer)

    if is_correct:
        return AnswerEvaluation(
            is_correct=True,
            score=1.0,
            feedback=(
                f"Correct. Your answer matches the expected answer for "
                f"{target_concept}."
            ),
            mistake_type="none",
        )

    mistake_type = fallback_classify_mistake(
        target_concept=target_concept,
        correct_answer=correct_answer,
    )

    return AnswerEvaluation(
        is_correct=False,
        score=0.0,
        feedback=(
            f"Not quite. You answered '{user_answer}', but the expected answer is "
            f"'{correct_answer}'. Review this concept: {target_concept}."
        ),
        mistake_type=mistake_type,
    )


def evaluate_answer(
    user_answer: str,
    correct_answer: str,
    target_concept: str,
) -> AnswerEvaluation:
    """
    AI answer evaluator + mistake classifier.

    It accepts semantically equivalent open-ended answers instead of requiring
    exact string matching.
    """

    if not settings.use_openai:
        return fallback_evaluate_answer(
            user_answer=user_answer,
            correct_answer=correct_answer,
            target_concept=target_concept,
        )

    try:
        raw = generate_structured_json(
            system_prompt=(
                "You are the answer evaluation and mistake classification agent "
                "for FluentVerse, an AI-native Spanish learning app. Evaluate the "
                "learner's answer semantically, not only by exact string match. "
                "Give brief helpful feedback and classify the mistake type."
            ),
            user_prompt=(
                "Evaluate this learner answer.\n\n"
                f"User answer:\n{user_answer}\n\n"
                f"Reference correct answer:\n{correct_answer}\n\n"
                f"Target concept:\n{target_concept}\n\n"
                f"Allowed mistake types:\n{json.dumps(VALID_MISTAKE_TYPES)}\n\n"
                "Rules:\n"
                "- Accept semantically equivalent answers, even if wording differs.\n"
                "- For multiple choice or fill-in-the-blank, be stricter.\n"
                "- For interpretation or short response, grade meaning and usefulness.\n"
                "- score must be between 0.0 and 1.0.\n"
                "- is_correct should usually be true when score >= 0.75.\n"
                "- If correct, mistake_type must be 'none'.\n"
                "- If incorrect, choose one mistake_type from the allowed list.\n"
                "- Feedback should be short, specific, and encouraging.\n"
            ),
            schema_name="answer_evaluation",
            json_schema=AnswerEvaluation.model_json_schema(),
        )

        evaluation = AnswerEvaluation(**raw)

        if evaluation.mistake_type not in VALID_MISTAKE_TYPES:
            evaluation.mistake_type = "concept_gap"

        return evaluation

    except Exception as error:
        print(f"OpenAI answer evaluation failed. Falling back to exact evaluator. Error: {error}")
        return fallback_evaluate_answer(
            user_answer=user_answer,
            correct_answer=correct_answer,
            target_concept=target_concept,
        )