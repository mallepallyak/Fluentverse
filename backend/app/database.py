import sqlite3
from pathlib import Path
from typing import Any


DB_PATH = Path(__file__).resolve().parent.parent / "fluentverse.db"


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS concept_mastery (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_id TEXT NOT NULL,
                concept TEXT NOT NULL,
                score REAL NOT NULL DEFAULT 0.60,
                correct_count INTEGER NOT NULL DEFAULT 0,
                mistake_count INTEGER NOT NULL DEFAULT 0,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(profile_id, concept)
            );
            """
        )
        connection.commit()


def get_or_create_mastery(profile_id: str, concept: str) -> dict[str, Any]:
    with get_connection() as connection:
        existing = connection.execute(
            """
            SELECT profile_id, concept, score, correct_count, mistake_count, updated_at
            FROM concept_mastery
            WHERE profile_id = ? AND concept = ?;
            """,
            (profile_id, concept),
        ).fetchone()

        if existing:
            return dict(existing)

        connection.execute(
            """
            INSERT INTO concept_mastery (
                profile_id,
                concept,
                score,
                correct_count,
                mistake_count
            )
            VALUES (?, ?, 0.60, 0, 0);
            """,
            (profile_id, concept),
        )
        connection.commit()

        created = connection.execute(
            """
            SELECT profile_id, concept, score, correct_count, mistake_count, updated_at
            FROM concept_mastery
            WHERE profile_id = ? AND concept = ?;
            """,
            (profile_id, concept),
        ).fetchone()

        return dict(created)


def update_mastery_score(
    profile_id: str,
    concept: str,
    is_correct: bool,
) -> dict[str, Any]:
    current = get_or_create_mastery(profile_id=profile_id, concept=concept)
    score_before = float(current["score"])

    if is_correct:
        score_after = min(score_before + 0.08, 1.0)
        correct_increment = 1
        mistake_increment = 0
    else:
        score_after = max(score_before - 0.10, 0.0)
        correct_increment = 0
        mistake_increment = 1

    with get_connection() as connection:
        connection.execute(
            """
            UPDATE concept_mastery
            SET
                score = ?,
                correct_count = correct_count + ?,
                mistake_count = mistake_count + ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE profile_id = ? AND concept = ?;
            """,
            (
                score_after,
                correct_increment,
                mistake_increment,
                profile_id,
                concept,
            ),
        )
        connection.commit()

    return {
        "concept": concept,
        "score_before": score_before,
        "score_after": score_after,
    }


def list_mastery_for_profile(profile_id: str) -> list[dict[str, Any]]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT profile_id, concept, score, correct_count, mistake_count, updated_at
            FROM concept_mastery
            WHERE profile_id = ?
            ORDER BY updated_at DESC;
            """,
            (profile_id,),
        ).fetchall()

        return [dict(row) for row in rows]