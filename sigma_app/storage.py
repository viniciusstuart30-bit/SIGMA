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
            CREATE TABLE IF NOT EXISTS leaders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                leader_name TEXT NOT NULL,
                sector TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(leader_name)
            )
            """
        )
        connection.commit()


def get_leader_by_id(database_path, leader_id):
    if leader_id is None:
        return None
    with get_connection(database_path) as connection:
        return connection.execute(
            "SELECT id, leader_name, sector, created_at FROM leaders WHERE id = ?",
            (leader_id,),
        ).fetchone()


def get_leader_by_name(database_path, leader_name):
    with get_connection(database_path) as connection:
        return connection.execute(
            "SELECT id, leader_name, sector, password_hash, created_at FROM leaders WHERE leader_name = ?",
            (leader_name,),
        ).fetchone()


def create_leader(database_path, leader_name, sector, password):
    password_hash = generate_password_hash(password)
    with get_connection(database_path) as connection:
        cursor = connection.execute(
            "INSERT INTO leaders (leader_name, sector, password_hash) VALUES (?, ?, ?)",
            (leader_name, sector, password_hash),
        )
        connection.commit()
        return get_leader_by_id(database_path, cursor.lastrowid)


def verify_leader(database_path, leader_name, password):
    leader = get_leader_by_name(database_path, leader_name)
    if leader is None:
        return None
    if not check_password_hash(leader["password_hash"], password):
        return None
    return leader