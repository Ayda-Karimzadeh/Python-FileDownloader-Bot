import sqlite3
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER UNIQUE,
        first_name TEXT ,
        last_name TEXT,
        phone TEXT UNIQUE,
        email TEXT UNIQUE           
    )
    """)

    conn.commit()
    conn.close()