from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QMessageBox, QFormLayout, QDateEdit,
    QTableWidget, QTableWidgetItem, QComboBox, QDoubleSpinBox,
    QHeaderView, QSpinBox, QAbstractItemView
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


class PurchaseOrderInputWindow(QWidget):
    def __init__(self, go_back_callback):
        super().__init__()
        self.setObjectName("QueryWindow")
        self.go_back_callback = go_back_callback
        self.products = []
        self.suppliers = []

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)

        back_button = QPushButton("Volver")
        back_button.setObjectName("back_button")
        back_button.clicked.connect(self.go_back_callback)
        main_layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignLeft)

        main_layout.addWidget(QLabel("Registrar Nueva Orden de Compra"))

        self.form_layout = QFormLayout()
        self.supplier_combo = QComboBox()
        self.date_input = QDateEdit(calendarPopup=True)
        self.date_input.setDate(QDate.currentDate())
        self.total_input = QDoubleSpinBox()
        self.total_input.setMaximum(1000000.00)
        self.total_input.setDecimals(2)

        self.form_layout.addRow("Proveedor:", self.supplier_combo)
        self.form_layout.addRow("Fecha Suministro:", self.date_input)
        self.form_layout.addRow("Total Pago:", self.total_input)
        main_layout.addLayout(self.form_layout)

        main_layout.addWidget(QLabel("Detalles de la Orden"))

        self.detail_layout = QFormLayout()
        self.product_combo = QComboBox()
        self.purchase_price_input = QDoubleSpinBox()
        self.purchase_price_input.setMaximum(100000.00)
        self.purchase_price_input.setDecimals(2)
        self.quantity_input = QSpinBox()
        self.quantity_input.setMaximum(10000)
        self.quantity_input.setMinimum(1)
        self.add_detail_button = QPushButton("Añadir Producto a la Orden")

        self.detail_layout.addRow("Producto:", self.product_combo)
        self.detail_layout.addRow("Precio Compra:", self.purchase_price_input)
        self.detail_layout.addRow("Cantidad:", self.quantity_input)
        self.detail_layout.addRow(self.add_detail_button)
        main_layout.addLayout(self.detail_layout)

        self.details_table = QTableWidget()
        self.setup_table()
        main_layout.addWidget(self.details_table)

        self.remove_detail_button = QPushButton("Remover Producto Seleccionado")
        self.remove_detail_button.clicked.connect(self.remove_selected_detail)
        main_layout.addWidget(self.remove_detail_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.register_button = QPushButton("Registrar Orden de Compra")
        self.register_button.clicked.connect(self.register_purchase_order)
        main_layout.addWidget(self.register_button, alignment=Qt.AlignmentFlag.AlignAbsolute)

        main_layout.addStretch()  # <--- LÍNEA AÑADIDA

        self.add_detail_button.clicked.connect(self.add_detail_to_table)

        load_stylesheet(self, "query_windows.css")
        self.load_data()

    def load_data(self):
        try:
            self.products = DB_GLOBAL.get_products_list()
            self.product_combo.clear()
            for product_id, name in self.products:
                self.product_combo.addItem(name, product_id)

            self.suppliers = DB_GLOBAL.get_suppliers_list()
            self.supplier_combo.clear()
            for supplier_id, name in self.suppliers:
                self.supplier_combo.addItem(name, supplier_id)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar la lista de productos/proveedores: {e}")

    def setup_table(self):
        self.details_table.setColumnCount(5)
        self.details_table.setHorizontalHeaderLabels(["ID Producto", "Nombre", "Precio Compra", "Cantidad", "Subtotal"])
        self.details_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.details_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.details_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

    def add_detail_to_table(self):
        product_id = self.product_combo.currentData()
        product_name = self.product_combo.currentText()
        price = self.purchase_price_input.value()
        quantity = self.quantity_input.value()

        if product_id is None or price <= 0 or quantity <= 0:
            QMessageBox.warning(self, "Error", "Seleccione producto, precio y cantidad válidos.")
            return

        subtotal = price * quantity

        row_position = self.details_table.rowCount()
        self.details_table.insertRow(row_position)
        self.details_table.setItem(row_position, 0, QTableWidgetItem(str(product_id)))
        self.details_table.setItem(row_position, 1, QTableWidgetItem(product_name))
        self.details_table.setItem(row_position, 2, QTableWidgetItem(str(price)))
        self.details_table.setItem(row_position, 3, QTableWidgetItem(str(quantity)))
        self.details_table.setItem(row_position, 4, QTableWidgetItem(f"{subtotal:.2f}"))

    def remove_selected_detail(self):
        selected_row = self.details_table.currentRow()
        if selected_row >= 0:
            self.details_table.removeRow(selected_row)
        else:
            QMessageBox.warning(self, "Error", "Seleccione un producto de la tabla para remover.")

    def register_purchase_order(self):
        supplier_id = self.supplier_combo.currentData()
        date = self.date_input.date().toString("yyyy-MM-dd")
        total = self.total_input.value()

        if supplier_id is None or total <= 0:
            QMessageBox.warning(self, "Error", "Proveedor y total son obligatorios.")
            return

        details = []
        for row in range(self.details_table.rowCount()):
            product_id = int(self.details_table.item(row, 0).text())
            price = float(self.details_table.item(row, 2).text())
            quantity = int(self.details_table.item(row, 3).text())
            details.append((product_id, price, quantity))

        if not details:
            QMessageBox.warning(self, "Error", "Debe añadir al menos un producto a la orden.")
            return

        try:
            new_id = DB_GLOBAL.add_new_purchase_order(supplier_id, date, total, details)
            if new_id:
                QMessageBox.information(self, "Éxito",
                                        f"Orden de Compra registrada con ID: {new_id}. Stock actualizado.")
                self.total_input.setValue(0)
                self.details_table.setRowCount(0)
            else:
                QMessageBox.critical(self, "Error",
                                     "No se pudo registrar la orden de compra. La transacción fue revertida.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {e}")