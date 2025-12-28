import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "booktrack.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, google_id TEXT NOT NULL, title TEXT NOT NULL, authors TEXT, thumbnail TEXT, description TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, status TEXT DEFAULT 'to_read', UNIQUE(user_id, google_id));")

    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL UNIQUE, password_hash TEXT NOT NULL);")

    conn.commit()
    conn.close()