import sys
import random
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton


class EscapeButtonWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.button = None
        self.escape_margin = 80  # Зона убегания
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Убегающая кнопка')
        self.setGeometry(300, 300, 800, 600)

        # Создаем кнопку
        self.button = QPushButton('Попробуй нажать!', self)
        self.button.resize(120, 50)
        self.button.move(350, 275)

        # Включаем отслеживание мыши для окна
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        # Получаем позицию курсора в координатах текущего виджета
        cursor_pos = event.pos()  # <-- исправлено
        self.checkAndMoveButton(cursor_pos)
        super().mouseMoveEvent(event)

    def checkAndMoveButton(self, cursor_pos):
        # Получаем область кнопки с запасом
        button_rect = self.button.geometry()
        escape_zone = button_rect.adjusted(
            -self.escape_margin,
            -self.escape_margin,
            self.escape_margin,
            self.escape_margin
        )

        # Если курсор в зоне убегания - перемещаем кнопку
        if escape_zone.contains(cursor_pos):
            self.moveButton()

    def moveButton(self):
        # Вычисляем доступные границы для перемещения
        max_x = self.width() - self.button.width()
        max_y = self.height() - self.button.height()

        # Генерируем случайную позицию в пределах формы
        new_x = random.randint(0, max_x)
        new_y = random.randint(0, max_y)

        # Перемещаем кнопку
        self.button.move(new_x, new_y)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EscapeButtonWindow()
    window.show()
    sys.exit(app.exec())