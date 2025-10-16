import sqlite3
import hashlib


def create_user_table():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username, password):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    password_hash = hash_password(password)

    try:
        cursor.execute(
            'INSERT INTO users (username, password_hash) VALUES (?, ?)',
            (username, password_hash)
        )
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    finally:
        conn.close()

    return success


def verify_user(username, password):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    cursor.execute(
        'SELECT password_hash FROM users WHERE username = ?',
        (username,)
    )
    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0] == hash_password(password)
    return False