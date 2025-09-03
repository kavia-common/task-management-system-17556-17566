from __future__ import annotations
import os
import sqlite3
from typing import Any, Dict, List, Optional

DB_PATH = os.environ.get("SQLITE_DB_PATH", os.path.join(os.path.dirname(__file__), "..", "todo.db"))

def _get_connection() -> sqlite3.Connection:
    """Create and return a SQLite connection with row factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    """Initialize the SQLite database and create tables if not exist."""
    conn = _get_connection()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        conn.commit()
    finally:
        conn.close()

# PUBLIC_INTERFACE
def create_task(title: str, completed: bool = False) -> Dict[str, Any]:
    """Create a new task in the database."""
    conn = _get_connection()
    try:
        cur = conn.execute(
            "INSERT INTO tasks (title, completed) VALUES (?, ?)",
            (title, 1 if completed else 0),
        )
        conn.commit()
        task_id = cur.lastrowid
        return get_task(task_id)  # type: ignore[return-value]
    finally:
        conn.close()

# PUBLIC_INTERFACE
def list_tasks() -> List[Dict[str, Any]]:
    """Return all tasks."""
    conn = _get_connection()
    try:
        cur = conn.execute("SELECT id, title, completed FROM tasks ORDER BY id DESC")
        rows = cur.fetchall()
        return [
            {"id": row["id"], "title": row["title"], "completed": bool(row["completed"])}
            for row in rows
        ]
    finally:
        conn.close()

# PUBLIC_INTERFACE
def get_task(task_id: int) -> Optional[Dict[str, Any]]:
    """Return a single task by id or None if not found."""
    conn = _get_connection()
    try:
        cur = conn.execute("SELECT id, title, completed FROM tasks WHERE id = ?", (task_id,))
        row = cur.fetchone()
        if row is None:
            return None
        return {"id": row["id"], "title": row["title"], "completed": bool(row["completed"])}
    finally:
        conn.close()

# PUBLIC_INTERFACE
def update_task(task_id: int, title: Optional[str] = None, completed: Optional[bool] = None) -> Optional[Dict[str, Any]]:
    """Update a task's title and/or completed status. Returns updated task or None."""
    existing = get_task(task_id)
    if existing is None:
        return None

    new_title = title if title is not None else existing["title"]
    new_completed = completed if completed is not None else existing["completed"]

    conn = _get_connection()
    try:
        conn.execute(
            "UPDATE tasks SET title = ?, completed = ? WHERE id = ?",
            (new_title, 1 if new_completed else 0, task_id),
        )
        conn.commit()
        return get_task(task_id)
    finally:
        conn.close()

# PUBLIC_INTERFACE
def delete_task(task_id: int) -> bool:
    """Delete a task. Returns True if a row was deleted, else False."""
    conn = _get_connection()
    try:
        cur = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        return cur.rowcount > 0
    finally:
        conn.close()
