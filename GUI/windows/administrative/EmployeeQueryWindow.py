from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout
)
from PySide6.QtCore import Qt
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


class NumericTableWidgetItem(QTableWidgetItem):
    def __init__(self, value, is_float=False):
        super().__init__(str(value))
        self.value = value
        self.is_float = is_float

    def __lt__(self, other):
        try:
            # Forcing numeric comparison for sorting
            if self.is_float:
                return float(self.value) < float(other.value)
            return int(self.value) < int(other.value)
        except ValueError:
            # Fallback to string comparison if not a valid number
            return super().__lt__(other)


class EmployeeQueryWindow(QWidget):
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

        self.edit_toggle_button = QPushButton("Habilitar Edición")
        self.edit_toggle_button.setObjectName("edit_toggle_button")
        self.edit_toggle_button.setEnabled(False)
        self.edit_toggle_button.setToolTip("La edición está deshabilitada para esta vista.")

        top_layout.addStretch()
        top_layout.addWidget(self.edit_toggle_button)
        main_layout.addLayout(top_layout)

        main_layout.addWidget(QLabel("Consultas de Empleados"))

        buttons_layout = QHBoxLayout()
        load_list_button = QPushButton("Cargar Lista de Personal")
        load_list_button.clicked.connect(self.load_personal_list)
        buttons_layout.addWidget(load_list_button)

        load_performance_button = QPushButton("Ver Rendimiento de Ventas")
        load_performance_button.clicked.connect(self.load_employee_performance)
        buttons_layout.addWidget(load_performance_button)
        main_layout.addLayout(buttons_layout)

        self.results_table = QTableWidget()
        self.setup_table()
        main_layout.addWidget(self.results_table)

        load_stylesheet(self, "query_windows.css")
        self.load_personal_list()

    # ADDED: Escape key functionality
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.go_back_callback()
        else:
            super().keyPressEvent(event)

    def setup_table(self):
        self.results_table.setSortingEnabled(True)
        self.results_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.results_table.setAlternatingRowColors(True)
        self.results_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.results_table.verticalHeader().setVisible(False)

    def load_personal_list(self):
        results = DB_GLOBAL.get_vista_personal()
        headers = ["ID", "Nombre", "Puesto", "Salario", "Turno", "Entrada", "Salida"]
        self.populate_table(headers, results, is_performance_view=False)
        if results:
            self.results_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
            self.results_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
            self.results_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)

    def load_employee_performance(self):
        results = DB_GLOBAL.get_vista_resumen_ventas_empleado()
        headers = ["ID", "Nombre", "Puesto", "N. Ventas", "Total Generado"]
        self.populate_table(headers, results, is_performance_view=True)
        if results:
            self.results_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
            self.results_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
            self.results_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)

    def populate_table(self, headers, data, is_performance_view=False):
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

                if not is_performance_view and col_num == 3:  # Salario in Personal list (float)
                    table_item = NumericTableWidgetItem(str(item), is_float=True)
                elif is_performance_view and col_num == 4:  # Total Generado in Performance list (float)
                    table_item = NumericTableWidgetItem(str(item), is_float=True)
                elif (col_num == 0) or (is_performance_view and col_num == 3):  # ID or N. Ventas (integer)
                    table_item = NumericTableWidgetItem(str(item))

                self.results_table.setItem(row_num, col_num, table_item)

        self.results_table.resizeRowsToContents()
        self.results_table.setSortingEnabled(True)