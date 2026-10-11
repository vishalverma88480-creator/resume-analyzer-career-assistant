import sqlite3
import json
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "resume_analyzer.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection



def create_table():
    connection = get_connection()

    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL DEFAULT '',
                score INTEGER NOT NULL DEFAULT 0,
                word_count INTEGER NOT NULL DEFAULT 0,
                skills_found TEXT NOT NULL DEFAULT '[]',
                strengths TEXT NOT NULL DEFAULT '[]',
                improvements TEXT NOT NULL DEFAULT '[]',
                career_recommendations TEXT NOT NULL DEFAULT '[]',
                roadmap TEXT NOT NULL DEFAULT '[]',
                analysis_details TEXT NOT NULL DEFAULT '{}'
            )
        """)

        # Add columns missing from an older database.
        existing_columns = {
            row["name"]
            for row in connection.execute(
                "PRAGMA table_info(analyses)"
            ).fetchall()
        }

        required_columns = {
            "filename": "TEXT NOT NULL DEFAULT ''",
            "created_at": "TEXT NOT NULL DEFAULT ''",
            "score": "INTEGER NOT NULL DEFAULT 0",
            "word_count": "INTEGER NOT NULL DEFAULT 0",
            "skills_found": "TEXT NOT NULL DEFAULT '[]'",
            "strengths": "TEXT NOT NULL DEFAULT '[]'",
            "improvements": "TEXT NOT NULL DEFAULT '[]'",
            "career_recommendations": "TEXT NOT NULL DEFAULT '[]'",
            "roadmap": "TEXT NOT NULL DEFAULT '[]'",
            "analysis_details": "TEXT NOT NULL DEFAULT '{}'"
        }

        for column_name, column_definition in required_columns.items():
            if column_name not in existing_columns:
                connection.execute(
                    f"ALTER TABLE analyses ADD COLUMN "
                    f"{column_name} {column_definition}"
                )

        connection.commit()

    finally:
        connection.close()

        
def save_analysis(result):
    """Save a resume analysis dictionary to SQLite."""
    connection = get_connection()

    try:
        cursor = connection.execute("""
            INSERT INTO analyses (
                filename,
                created_at,
                score,
                word_count,
                skills_found,
                strengths,
                improvements,
                career_recommendations,
                roadmap,
                analysis_details
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            result.get("filename", "resume.pdf"),
            result.get("created_at", ""),
            result.get("score", 0),
            result.get("word_count", 0),
            json.dumps(result.get("skills_found", [])),
            json.dumps(result.get("strengths", [])),
            json.dumps(result.get("improvements", [])),
            json.dumps(result.get("career_recommendations", [])),
            json.dumps(result.get("roadmap", [])),
            json.dumps(result.get("analysis_details", {}))
        ))

        connection.commit()
        return cursor.lastrowid

    finally:
        connection.close()

        
def _convert_row(row):
    """Convert a database row into a Python dictionary."""
    if row is None:
        return None

    result = dict(row)

    json_fields = [
        "skills_found",
        "strengths",
        "improvements",
        "career_recommendations",
        "roadmap",
        "analysis_details"
    ]

    for field in json_fields:
        if field in result:
            default = "{}" if field == "analysis_details" else "[]"
            result[field] = json.loads(result[field] or default)

    return result


def get_history():
    """Return all saved analyses, newest first."""
    connection = get_connection()

    try:
        rows = connection.execute(
            "SELECT * FROM analyses ORDER BY id DESC"
        ).fetchall()

        return [_convert_row(row) for row in rows]

    finally:
        connection.close()


def get_analysis(analysis_id):
    """Return one analysis by its ID."""
    connection = get_connection()

    try:
        row = connection.execute(
            "SELECT * FROM analyses WHERE id = ?",
            (analysis_id,)
        ).fetchone()

        return _convert_row(row)

    finally:
        connection.close()


def delete_analysis(analysis_id):
    """Delete one analysis from history."""
    connection = get_connection()

    try:
        cursor = connection.execute(
            "DELETE FROM analyses WHERE id = ?",
            (analysis_id,)
        )

        connection.commit()
        return cursor.rowcount > 0

    finally:
        connection.close()