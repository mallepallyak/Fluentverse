from pydantic import BaseModel
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
    term: str
    meaning: str
    difficulty: str


class ContentAnalysis(BaseModel):
    language: str
    difficulty: str
    vocabulary: list[VocabularyItem]
    grammar_concepts: list[str]
    idioms: list[str]
    slang: list[str]
    cultural_notes: list[str]

class CurriculumDecision(BaseModel):
    learner_level: str
    selected_focus: list[str]
    skipped_items: list[str]
    reason: str
    target_difficulty: str


class PersonalizedLesson(BaseModel):
    title: str
    learner_level: str
    focus_concepts: list[str]
    explanation: str
    examples: list[str]
    cultural_context: str


class Exercise(BaseModel):
    type: str
    prompt: str
    choices: Optional[list[str]] = None
    correct_answer: str
    target_concept: str


class DemoCompareResponse(BaseModel):
    content: str
    content_analysis: ContentAnalysis
    beginner_lesson: PersonalizedLesson
    intermediate_lesson: PersonalizedLesson
    beginner_exercises: list[Exercise]
    intermediate_exercises: list[Exercise]
    personalization_differences: list[str]