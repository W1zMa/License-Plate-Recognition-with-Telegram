import sqlite3
from typing import List, Optional

DB = 'data/db.sqlite3'

def get_conn():
    conn = sqlite3.connect(DB, timeout=30)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        number TEXT NOT NULL,
        accuracy REAL,
        user_id INTEGER,
        file_path TEXT,
        added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_number ON cars(number)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_user ON cars(user_id)")
    conn.commit()
    conn.close()

def save_plate(number: str, user_id: int, file_path: Optional[str]=None, accuracy: Optional[float]=None):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO cars (number, user_id, file_path, accuracy) VALUES (?, ?, ?, ?)",
                (number, user_id, file_path, accuracy))
    conn.commit()
    conn.close()

def get_count(number: str, user_id: Optional[int]=None) -> int:
    conn = get_conn()
    cur = conn.cursor()
    if user_id is None:
        cur.execute("SELECT COUNT(*) FROM cars WHERE number = ?", (number,))
    else:
        cur.execute("SELECT COUNT(*) FROM cars WHERE number = ? AND user_id = ?", (number, user_id))
    count = cur.fetchone()[0]
    conn.close()
    return count

def get_info(numbers_input):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM cars WHERE number = ?", (numbers_input,))
    rows = cur.fetchall()
    conn.close()
    return rows


def reset_count(number: str, user_id: Optional[int]=None):
    conn = get_conn()
    cur = conn.cursor()
    if user_id is None:
        cur.execute("DELETE FROM cars WHERE number = ?", (number,))
    else:
        cur.execute("DELETE FROM cars WHERE number = ? AND user_id = ?", (number, user_id))
    conn.commit()
    conn.close()

#def get_history(number: str, limit: int=50) -> List[sqlite3.Row]:
#   conn = get_conn()
#   cur = conn.cursor()
#   cur.execute(f"SELECT * FROM cars WHERE number = ? ORDER BY added_at DESC LIMIT {limit}", (number,))
#   rows = cur.fetchall()
#    conn.close()
#    return rows    