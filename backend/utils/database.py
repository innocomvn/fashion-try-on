"""
Database utilities using SQLite
"""

import sqlite3
from datetime import datetime
from typing import Optional, List, Dict
from contextlib import contextmanager

from backend.config import settings


class Database:
    """Simple SQLite database handler"""

    def __init__(self, db_path: str = None):
        self.db_path = db_path or settings.DATABASE_URL.replace("sqlite:///", "")
        self._init_db()

    def _init_db(self):
        """Initialize database and create tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tryon_tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT UNIQUE NOT NULL,
                    model_image_path TEXT NOT NULL,
                    garment_image_path TEXT NOT NULL,
                    result_image_path TEXT,
                    provider TEXT NOT NULL,
                    category TEXT NOT NULL,
                    status TEXT NOT NULL,
                    error_message TEXT,
                    denoise_steps INTEGER,
                    seed INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    processing_time REAL
                )
            """)
            conn.commit()

    @contextmanager
    def get_connection(self):
        """Get database connection context manager"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def create_task(self, task_data: Dict) -> str:
        """Create new task in database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO tryon_tasks
                (task_id, model_image_path, garment_image_path, provider,
                 category, status, denoise_steps, seed)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                task_data['task_id'],
                task_data['model_image_path'],
                task_data['garment_image_path'],
                task_data['provider'],
                task_data['category'],
                task_data['status'],
                task_data.get('denoise_steps', 30),
                task_data.get('seed', 42)
            ))
            conn.commit()
            return task_data['task_id']

    def get_task(self, task_id: str) -> Optional[Dict]:
        """Get task by ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tryon_tasks WHERE task_id = ?", (task_id,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None

    def update_task(self, task_id: str, updates: Dict):
        """Update task in database"""
        updates['updated_at'] = datetime.now().isoformat()

        set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values()) + [task_id]

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"UPDATE tryon_tasks SET {set_clause} WHERE task_id = ?",
                values
            )
            conn.commit()

    def list_tasks(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """List all tasks"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM tryon_tasks ORDER BY created_at DESC LIMIT ? OFFSET ?",
                (limit, offset)
            )
            return [dict(row) for row in cursor.fetchall()]

    def delete_task(self, task_id: str):
        """Delete task from database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tryon_tasks WHERE task_id = ?", (task_id,))
            conn.commit()


# Global database instance
db = Database()
