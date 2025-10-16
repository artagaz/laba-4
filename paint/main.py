import sys
import random
from PyQt6 import QtWidgets, QtGui, QtCore


class DrawingWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.shapes = []
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.setMinimumSize(400, 300)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.add_shape("circle", event.pos())
        elif event.button() == QtCore.Qt.MouseButton.RightButton:
            self.add_shape("square", event.pos())
        event.accept()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Space:
            cursor_pos = self.mapFromGlobal(QtGui.QCursor.pos())
            if self.rect().contains(cursor_pos):
                self.add_shape("triangle", cursor_pos)
            event.accept()
        else:
            super().keyPressEvent(event) # another keys

    def add_shape(self, shape_type, position):
        color = QtGui.QColor(
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )
        size = random.randint(20, 60)

        self.shapes.append({
            'type': shape_type,
            'position': position,
            'color': color,
            'size': size
        })
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for shape in self.shapes:
            painter.setBrush(shape['color'])
            painter.setPen(shape['color'])

            x = shape['position'].x() - shape['size'] // 2
            y = shape['position'].y() - shape['size'] // 2
            size = shape['size']

            if shape['type'] == "circle":
                painter.drawEllipse(x, y, size, size)
            elif shape['type'] == "square":
                painter.drawRect(x, y, size, size)
            elif shape['type'] == "triangle":
                points = [
                    QtCore.QPoint(x + size // 2, y),
                    QtCore.QPoint(x, y + size),
                    QtCore.QPoint(x + size, y + size)
                ]
                painter.drawPolygon(QtGui.QPolygon(points))


class ShapeDrawer(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shape Drawer")
        self.setGeometry(100, 100, 800, 600)

        self.drawing_widget = DrawingWidget()
        self.setCentralWidget(self.drawing_widget)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ShapeDrawer()
    window.show()
    sys.exit(app.exec())