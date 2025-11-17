from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QLineEdit, QTableWidget, QTableWidgetItem,
    QAbstractItemView, QHeaderView, QMessageBox
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



class ClientEntryWindow(QWidget):
    def __init__(self, go_to_main_menu_callback, go_to_new_client_callback):
        super().__init__()
        self.setObjectName("ClientEntryWindow")
        self.table_id = -1
        self.go_to_main_menu_callback = go_to_main_menu_callback
        self.go_to_new_client_callback = go_to_new_client_callback
        self.id_column_color = QColor(160, 160, 160)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.layout)

        self.return_button = QPushButton("Volver al Menú Principal")
        self.return_button.setObjectName("return_button")
        self.return_button.clicked.connect(self.go_to_main_menu_callback)
        self.layout.addWidget(self.return_button)

        self.new_client_button = QPushButton("Agregar Nuevo Cliente")
        self.new_client_button.setObjectName("new_client_buttom")
        self.new_client_button.clicked.connect(self.on_new_client_click)
        self.layout.addWidget(self.new_client_button)

        self.search_label = QLabel("Cliente:")
        self.layout.addWidget(self.search_label)

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Buscar por nombre, teléfono o correo...")
        self.layout.addWidget(self.search_box)

        self.client_table = QTableWidget()
        self.client_table.setColumnCount(4)
        self.client_table.setHorizontalHeaderLabels(["ID", "Nombre", "Teléfono", "Correo"])
        self.client_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.client_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.client_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.client_table.verticalHeader().setVisible(False)

        header = self.client_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)

        self.layout.addWidget(self.client_table)

        self.search_box.textChanged.connect(self.search_clients)
        self.client_table.cellClicked.connect(self.select_client)

        load_stylesheet(self, "client_entry_window.css")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.go_to_main_menu_callback()
        else:
            super().keyPressEvent(event)
    def set_table(self, table_id):
        self.table_id = table_id
        print(f"Ventana de cliente abierta para Mesa ID: {self.table_id}")
        self.search_box.clear()
        self.client_table.setRowCount(0)
        self.search_clients()

    def search_clients(self):
        search_text = self.search_box.text()
        results = DB_GLOBAL.search_client(search_text)
        self.client_table.setRowCount(0)
        if results:
            for row_num, (client_id, nombre, telefono, correo) in enumerate(results):
                self.client_table.insertRow(row_num)

                id_item = QTableWidgetItem(str(client_id))
                id_item.setBackground(self.id_column_color)
                name_item = QTableWidgetItem(str(nombre))
                phone_item = QTableWidgetItem(str(telefono))
                email_item = QTableWidgetItem(str(correo))

                self.client_table.setItem(row_num, 0, id_item)
                self.client_table.setItem(row_num, 1, name_item)
                self.client_table.setItem(row_num, 2, phone_item)
                self.client_table.setItem(row_num, 3, email_item)

    def select_client(self, row, column):
        client_id_item = self.client_table.item(row, 0)
        client_id = int(client_id_item.text())

        client_name_item = self.client_table.item(row, 1)
        client_name = client_name_item.text()

        print(f"Cliente seleccionado: ID {client_id}, Nombre: {client_name}")
        print(f"Asignando a Mesa ID: {self.table_id}")
        DB_GLOBAL.assign_table(self.table_id, client_id)

        QMessageBox.information(self, "Asignación Exitosa",
                                f"Cliente {client_name} (ID: {client_id}) asignado a la Mesa ID: {self.table_id}")
        self.go_to_main_menu_callback()

    def on_new_client_click(self):
        self.go_to_new_client_callback(self.table_id)