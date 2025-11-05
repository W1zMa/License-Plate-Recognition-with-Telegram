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
        timecode REAL,
        count INTEGER,
        file_path TEXT,
        added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_number ON cars(number)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_user ON cars(count)")
    conn.commit()
    conn.close()

def save_plate(number: str, count: int, file_path: Optional[str]=None, accuracy: Optional[float]=None, timecode: Optional[float]=None):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO cars (number, count, file_path, accuracy, timecode) VALUES (?, ?, ?, ?, ?)",
                (number, count, file_path, accuracy, timecode))
    conn.commit()
    conn.close()
    
def get_count(number: str) -> int:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM cars WHERE number = ? AND count > 0", (number,))
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

def reset_count(number: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE cars SET count = 0 WHERE number = ?", (number,))
    conn.commit()
    conn.close()

  