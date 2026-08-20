from typing_extensions import NotRequired, TypedDict
from langgraph.graph import END, START, StateGraph
from app.seed.demo_exercise_bank import DEMO_EXERCISE_BANK
from app.ai.agents.answer_evaluator import evaluate_answer
from app.schemas.ai_outputs import AnswerEvaluation
from app.ai.agents.learner_state_updater import update_persistent_mastery
from app.schemas.ai_outputs import AnswerEvaluation, MasteryUpdate
from typing import Literal
from typing_extensions import NotRequired, TypedDict
from app.ai.agents.next_lesson_planner import plan_next_lesson
from app.schemas.ai_outputs import (
    AnswerEvaluation,
    MasteryUpdate,
    NextLessonPlan,
    SubmitAnswerRequest,
    SubmitAnswerResponse,
)

NextAction = Literal["remediate", "practice", "advance"]

class AnswerWorkflowState(TypedDict):
    # Input state: these must exist when the graph starts.
    profile_id: str
    exercise_id: str
    user_answer: str

    # Derived state: nodes will add these later.
    correct_answer: NotRequired[str]
    target_concept: NotRequired[str]
    evaluation: NotRequired[AnswerEvaluation]
    updated_mastery: NotRequired[MasteryUpdate]
    
    next_action: NotRequired[NextAction]
    planning_instruction: NotRequired[str]
    next_lesson_plan: NotRequired[NextLessonPlan]


def load_exercise_node(
    state: AnswerWorkflowState,
) -> dict:
    exercise = DEMO_EXERCISE_BANK.get(state["exercise_id"])

    if exercise is None:
        raise ValueError(
            f"Unknown exercise_id: {state['exercise_id']}"
        )

    if exercise["profile_id"] != state["profile_id"]:
        raise ValueError(
            f"Exercise {state['exercise_id']} does not belong to "
            f"profile {state['profile_id']}"
        )

    return {
        "correct_answer": exercise["correct_answer"],
        "target_concept": exercise["target_concept"],
    }

def evaluate_answer_node(
    state: AnswerWorkflowState,
) -> dict:
    evaluation = evaluate_answer(
        user_answer=state["user_answer"],
        correct_answer=state["correct_answer"],
        target_concept=state["target_concept"],
    )

    return {
        "evaluation": evaluation,
    }

def update_mastery_node(
    state: AnswerWorkflowState,
) -> dict:
    updated_mastery = update_persistent_mastery(
        profile_id=state["profile_id"],
        target_concept=state["target_concept"],
        evaluation=state["evaluation"],
    )

    return {
        "updated_mastery": updated_mastery,
    }

def route_after_mastery(
    state: AnswerWorkflowState,
) -> NextAction:
    score = state["updated_mastery"].score_after

    if score < 0.40:
        return "remediate"

    if score < 0.75:
        return "practice"

    return "advance"

def remediate_node(
    state: AnswerWorkflowState,
) -> dict:
    return {
        "next_action": "remediate",
        "planning_instruction": (
            "The learner has low mastery. Use a simpler explanation, "
            "one concrete example, and guided practice on the same concept."
        ),
    }


def practice_node(
    state: AnswerWorkflowState,
) -> dict:
    return {
        "next_action": "practice",
        "planning_instruction": (
            "The learner has developing mastery. Give targeted practice "
            "at roughly the same difficulty with less scaffolding."
        ),
    }


def advance_node(
    state: AnswerWorkflowState,
) -> dict:
    return {
        "next_action": "advance",
        "planning_instruction": (
            "The learner has strong mastery. Increase difficulty slightly "
            "or apply the concept in a more natural production task."
        ),
    }

def plan_next_lesson_node(
    state: AnswerWorkflowState,
) -> dict:
    next_lesson_plan = plan_next_lesson(
        profile_id=state["profile_id"],
        target_concept=state["target_concept"],
        user_answer=state["user_answer"],
        correct_answer=state["correct_answer"],
        evaluation=state["evaluation"],
        updated_mastery=state["updated_mastery"],
        next_action=state["next_action"],
        planning_instruction=state["planning_instruction"],
    )

    return {
        "next_lesson_plan": next_lesson_plan,
    }

builder = StateGraph(AnswerWorkflowState)

builder.add_node("load_exercise", load_exercise_node)
builder.add_node("evaluate_answer", evaluate_answer_node)
builder.add_node("update_mastery", update_mastery_node)
builder.add_node("remediate", remediate_node)
builder.add_node("practice", practice_node)
builder.add_node("advance", advance_node)
builder.add_node(
    "plan_next_lesson",
    plan_next_lesson_node,
)

builder.add_edge(START, "load_exercise")
builder.add_edge("load_exercise", "evaluate_answer")
builder.add_edge("evaluate_answer", "update_mastery")
builder.add_conditional_edges(
    "update_mastery",
    route_after_mastery,
)
builder.add_edge("remediate", "plan_next_lesson")
builder.add_edge("practice", "plan_next_lesson")
builder.add_edge("advance", "plan_next_lesson")
builder.add_edge("plan_next_lesson", END)


answer_graph = builder.compile()    

def process_answer_submission_with_graph(
    request: SubmitAnswerRequest,
) -> SubmitAnswerResponse:
    result = answer_graph.invoke(
        {
            "profile_id": request.profile_id,
            "exercise_id": request.exercise_id,
            "user_answer": request.user_answer,
        }
    )

    next_lesson_plan = result["next_lesson_plan"]

    return SubmitAnswerResponse(
        profile_id=result["profile_id"],
        exercise_id=result["exercise_id"],
        user_answer=result["user_answer"],
        correct_answer=result["correct_answer"],
        evaluation=result["evaluation"],
        updated_mastery=result["updated_mastery"],
        next_recommendation=(
            f"{next_lesson_plan.title}: "
            f"{next_lesson_plan.recommended_activity}"
        ),
        next_lesson_plan=next_lesson_plan,
    )