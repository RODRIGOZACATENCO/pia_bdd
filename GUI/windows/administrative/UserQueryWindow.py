from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from app.bar_db import DB_GLOBAL
import os


def load_stylesheet(widget, css_file_name):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        resources_dir = os.path.join(current_dir, '..', '..', 'resources')
        file_path = os.path.join(resources_dir, css_file_name)

        with open(file_path, 'r', encoding='utf-8') as f:
            style = f.read()
            widget.setStyleSheet(style)
    except Exception as e:
        print(f"Error loading stylesheet {css_file_name}: {e}")


class UserQueryWindow(QWidget):
    def __init__(self, go_back_callback):
        super().__init__()
        self.setObjectName("QueryWindow")
        self.go_back_callback = go_back_callback

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)

        top_layout = QHBoxLayout()
        back_button = QPushButton("Volver")
        back_button.setObjectName("back_button")
        back_button.clicked.connect(self.go_back_callback)
        top_layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignLeft)

        main_layout.addLayout(top_layout)

        main_layout.addWidget(QLabel("Consulta de Usuarios del Sistema"))

        self.results_table = QTableWidget()
        self.setup_table()
        main_layout.addWidget(self.results_table)

        load_stylesheet(self, "query_windows.css")
        self.load_data()

    def setup_table(self):
        self.results_table.setSortingEnabled(True)
        self.results_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.results_table.setAlternatingRowColors(True)
        self.results_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.results_table.verticalHeader().setVisible(False)

    def load_data(self):
        try:
            results = DB_GLOBAL.get_user_accounts_view()
            headers = ["ID Usuario", "Nombre Usuario", "Empleado", "Puesto"]
            self.populate_table(headers, results)

            if results:
                self.results_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
                self.results_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
                self.results_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
                self.results_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar la lista de usuarios: {e}")

    def populate_table(self, headers, data):
        self.results_table.setSortingEnabled(False)
        self.results_table.setRowCount(0)
        self.results_table.setColumnCount(len(headers))
        self.results_table.setHorizontalHeaderLabels(headers)

        if not data:
            self.results_table.setSortingEnabled(True)
            return

        self.results_table.setRowCount(len(data))
        for row_num, row_data in enumerate(data):
            for col_num, item in enumerate(row_data):
                table_item = QTableWidgetItem(str(item))
                self.results_table.setItem(row_num, col_num, table_item)

        self.results_table.resizeRowsToContents()
        self.results_table.setSortingEnabled(True)