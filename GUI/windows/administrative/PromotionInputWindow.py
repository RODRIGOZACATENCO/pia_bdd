from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QLineEdit, QMessageBox, QFormLayout, QDateEdit,
    QTableWidget, QTableWidgetItem, QComboBox, QDoubleSpinBox,
    QHBoxLayout, QHeaderView
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


class PromotionInputWindow(QWidget):
    def __init__(self, go_back_callback):
        super().__init__()
        self.setObjectName("QueryWindow")
        self.go_back_callback = go_back_callback
        self.products = []

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)

        back_button = QPushButton("Volver")
        back_button.setObjectName("back_button")
        back_button.clicked.connect(self.go_back_callback)
        main_layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignLeft)

        main_layout.addWidget(QLabel("Registrar Nueva Promoción"))

        self.form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.start_date_input = QDateEdit(calendarPopup=True)
        self.start_date_input.setDate(QDate.currentDate())
        self.end_date_input = QDateEdit(calendarPopup=True)
        self.end_date_input.setDate(QDate.currentDate().addDays(7))

        self.form_layout.addRow("Nombre:", self.name_input)
        self.form_layout.addRow("Fecha Inicio:", self.start_date_input)
        self.form_layout.addRow("Fecha Fin:", self.end_date_input)
        main_layout.addLayout(self.form_layout)

        main_layout.addWidget(QLabel("Detalles de la Promoción"))

        self.detail_layout = QHBoxLayout()
        self.product_combo = QComboBox()
        self.offer_price_input = QDoubleSpinBox()
        self.offer_price_input.setMaximum(100000.00)
        self.offer_price_input.setDecimals(2)
        self.add_detail_button = QPushButton("Añadir Producto")

        self.detail_layout.addWidget(QLabel("Producto:"))
        self.detail_layout.addWidget(self.product_combo)
        self.detail_layout.addWidget(QLabel("Precio Oferta:"))
        self.detail_layout.addWidget(self.offer_price_input)
        self.detail_layout.addWidget(self.add_detail_button)
        main_layout.addLayout(self.detail_layout)

        self.details_table = QTableWidget()
        self.setup_table()
        main_layout.addWidget(self.details_table)

        self.remove_detail_button = QPushButton("Remover Producto Seleccionado")
        self.remove_detail_button.clicked.connect(self.remove_selected_detail)
        main_layout.addWidget(self.remove_detail_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.register_button = QPushButton("Registrar Promoción")
        self.register_button.clicked.connect(self.register_promotion)
        main_layout.addWidget(self.register_button, alignment=Qt.AlignmentFlag.AlignAbsolute)

        main_layout.addStretch()

        self.add_detail_button.clicked.connect(self.add_detail_to_table)

        load_stylesheet(self, "query_windows.css")
        self.load_product_data()

    def load_product_data(self):
        try:
            self.products = DB_GLOBAL.get_products_list()
            self.product_combo.clear()
            for product_id, name in self.products:
                self.product_combo.addItem(name, product_id)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar la lista de productos: {e}")

    def setup_table(self):
        self.details_table.setColumnCount(3)
        self.details_table.setHorizontalHeaderLabels(["ID Producto", "Nombre", "Precio Oferta"])
        self.details_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.details_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.details_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

    def add_detail_to_table(self):
        product_id = self.product_combo.currentData()
        product_name = self.product_combo.currentText()
        offer_price = self.offer_price_input.value()

        if product_id is None or offer_price <= 0:
            QMessageBox.warning(self, "Error", "Seleccione un producto y un precio de oferta válido.")
            return

        row_position = self.details_table.rowCount()
        self.details_table.insertRow(row_position)
        self.details_table.setItem(row_position, 0, QTableWidgetItem(str(product_id)))
        self.details_table.setItem(row_position, 1, QTableWidgetItem(product_name))
        self.details_table.setItem(row_position, 2, QTableWidgetItem(str(offer_price)))

    def remove_selected_detail(self):
        selected_row = self.details_table.currentRow()
        if selected_row >= 0:
            self.details_table.removeRow(selected_row)
        else:
            QMessageBox.warning(self, "Error", "Seleccione un producto de la tabla para remover.")

    def register_promotion(self):
        name = self.name_input.text()
        start_date = self.start_date_input.date().toString("yyyy-MM-dd")
        end_date = self.end_date_input.date().toString("yyyy-MM-dd")

        if not name:
            QMessageBox.warning(self, "Error", "El nombre es obligatorio.")
            return

        details = []
        for row in range(self.details_table.rowCount()):
            product_id = int(self.details_table.item(row, 0).text())
            offer_price = float(self.details_table.item(row, 2).text())
            details.append((product_id, offer_price))

        if not details:
            QMessageBox.warning(self, "Error", "Debe añadir al menos un producto a la promoción.")
            return

        try:
            new_id = DB_GLOBAL.add_new_promotion_with_details(name, start_date, end_date, details)
            if new_id:
                QMessageBox.information(self, "Éxito", f"Promoción '{name}' registrada con ID: {new_id}.")
                self.name_input.clear()
                self.details_table.setRowCount(0)
            else:
                QMessageBox.critical(self, "Error", "No se pudo registrar la promoción.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {e}")