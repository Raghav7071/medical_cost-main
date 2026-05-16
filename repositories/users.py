"""User accounts: hashing, registration, verification, and one-shot migration
of legacy plaintext passwords."""

import hashlib
import os
import sqlite3

from repositories.db import connect


def _hash_password(password: str, salt: str) -> str:
    return hashlib.sha256((salt + password).encode("utf-8")).hexdigest()


def _looks_hashed(value: str) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(c in "0123456789abcdef" for c in value)


def migrate_plaintext_passwords(conn: sqlite3.Connection) -> None:
    """Rehash any rows whose password is still plaintext (no salt, or stored
    value isn't a 64-char hex digest)."""
    c = conn.cursor()
    c.execute("SELECT id, password, salt FROM users")
    for user_id, password, salt in c.fetchall():
        if salt and _looks_hashed(password):
            continue
        new_salt = os.urandom(16).hex()
        new_hash = _hash_password(password or "", new_salt)
        c.execute("UPDATE users SET password=?, salt=? WHERE id=?", (new_hash, new_salt, user_id))
    conn.commit()


def seed_admin_if_missing(conn: sqlite3.Connection) -> None:
    """Ensure a default `admin` user exists. Replaces the old hardcoded
    admin/admin123 bypass in the entry point — the credential now lives in
    the DB and can (and should) be changed."""
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username=?", ("admin",))
    if c.fetchone():
        return
    salt = os.urandom(16).hex()
    c.execute(
        "INSERT INTO users (username, password, salt, email) VALUES (?, ?, ?, ?)",
        ("admin", _hash_password("admin123", salt), salt, "admin@local"),
    )
    conn.commit()


def add_user(username: str, password: str, email: str) -> bool:
    if not username or not password:
        return False
    conn = connect()
    c = conn.cursor()
    try:
        salt = os.urandom(16).hex()
        c.execute(
            "INSERT INTO users (username, password, salt, email) VALUES (?, ?, ?, ?)",
            (username, _hash_password(password, salt), salt, email),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def verify_user(username: str, password: str) -> int | None:
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT id, password, salt FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    user_id, stored_hash, salt = row
    if not salt:
        return None
    return user_id if _hash_password(password, salt) == stored_hash else None
