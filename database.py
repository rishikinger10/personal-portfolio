import sqlite3
import os

# keeping the db next to the code so it's easy to nuke and reseed
DB_PATH = os.path.join(os.path.dirname(__file__), "portfolio.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # fk's are off by default in sqlite which bit me once already
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS profile (
        id INTEGER PRIMARY KEY,
        full_name TEXT NOT NULL,
        headline TEXT,
        tagline TEXT,
        email TEXT,
        phone TEXT,
        location TEXT,
        about TEXT,
        education TEXT,
        cgpa TEXT
    );

    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        summary TEXT,
        stack TEXT,          -- comma separated, didn't feel like a join table
        highlights TEXT,     -- one bullet per line
        sort_order INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        items TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS experience (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL,
        org TEXT NOT NULL,
        period TEXT,
        bullets TEXT
    );

    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_name TEXT,
        sender_email TEXT,
        body TEXT,
        received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("tables created ->", DB_PATH)
