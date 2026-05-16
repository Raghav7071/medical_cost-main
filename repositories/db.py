"""SQLite connection helper + schema/migration bootstrap. Other repositories
import :func:`connect` instead of opening their own connections."""

import os
import sqlite3

from config import DB_NAME


def connect() -> sqlite3.Connection:
    return sqlite3.connect(DB_NAME)


def db_path() -> str:
    return DB_NAME


def db_size_kb() -> float:
    return os.path.getsize(DB_NAME) / 1024 if os.path.exists(DB_NAME) else 0.0


def init_db() -> None:
    # Import inside the function to avoid a circular import (users -> db).
    from repositories.users import migrate_plaintext_passwords, seed_admin_if_missing

    conn = connect()
    c = conn.cursor()

    c.execute(
        """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            salt TEXT,
            email TEXT
        )"""
    )

    # Backfill the salt column on databases that predate it.
    c.execute("PRAGMA table_info(users)")
    cols = [row[1] for row in c.fetchall()]
    if "salt" not in cols:
        c.execute("ALTER TABLE users ADD COLUMN salt TEXT")

    c.execute(
        """CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            disease TEXT,
            country TEXT,
            total_cost REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )"""
    )

    c.execute(
        """CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )"""
    )

    conn.commit()
    migrate_plaintext_passwords(conn)
    seed_admin_if_missing(conn)
    conn.close()
