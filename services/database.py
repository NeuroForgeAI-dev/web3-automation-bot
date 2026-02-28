"""SQLite database for bookings and leads."""
import sqlite3
from datetime import datetime
from pathlib import Path


class Database:
    def __init__(self, db_path: str = "data/bot.db"):
        Path("data").mkdir(exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._init_tables()

    def _init_tables(self):
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                details TEXT,
                status TEXT DEFAULT 'pending',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                message TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
        """)
        self.conn.commit()

    def create_booking(self, user_id: int, details: str):
        self.conn.execute("INSERT INTO bookings (user_id, details) VALUES (?, ?)", (user_id, details))
        self.conn.commit()

    def save_lead(self, user_id: int, username: str, message: str):
        self.conn.execute("INSERT INTO leads (user_id, username, message) VALUES (?, ?, ?)",
                         (user_id, username or "", message))
        self.conn.commit()

    def get_stats(self) -> dict:
        bookings = self.conn.execute("SELECT COUNT(*) FROM bookings").fetchone()[0]
        leads = self.conn.execute("SELECT COUNT(*) FROM leads").fetchone()[0]
        return {"total_bookings": bookings, "total_leads": leads}
