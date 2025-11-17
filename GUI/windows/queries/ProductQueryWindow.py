from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit,
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


class ProductQueryWindow(QWidget):
    def __init__(self, go_back_callback):
        super().__init__()
        self.setObjectName("QueryWindow")
        self.go_back_callback = go_back_callback

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)

        back_button = QPushButton("Volver")
        back_button.setObjectName("back_button")
        back_button.clicked.connect(self.go_back_callback)
        main_layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignLeft)

        main_layout.addWidget(QLabel("Consultas de Productos"))

        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Buscar por:"))
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Nombre o marca...")
        search_layout.addWidget(self.search_box)

        search_button = QPushButton("Buscar en Catálogo")
        search_button.clicked.connect(self.load_product_search)
        search_layout.addWidget(search_button)
        main_layout.addLayout(search_layout)

        most_sold_layout = QHBoxLayout()
        most_sold_product_button = QPushButton("Más Vendidos por Producto")
        most_sold_product_button.clicked.connect(self.load_most_sold_by_product)
        most_sold_layout.addWidget(most_sold_product_button)

        most_sold_brand_button = QPushButton("Más Vendidos por Marca")
        most_sold_brand_button.clicked.connect(self.load_most_sold_by_brand)
        most_sold_layout.addWidget(most_sold_brand_button)

        most_sold_type_button = QPushButton("Más Vendidos por Tipo")
        most_sold_type_button.clicked.connect(self.load_most_sold_by_type)
        most_sold_layout.addWidget(most_sold_type_button)

        main_layout.addLayout(most_sold_layout)

        self.results_table = QTableWidget()
        self.setup_table()
        main_layout.addWidget(self.results_table)

        load_stylesheet(self, "query_windows.css")
        self.load_product_search()

    def setup_table(self):
        self.results_table.setSortingEnabled(True)
        self.results_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.results_table.setAlternatingRowColors(True)
        self.results_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.results_table.verticalHeader().setVisible(False)

    def load_product_search(self):
        search_term = self.search_box.text()

        if not search_term:
            results = DB_GLOBAL.get_vista_productos()
            headers = ["Producto", "Marca", "Tipo", "Precio", "Stock"]
            self.populate_table(headers, results, view_type="CATALOGO")
        else:
            results = DB_GLOBAL.search_product_gui(search_term)
            headers = ["ID", "Nombre", "Precio", "Stock", "PromoID"]
            self.populate_table(headers, results, view_type="SEARCH")

        if results:
            self.results_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
            self.results_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
            if not search_term:
                self.results_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
                self.results_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
                self.results_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
            else:
                self.results_table.horizontalHeader().setColumnHidden(4, True)

    def load_most_sold_by_product(self):
        results = DB_GLOBAL.get_most_sold_by_product()
        headers = ["Producto", "Total Vendido"]
        self.populate_table(headers, results, view_type="MOST_SOLD")
        if results:
            self.results_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
            self.results_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)

    def load_most_sold_by_brand(self):
        results = DB_GLOBAL.get_most_sold_by_brand()
        headers = ["Marca", "Total Vendido"]
        self.populate_table(headers, results, view_type="MOST_SOLD")
        if results:
            self.results_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
            self.results_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)

    def load_most_sold_by_type(self):
        results = DB_GLOBAL.get_most_sold_by_type()
        headers = ["Tipo", "Total Vendido"]
        self.populate_table(headers, results, view_type="MOST_SOLD")
        if results:
            self.results_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
            self.results_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)

    def populate_table(self, headers, data, view_type="CATALOGO"):
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

                if view_type == "CATALOGO":
                    if col_num == 3:  # Precio (float)
                        table_item = NumericTableWidgetItem(str(item), is_float=True)
                    elif col_num == 4:  # Stock (integer)
                        table_item = NumericTableWidgetItem(str(item))
                elif view_type == "SEARCH":
                    if col_num == 0 or col_num == 3 or col_num == 4:  # ID, Stock, PromoID (integer)
                        table_item = NumericTableWidgetItem(str(item))
                        if col_num == 0:
                            table_item.setFlags(table_item.flags() & ~Qt.ItemIsEditable)
                    elif col_num == 2:  # Precio (float)
                        table_item = NumericTableWidgetItem(str(item), is_float=True)
                elif view_type == "MOST_SOLD":
                    if col_num == 1:  # Total Vendido (float)
                        table_item = NumericTableWidgetItem(str(item), is_float=True)

                self.results_table.setItem(row_num, col_num, table_item)

        self.results_table.resizeRowsToContents()
        self.results_table.setSortingEnabled(True)