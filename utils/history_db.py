import sqlite3
import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent

HISTORY_DIR = BASE_DIR / "history"

HISTORY_DIR.mkdir(
    exist_ok=True
)

DATABASE_PATH = HISTORY_DIR / "verifi_history.db"

def get_connection():

    return sqlite3.connect(
        DATABASE_PATH
    )

def create_history_table():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS verifications (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            created_at TEXT NOT NULL,

            input_text TEXT NOT NULL,

            verdict TEXT NOT NULL,

            confidence REAL NOT NULL,

            supported_claims INTEGER DEFAULT 0,

            contradicted_claims INTEGER DEFAULT 0,

            unverified_claims INTEGER DEFAULT 0,

            total_claims INTEGER DEFAULT 0,

            claims_data TEXT
        )
        """
    )

    connection.commit()

    connection.close()

def save_verification(
    input_text,
    overall,
    claim_results
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO verifications (
            created_at,
            input_text,
            verdict,
            confidence,
            supported_claims,
            contradicted_claims,
            unverified_claims,
            total_claims,
            claims_data
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            input_text,

            overall.get(
                "verdict",
                "UNVERIFIED"
            ),

            overall.get(
                "confidence",
                0.0
            ),

            overall.get(
                "supported_claims",
                0
            ),

            overall.get(
                "contradicted_claims",
                0
            ),

            overall.get(
                "unverified_claims",
                0
            ),

            overall.get(
                "total_claims",
                0
            ),

            json.dumps(
                claim_results,
                ensure_ascii=False
            )
        )
    )

    connection.commit()

    connection.close()

def get_history():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            created_at,
            input_text,
            verdict,
            confidence,
            supported_claims,
            contradicted_claims,
            unverified_claims,
            total_claims,
            claims_data

        FROM verifications

        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return rows

def delete_history_item(
    verification_id
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM verifications
        WHERE id = ?
        """,
        (
            verification_id,
        )
    )

    connection.commit()

    connection.close()

create_history_table()
