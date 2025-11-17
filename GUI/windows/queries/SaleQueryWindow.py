from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QDateEdit,
    QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout
)
from PySide6.QtCore import Qt, QDate
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


class SaleQueryWindow(QWidget):
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
        self.edit_toggle_button.setToolTip("La edición de ventas no está permitida.")

        top_layout.addStretch()
        top_layout.addWidget(self.edit_toggle_button)
        main_layout.addLayout(top_layout)

        main_layout.addWidget(QLabel("Ventas por Rango de Fecha"))

        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("Desde:"))
        self.date_start = QDateEdit(calendarPopup=True)
        self.date_start.setDate(QDate.currentDate().addDays(-7))
        date_layout.addWidget(self.date_start)

        date_layout.addWidget(QLabel("Hasta:"))
        self.date_end = QDateEdit(calendarPopup=True)
        self.date_end.setDate(QDate.currentDate())
        date_layout.addWidget(self.date_end)

        search_button = QPushButton("Buscar Ventas")
        search_button.clicked.connect(self.load_sales_by_date)
        date_layout.addWidget(search_button)
        main_layout.addLayout(date_layout)

        self.results_table = QTableWidget()
        self.setup_table()
        main_layout.addWidget(self.results_table)

        load_stylesheet(self, "query_windows.css")
        self.load_sales_by_date()

    def setup_table(self):
        self.results_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.results_table.setAlternatingRowColors(True)
        self.results_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.results_table.verticalHeader().setVisible(False)

    def load_sales_by_date(self):
        start_date = self.date_start.date().toString("yyyy-MM-dd")
        end_date = self.date_end.date().toString("yyyy-MM-dd")
        results = DB_GLOBAL.get_sales_between_dates(start_date, end_date)
        headers = ["Venta ID", "Cliente", "Empleado", "Total", "Fecha"]
        self.populate_table(headers, results)
        if results:
            self.results_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
            self.results_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
            self.results_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)

    def populate_table(self, headers, data):
        self.results_table.setRowCount(0)
        self.results_table.setColumnCount(len(headers))
        self.results_table.setHorizontalHeaderLabels(headers)

        if not data:
            return

        self.results_table.setRowCount(len(data))
        for row_num, row_data in enumerate(data):
            for col_num, item in enumerate(row_data):
                table_item = QTableWidgetItem(str(item))

                if col_num == 0:  # Venta ID (integer)
                    table_item = NumericTableWidgetItem(str(item))
                elif col_num == 3:  # Total (float)
                    table_item = NumericTableWidgetItem(str(item), is_float=True)

                self.results_table.setItem(row_num, col_num, table_item)

        self.results_table.resizeRowsToContents()