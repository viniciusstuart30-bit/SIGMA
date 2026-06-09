import sqlite3
from pathlib import Path

from werkzeug.security import check_password_hash, generate_password_hash


def get_connection(database_path):
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database(database_path):
    Path(database_path).parent.mkdir(parents=True, exist_ok=True)
    with get_connection(database_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.commit()


def get_user_by_id(database_path, user_id):
    if user_id is None:
        return None
    with get_connection(database_path) as connection:
        return connection.execute(
            "SELECT id, username, created_at FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()


def get_user_by_username(database_path, username):
    with get_connection(database_path) as connection:
        return connection.execute(
            "SELECT id, username, password_hash, created_at FROM users WHERE username = ?",
            (username,),
        ).fetchone()


def create_user(database_path, username, password):
    password_hash = generate_password_hash(password)
    with get_connection(database_path) as connection:
        cursor = connection.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash),
        )
        connection.commit()
        return get_user_by_id(database_path, cursor.lastrowid)


def verify_user(database_path, username, password):
    user = get_user_by_username(database_path, username)
    if user is None:
        return None
    if not check_password_hash(user["password_hash"], password):
        return None
    return user