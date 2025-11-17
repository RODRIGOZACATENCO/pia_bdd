from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QLineEdit, QTableWidget, QTableWidgetItem,
    QAbstractItemView, QHeaderView, QMessageBox,
    QHBoxLayout, QSpinBox
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


class AddOrderWindow(QWidget):
    def __init__(self, on_occupied_table):
        super().__init__()
        self.setObjectName("QueryWindow")
        self.on_occupied_table = on_occupied_table
        self.sale_id = -1
        self.table_id = -1

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.title = QLabel("Agregar Orden")
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title)

        search_layout = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Buscar producto por nombre...")
        self.search_box.textChanged.connect(self._search_products)
        search_layout.addWidget(self.search_box)
        self.layout.addLayout(search_layout)

        controls_layout = QHBoxLayout()
        self.selected_product_label = QLabel("Seleccione un producto...")
        self.selected_product_label.setObjectName("selected_product_label")
        controls_layout.addWidget(self.selected_product_label, 1)

        self.qty_label = QLabel("Cantidad:")
        self.quantity_spinbox = QSpinBox()
        self.quantity_spinbox.setMinimum(1)
        self.quantity_spinbox.setValue(1)
        self.add_button = QPushButton("Agregar")
        self.add_button.clicked.connect(self._add_order)

        controls_layout.addWidget(self.qty_label)
        controls_layout.addWidget(self.quantity_spinbox)
        controls_layout.addWidget(self.add_button)
        self.layout.addLayout(controls_layout)

        self.products_table = QTableWidget()
        self.setup_table()
        self.products_table.itemSelectionChanged.connect(self._on_product_selected)
        self.layout.addWidget(self.products_table)

        self.back_button = QPushButton("Volver a la Mesa")
        self.back_button.setObjectName("back_button")
        self.back_button.clicked.connect(self._on_back_click)
        self.layout.addWidget(self.back_button)

        load_stylesheet(self, "add_order_window.css")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self._on_back_click()
        else:
            super().keyPressEvent(event)

    def setup_table(self):
        self.products_table.setSortingEnabled(True)
        self.products_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.products_table.setAlternatingRowColors(True)
        self.products_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.products_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.products_table.verticalHeader().setVisible(False)
        self.products_table.setColumnHidden(4, True)

        header = self.products_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)

    def populate_table(self, headers, data):
        self.products_table.setSortingEnabled(False)
        self.products_table.setRowCount(0)
        self.products_table.setColumnCount(len(headers))
        self.products_table.setHorizontalHeaderLabels(headers)

        if not data:
            self.products_table.setSortingEnabled(True)
            return

        self.products_table.setRowCount(len(data))
        for row_num, row_data in enumerate(data):
            for col_num, item in enumerate(row_data):
                table_item = QTableWidgetItem(str(item))

                self.products_table.setItem(row_num, col_num, table_item)

        self.products_table.resizeRowsToContents()
        self.products_table.setSortingEnabled(True)

    def set_data(self, sale_id, table_id):
        self.sale_id = sale_id
        self.table_id = table_id
        self.title.setText(f"Agregar Orden (Venta ID: {self.sale_id})")
        self.search_box.clear()
        self.products_table.setRowCount(0)
        self._search_products()

    def _on_back_click(self):
        if self.table_id != -1:
            self.on_occupied_table(self.table_id)

    def _on_product_selected(self):
        selected_rows = self.products_table.selectionModel().selectedRows()
        if not selected_rows:
            self.selected_product_label.setText("Seleccione un producto...")
            return

        row = selected_rows[0].row()
        product_name_item = self.products_table.item(row, 1)

        if product_name_item:
            self.selected_product_label.setText(f"Producto: {product_name_item.text()}")

    def _search_products(self):
        search_text = self.search_box.text()
        results = DB_GLOBAL.search_product_gui(search_text)

        processed_results = []
        if results:
            for (prod_id, nombre, precio, stock, promo_id) in results:
                promo_id_str = str(promo_id) if promo_id is not None else ""
                processed_results.append((prod_id, nombre, precio, stock, promo_id_str))

        headers = ["ID", "Nombre", "Precio", "Stock", "PromoID"]
        self.populate_table(headers, processed_results)

        if results:
            self.products_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
            self.products_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
            self.products_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
            self.products_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)

    def _add_order(self):
        selected_rows = self.products_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Error", "Seleccione un producto de la lista.")
            return

        row = selected_rows[0].row()
        product_id = int(self.products_table.item(row, 0).text())
        price_at_sale = float(self.products_table.item(row, 2).text())
        current_stock = int(self.products_table.item(row, 3).text())
        quantity = self.quantity_spinbox.value()

        promocion_id_str = self.products_table.item(row, 4).text()
        promocion_id = None
        if promocion_id_str:
            try:
                promocion_id = int(promocion_id_str)
            except ValueError:
                promocion_id = None

        if quantity > current_stock:
            QMessageBox.warning(self, "Error", f"No hay suficiente stock. Disponible: {current_stock}")
            return

        success = DB_GLOBAL.register_order_gui(self.sale_id, product_id, quantity, price_at_sale, promocion_id)

        if success:
            QMessageBox.information(self, "Éxito", "Orden agregada exitosamente.")
            self._search_products()
        else:
            QMessageBox.critical(self, "Error", "No se pudo agregar la orden. Verifique el stock.")
            self._search_products()