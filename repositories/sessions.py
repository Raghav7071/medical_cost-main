"""Persistent session tokens. A token is stashed in the URL via Streamlit's
query params so login survives a browser reload."""

import secrets

from repositories.db import connect


def create_session(user_id: int) -> str:
    """Generate a fresh token for a user and persist it."""
    token = secrets.token_urlsafe(32)
    conn = connect()
    try:
        conn.execute(
            "INSERT INTO sessions (token, user_id) VALUES (?, ?)", (token, user_id)
        )
        conn.commit()
    finally:
        conn.close()
    return token


def resolve_session(token: str) -> tuple[int, str] | None:
    """Return (user_id, username) for a valid token, or None if not found."""
    if not token:
        return None
    conn = connect()
    try:
        c = conn.cursor()
        c.execute(
            "SELECT u.id, u.username FROM sessions s "
            "JOIN users u ON u.id = s.user_id WHERE s.token = ?",
            (token,),
        )
        row = c.fetchone()
    finally:
        conn.close()
    if not row:
        return None
    return int(row[0]), str(row[1])


def delete_session(token: str) -> None:
    if not token:
        return
    conn = connect()
    try:
        conn.execute("DELETE FROM sessions WHERE token = ?", (token,))
        conn.commit()
    finally:
        conn.close()
