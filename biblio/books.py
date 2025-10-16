import sqlite3
import os

def create_books_table():
    try:
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER NOT NULL,
                genre TEXT NOT NULL,
                image_path TEXT
            )
        ''')
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False

def get_all_books():
    try:
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books')
        books = cursor.fetchall()
        conn.close()
        return books if books else []
    except Exception:
        return []

def search_books_by_author(author):
    try:
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM books WHERE author LIKE ?',
            (f'%{author}%',)
        )
        books = cursor.fetchall()
        conn.close()
        return books if books else []
    except Exception:
        return []

def search_books_by_title(title):
    try:
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM books WHERE title LIKE ?',
            (f'%{title}%',)
        )
        books = cursor.fetchall()
        conn.close()
        return books if books else []
    except Exception:
        return []

def add_book(title, author, year, genre, image_path=None):
    try:
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO books (title, author, year, genre, image_path)
               VALUES (?, ?, ?, ?, ?)''',
            (title, author, year, genre, image_path)
        )
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False

def update_book(book_id, title, author, year, genre, image_path=None):
    try:
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute(
            '''UPDATE books SET title=?, author=?, year=?, genre=?, image_path=?
               WHERE id=?''',
            (title, author, year, genre, image_path, book_id)
        )
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False

def delete_book(book_id):
    try:
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM books WHERE id=?', (book_id,))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False

def get_book_by_id(book_id):
    try:
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
        book = cursor.fetchone()
        conn.close()
        return book
    except Exception:
        return None