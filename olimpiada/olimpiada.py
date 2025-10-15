import sys
import csv
from PyQt6 import QtWidgets, uic, QtGui, QtCore
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QTableWidgetItem

class OlympiadData:

    def __init__(self):
        self.original_data = []
        self.schools = set()
        self.classes = set()

    def load_from_file(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            self.original_data = []
            self.schools = set()
            self.classes = set()

            for row in reader:
                login = row['login']
                parts = login.split('-')
                if len(parts) >= 4:
                    school = parts[2]
                    class_ = parts[3]
                    self.schools.add(school)
                    self.classes.add(class_)
                    row['extracted_school'] = school
                    row['extracted_class'] = class_
                else:
                    row['extracted_school'] = None
                    row['extracted_class'] = None

                self.original_data.append(row)

    def get_filtered_data(self, selected_school, selected_class):
        return [
            row for row in self.original_data
            if (not selected_school or row['extracted_school'] == selected_school) and
               (not selected_class or row['extracted_class'] == selected_class)
        ]


class OlympiadViewer(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("olimpiada.ui", self)

        # Настройка таблицы один раз
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['Login', 'Full Name', 'Score'])
        self.tableWidget.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)  # ← вместо setFlags в цикле!

        self.olymp_data = OlympiadData()
        self.openButton.clicked.connect(self.open_file)
        self.combo_school.currentTextChanged.connect(self.apply_filters)
        self.combo_class.currentTextChanged.connect(self.apply_filters)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv)")
        if filename:
            try:
                self.olymp_data.load_from_file(filename)
                self.setup_filters()
                self.apply_filters()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))


    def setup_filters(self):
        self.combo_school.clear()
        self.combo_school.addItem("All Schools", "")
        for school in sorted(self.olymp_data.schools):
            self.combo_school.addItem(f"School {school}", school)

        self.combo_class.clear()
        self.combo_class.addItem("All Classes", "")
        for class_ in sorted(self.olymp_data.classes):
            self.combo_class.addItem(f"Class {class_}", class_)

    def apply_filters(self):
        selected_school = self.combo_school.currentData()
        selected_class = self.combo_class.currentData()

        filtered_data = self.olymp_data.get_filtered_data(selected_school, selected_class)
        filtered_data.sort(key=lambda x: int(x['Score']), reverse=True)

        self.tableWidget.setRowCount(len(filtered_data))
        self.tableWidget.clearContents()

        place_colors = {
            1: QtGui.QColor(255, 223, 0),
            2: QtGui.QColor(192, 192, 192),
            3: QtGui.QColor(205, 127, 50)
        }

        unique_scores = []
        for row in filtered_data:
            score = int(row['Score'])
            if score not in unique_scores:
                unique_scores.append(score)

        score_to_place = {}
        for i, score in enumerate(unique_scores):
            score_to_place[score] = i + 1

        for row_idx, row_data in enumerate(filtered_data):
            login_item = QTableWidgetItem(row_data['login'])
            name_item = QTableWidgetItem(row_data['user_name'])
            score_item = QTableWidgetItem(row_data['Score'])

            self.tableWidget.setItem(row_idx, 0, login_item)
            self.tableWidget.setItem(row_idx, 1, name_item)
            self.tableWidget.setItem(row_idx, 2, score_item)
            score = int(row_data['Score'])
            place = score_to_place.get(score, 0)

            if place <= 3:
                color = place_colors[place]
                for col in range(3):
                    item = self.tableWidget.item(row_idx, col)
                    item.setBackground(color)

        self.tableWidget.resizeColumnsToContents()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = OlympiadViewer()
    window.show()
    sys.exit(app.exec())
