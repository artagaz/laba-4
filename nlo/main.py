import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QKeyEvent


class UFOController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ufo_speed = 30
        self.initUI()

    def initUI(self):
        self.setWindowTitle('nlo')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #0a0a2a;")

        # create nlo
        self.ufo_label = QLabel(self)
        self.load_ufo_image()

        # set start pos
        self.ufo_x = 400
        self.ufo_y = 300
        self.update_ufo_position()

        self.keys_pressed = {
            Qt.Key.Key_Left: False,
            Qt.Key.Key_Right: False,
            Qt.Key.Key_Up: False,
            Qt.Key.Key_Down: False
        }

    def load_ufo_image(self):
        try:
            if os.path.exists("111.png"):
                pixmap = QPixmap("111.png")
            else:
                # simple ufo
                pixmap = QPixmap(80, 40)
                pixmap.fill(Qt.GlobalColor.transparent)

                from PyQt6.QtGui import QPainter, QBrush, QColor
                painter = QPainter(pixmap)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)

                painter.setBrush(QBrush(QColor(200, 200, 255)))
                painter.drawEllipse(0, 10, 80, 20)
                painter.setBrush(QBrush(QColor(100, 100, 200)))
                painter.drawEllipse(20, 0, 40, 20)
                painter.end()

            self.ufo_label.setPixmap(pixmap)
            self.ufo_label.resize(pixmap.width(), pixmap.height())

        except Exception as e:
            print(f"Ошибка загрузки изображения: {e}")

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() in (Qt.Key.Key_Left, Qt.Key.Key_Right, Qt.Key.Key_Up, Qt.Key.Key_Down):
            self.move_ufo(event.key())
            event.accept()
        else:
            super().keyPressEvent(event)

    def move_ufo(self, key):
        if key == Qt.Key.Key_Left:
            self.ufo_x -= self.ufo_speed
        elif key == Qt.Key.Key_Right:
            self.ufo_x += self.ufo_speed
        elif key == Qt.Key.Key_Up:
            self.ufo_y -= self.ufo_speed
        elif key == Qt.Key.Key_Down:
            self.ufo_y += self.ufo_speed

        self.handle_boundaries()
        self.update_ufo_position()

    def keyReleaseEvent(self, event: QKeyEvent):
        if event.key() in self.keys_pressed:
            self.keys_pressed[event.key()] = False
            event.accept()
        else:
            super().keyReleaseEvent(event)

    def handle_boundaries(self):
        ufo_width = self.ufo_label.width()
        ufo_height = self.ufo_label.height()
        window_width = self.width()
        window_height = self.height()

        # right left
        if self.ufo_x > window_width:
            self.ufo_x = -ufo_width
        elif self.ufo_x < -ufo_width:
            self.ufo_x = window_width

        # bottom up
        if self.ufo_y > window_height:
            self.ufo_y = -ufo_height
        elif self.ufo_y < -ufo_height:
            self.ufo_y = window_height

    def update_ufo_position(self):
        self.ufo_label.move(self.ufo_x, self.ufo_y)


def main():
    app = QApplication(sys.argv)
    controller = UFOController()
    controller.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
