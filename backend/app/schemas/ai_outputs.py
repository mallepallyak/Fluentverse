from pydantic import BaseModel, ConfigDict
from typing import Optional


class DemoCompareRequest(BaseModel):
    content: str


class LearnerProfile(BaseModel):
    id: str
    native_language: str
    target_language: str
    level: str
    goals: list[str]
    interests: list[str]
    known_vocabulary: list[str]
    weak_concepts: list[str]
    preferred_style: str


class VocabularyItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    term: str
    meaning: str
    difficulty: str


class ContentAnalysis(BaseModel):
    model_config = ConfigDict(extra="forbid")

    language: str
    difficulty: str
    vocabulary: list[VocabularyItem]
    grammar_concepts: list[str]
    idioms: list[str]
    slang: list[str]
    cultural_notes: list[str]

class CurriculumDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    learner_level: str
    selected_focus: list[str]
    skipped_items: list[str]
    reason: str
    target_difficulty: str


class PersonalizedLesson(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    learner_level: str
    focus_concepts: list[str]
    explanation: str
    examples: list[str]
    cultural_context: str


class Exercise(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    type: str
    prompt: str
    choices: list[str] | None
    target_concept: str

class GeneratedExerciseAnswer(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    correct_answer: str
    target_concept: str


class ExerciseGenerationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    exercises: list[Exercise]
    answer_key: list[GeneratedExerciseAnswer]

class PersonalizationExplanation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    beginner_reason: str
    intermediate_reason: str
    key_differences: list[str]

class DemoCompareResponse(BaseModel):
    content: str
    content_analysis: ContentAnalysis
    beginner_lesson: PersonalizedLesson
    intermediate_lesson: PersonalizedLesson
    beginner_exercises: list[Exercise]
    intermediate_exercises: list[Exercise]
    personalization_differences: list[str]
    personalization_explanation: PersonalizationExplanation

class SubmitAnswerRequest(BaseModel):
    profile_id: str
    exercise_id: str
    user_answer: str

class AnswerEvaluation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    is_correct: bool
    score: float
    feedback: str
    mistake_type: str


class MasteryUpdate(BaseModel):
    concept: str
    score_before: float
    score_after: float
    explanation: str

class NextLessonPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    reason: str
    focus_concepts: list[str]
    recommended_activity: str

class SubmitAnswerResponse(BaseModel):
    profile_id: str
    exercise_id: str
    user_answer: str
    correct_answer: str
    evaluation: AnswerEvaluation
    updated_mastery: MasteryUpdate
    next_recommendation: str
    next_lesson_plan: NextLessonPlan
    
class ConceptMasteryState(BaseModel):
    profile_id: str
    concept: str
    score: float
    correct_count: int
    mistake_count: int
    updated_at: str | None = None


class LearnerStateResponse(BaseModel):
    profile_id: str
    mastery: list[ConceptMasteryState]