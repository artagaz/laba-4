import sys
import sqlite3
from contextlib import contextmanager
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTableWidgetItem,
                             QPushButton, QMessageBox, QDialog, QHeaderView)
from PyQt6.QtCore import Qt
from PyQt6 import uic

DB_PATH = "films_db.sqlite"


@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    except Exception:
        conn.rollback()  # Rollback on error
        raise
    else:
        conn.commit()  # Commit on success
    finally:
        conn.close()


class FilmDialog(QDialog):
    def __init__(self, parent=None, film=None, genres=None):
        super().__init__(parent)
        uic.loadUi('dop.ui', self)

        self.film = film
        self.genres = genres or []

        for genre_id, genre_name in self.genres:
            self.genre_combo.addItem(genre_name, genre_id)

        if film:
            self.setWindowTitle("Редактировать фильм")
            self.fill_form()

        self.ok_button.clicked.connect(self.validate_and_accept)
        self.cancel_button.clicked.connect(self.reject)

    def fill_form(self):
        if self.film:
            self.title_edit.setText(self.film[1])  # title
            self.year_spin.setValue(self.film[2])  # year
            self.duration_spin.setValue(self.film[4])  # duration

            # Set genre
            genre_id = self.film[3]  # genre
            index = self.genre_combo.findData(genre_id)
            if index >= 0:
                self.genre_combo.setCurrentIndex(index)

    def validate_and_accept(self):
        title = self.title_edit.text().strip()
        year = self.year_spin.value()
        duration = self.duration_spin.value()
        genre_id = self.genre_combo.currentData()  # Get selected genre ID

        if not title:
            QMessageBox.warning(self, "Ошибка", "Название фильма не может быть пустым")
            return

        if year > 2025:
            QMessageBox.warning(self, "Ошибка", "Год выпуска не может быть в будущем")
            return

        if duration <= 0:
            QMessageBox.warning(self, "Ошибка", "Длительность должна быть положительной")
            return

        if duration > 1000:
            QMessageBox.warning(self, "Ошибка", "Длительность слишком большая")
            return

        if not isinstance(genre_id, int) or genre_id <= 0:
            QMessageBox.warning(self, "Ошибка", "Выберите корректный жанр")
            return

        self.accept()

    def get_data(self):
        return {
            'title': self.title_edit.text().strip(),
            'year': self.year_spin.value(),
            'duration': self.duration_spin.value(),
            'genre_id': self.genre_combo.currentData()  # Get selected genre ID
        }


class FilmsManager(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.setup_ui()
        self.load_films()

    def setup_ui(self):
        self.add_button.clicked.connect(self.add_film)
        self.edit_button.clicked.connect(self.edit_film)
        self.delete_button.clicked.connect(self.delete_film)

        # table setup
        self.films_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.films_table.setSelectionBehavior(self.films_table.SelectionBehavior.SelectRows)

    def _fill_table(self, films_data, genres_map):
        self.films_table.setRowCount(len(films_data))
        self.films_table.setColumnCount(5)
        display_headers = ['ID', 'Название', 'Год', 'Жанр', 'Длительность (мин)']
        self.films_table.setHorizontalHeaderLabels(display_headers)

        for row, (film_id, title, year, duration, genre_id) in enumerate(films_data):
            genre_name = genres_map.get(genre_id, "Неизвестно")
            # no null
            title = str(title) if title is not None else ""
            year = str(year) if year is not None else ""
            duration = str(duration) if duration is not None else ""
            genre_name = str(genre_name) if genre_name is not None else ""

            self.films_table.setItem(row, 0, QTableWidgetItem(str(film_id)))
            self.films_table.setItem(row, 1, QTableWidgetItem(title))
            self.films_table.setItem(row, 2, QTableWidgetItem(year))
            self.films_table.setItem(row, 3, QTableWidgetItem(genre_name))
            self.films_table.setItem(row, 4, QTableWidgetItem(duration))

    def load_films(self):
        try:
            # context manager
            with get_db_connection() as conn:
                cursor = conn.cursor()
                # sort by title
                cursor.execute("SELECT f.id, f.title, f.year, f.duration, f.genre FROM films f ORDER BY f.title")
                films = cursor.fetchall()
                # connect genre id to title
                cursor.execute("SELECT id, title FROM genres")
                genres = {g[0]: g[1] for g in cursor.fetchall()}

            # fill table with loaded data
            self._fill_table(films, genres)

        except sqlite3.Error as e:
            print(f"SQL ошибка: {e}")
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки данных: {e}")

    def add_film(self):
        genres = self.get_genres()
        dialog = FilmDialog(self, genres=genres)
        if dialog.exec():
            data = dialog.get_data()
            try:
                with get_db_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO films (title, year, duration, genre) VALUES (?, ?, ?, ?)",
                        (data['title'], data['year'], data['duration'], data['genre_id'])
                    )
                # reload table
                self.load_films()
                QMessageBox.information(self, "Успех", "Фильм успешно добавлен")
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка добавления фильма: {e}")

    def edit_film(self):
        selected_row = self.films_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите фильм для редактирования")
            return

        try:
            film_id = int(self.films_table.item(selected_row, 0).text())
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM films WHERE id = ?", (film_id,))
                film = cursor.fetchone()

            if film:
                genres = self.get_genres()
                dialog = FilmDialog(self, film=film, genres=genres)

                if dialog.exec():
                    data = dialog.get_data()
                    with get_db_connection() as conn:
                        cursor = conn.cursor()
                        cursor.execute(
                            "UPDATE films SET title=?, year=?, duration=?, genre=? WHERE id=?",
                            (data['title'], data['year'], data['duration'], data['genre_id'], film_id)
                        )
                    self.load_films()
                    QMessageBox.information(self, "Успех", "Фильм успешно обновлен")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка редактирования: {e}")

    def delete_film(self):
        selected_row = self.films_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите фильм для удаления")
            return

        try:
            film_id = int(self.films_table.item(selected_row, 0).text())
            film_title = self.films_table.item(selected_row, 1).text()

            reply = QMessageBox.question(
                self, 'Подтверждение удаления',
                f'Вы уверены, что хотите удалить фильм "{film_title}"?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                with get_db_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM films WHERE id = ?", (film_id,))
                self.load_films()
                QMessageBox.information(self, "Успех", "Фильм успешно удален")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка удаления: {e}")

    def get_genres(self):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, title FROM genres")
                return cursor.fetchall()
        except Exception as e:
            print(f"Ошибка получения жанров: {e}")
            return []


def main():
    app = QApplication(sys.argv)
    window = FilmsManager()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
