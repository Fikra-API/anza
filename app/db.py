import os
import sqlite3
from datetime import datetime, timezone

DATABASE_PATH = os.getenv("DATABASE_PATH", "anza.db")


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)


def create_user(email: str, password_hash: str, salt: str) -> int:
    created_at = datetime.now(timezone.utc).isoformat()
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (email, password_hash, salt, created_at) VALUES (?, ?, ?, ?)",
            (email, password_hash, salt, created_at),
        )
        return cursor.lastrowid


def get_user_by_email(email: str) -> sqlite3.Row | None:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        return cursor.fetchone()


def get_user_by_id(user_id: int) -> sqlite3.Row | None:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()
