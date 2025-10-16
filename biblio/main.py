import sys
from PyQt6.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, QFileDialog, QTableWidgetItem
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6 import uic

from auth import create_user_table, register_user, verify_user
from books import *


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/login.ui', self)

        self.login_btn.clicked.connect(self.login)
        self.register_btn.clicked.connect(self.register)

        create_user_table()
        self.main_window = None

    def login(self):
        username = self.login_username.text()
        password = self.login_password.text()

        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return

        if verify_user(username, password):
            self.accept()
            self.main_window = MainWindow()
            self.main_window.show()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")

    def register(self):
        username = self.reg_username.text()
        password = self.reg_password.text()
        confirm = self.reg_confirm.text()

        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return

        if password != confirm:
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают")
            return

        if register_user(username, password):
            QMessageBox.information(self, "Успех", "Регистрация завершена")
            self.tabs.setCurrentIndex(0)
            self.login_username.setText(username)
            self.reg_username.clear()
            self.reg_password.clear()
            self.reg_confirm.clear()
        else:
            QMessageBox.warning(self, "Ошибка", "Пользователь уже существует")


class BookDialog(QDialog):
    def __init__(self, parent=None, book=None):
        super().__init__(parent)
        uic.loadUi('ui/book_dialog.ui', self)

        self.book = book
        if book:
            self.setWindowTitle("Редактировать книгу")
            self.title_edit.setText(book[1])
            self.author_edit.setText(book[2])
            self.year_spin.setValue(book[3])
            self.genre_edit.setText(book[4])
            if book[5]:
                self.image_path_edit.setText(book[5])

        self.browse_btn.clicked.connect(self.browse_image)
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

    def browse_image(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Выберите изображение", "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if filename:
            self.image_path_edit.setText(filename)

    def get_data(self):
        return {
            'title': self.title_edit.text(),
            'author': self.author_edit.text(),
            'year': self.year_spin.value(),
            'genre': self.genre_edit.text(),
            'image_path': self.image_path_edit.text() or None
        }


class BookDetailDialog(QDialog):
    def __init__(self, book, parent=None):
        super().__init__(parent)
        uic.loadUi('ui/book_detail.ui', self)

        self.book = book
        self.close_btn.clicked.connect(self.accept)
        self.load_data()

    def load_data(self):
        self.title_label.setText(self.book[1])
        self.author_label.setText(self.book[2])
        self.year_label.setText(str(self.book[3]))
        self.genre_label.setText(self.book[4])

        if self.book[5] and os.path.exists(self.book[5]):
            pixmap = QPixmap(self.book[5])
        else:
            # if not picture loaded
            default_image_path = "images/default_book.jpg"
            if os.path.exists(default_image_path):
                pixmap = QPixmap(default_image_path)
            else:
                # if no def picture -> set color
                pixmap = QPixmap(200, 300)
                pixmap.fill(Qt.GlobalColor.lightGray)

        self.image_label.setPixmap(
            pixmap.scaled(200, 300, Qt.AspectRatioMode.KeepAspectRatio,
                          Qt.TransformationMode.SmoothTransformation)
        )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/main_window.ui', self)

        self.books_table.horizontalHeader().setStretchLastSection(True)
        self.books_table.setSelectionBehavior(self.books_table.SelectionBehavior.SelectRows)

        self.search_author_btn.clicked.connect(self.search_by_author)
        self.search_title_btn.clicked.connect(self.search_by_title)
        self.show_all_btn.clicked.connect(lambda: self.load_books(None))
        self.add_btn.clicked.connect(self.add_book)
        self.edit_btn.clicked.connect(self.edit_book)
        self.delete_btn.clicked.connect(self.delete_book)
        self.view_btn.clicked.connect(self.view_book)

        self.load_books(None)



    def load_books(self, books):
        if books is None or books is False:
            books = get_all_books()

        if not isinstance(books, (list, tuple)):
            books = []

        self.books_table.setRowCount(len(books))
        for row, book in enumerate(books):
            if len(book) >= 5:
                for col, value in enumerate(book[:5]):
                    item = QTableWidgetItem(str(value) if value is not None else "")
                    self.books_table.setItem(row, col, item)

    def search_by_author(self):
        query = self.search_edit.text()
        if query:
            books = search_books_by_author(query)
            self.load_books(books)

    def search_by_title(self):
        query = self.search_edit.text()
        if query:
            books = search_books_by_title(query)
            self.load_books(books)

    def add_book(self):
        dialog = BookDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            add_book(**data)
            self.load_books(None)

    def edit_book(self):
        selected = self.books_table.currentRow()
        if selected >= 0:
            book_id = int(self.books_table.item(selected, 0).text())
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
            book = cursor.fetchone()
            conn.close()

            if book:
                dialog = BookDialog(self, book)
                if dialog.exec():
                    data = dialog.get_data()
                    update_book(book_id, **data)
                    self.load_books(None)

    def delete_book(self):
        selected = self.books_table.currentRow()
        if selected >= 0:
            book_id = int(self.books_table.item(selected, 0).text())
            book = get_book_by_id(book_id)
            if book:
                reply = QMessageBox.question(
                    self, 'Подтверждение',
                    f'Вы уверены, что хотите удалить книгу "{book[1]}" (ID: {book[0]})?',
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if reply == QMessageBox.StandardButton.Yes:
                    delete_book(book_id)
                    self.load_books(None)
            else:
                QMessageBox.warning(self, "Ошибка", "Книга не найдена.")

    def view_book(self):
        selected = self.books_table.currentRow()
        if selected >= 0:
            book_id = int(self.books_table.item(selected, 0).text())
            book = get_book_by_id(book_id)
            if book:
                dialog = BookDetailDialog(book, self)
                dialog.exec()
            else:
                QMessageBox.warning(self, "Ошибка", "Книга не найдена.")


def main():
    app = QApplication(sys.argv)

    create_books_table()

    login_dialog = LoginDialog()

    if login_dialog.exec():
        sys.exit(app.exec())
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()