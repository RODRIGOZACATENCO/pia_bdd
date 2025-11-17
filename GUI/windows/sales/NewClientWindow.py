from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QLineEdit, QMessageBox, QFormLayout
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


class NewClientWindow(QWidget):
    def __init__(self, go_to_main_menu_callback, go_to_client_entry_callback):
        super().__init__()
        self.setObjectName("NewClientWindow")
        self.go_to_main_menu_callback = go_to_main_menu_callback
        self.go_to_client_entry_callback = go_to_client_entry_callback
        self.table_id = -1

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.title = QLabel("Registrar Nuevo Cliente")
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title)

        self.form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.dob_input = QLineEdit()
        self.dob_input.setPlaceholderText("YYYY-MM-DD")

        self.form_layout.addRow("Nombre:", self.name_input)
        self.form_layout.addRow("Teléfono:", self.phone_input)
        self.form_layout.addRow("Correo:", self.email_input)
        self.form_layout.addRow("Fecha Nacimiento:", self.dob_input)

        self.layout.addLayout(self.form_layout)

        self.register_button = QPushButton("Registrar y Asignar")
        self.register_button.setObjectName("registrar_button")
        self.register_button.clicked.connect(self.register_new_client)
        self.layout.addWidget(self.register_button)

        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.setObjectName("cancel_button")
        self.cancel_button.clicked.connect(self.on_cancel_click)
        self.layout.addWidget(self.cancel_button)

        load_stylesheet(self, "new_client_window.css")

    def set_data(self, table_id):
        self.table_id = table_id
        self.name_input.clear()
        self.phone_input.clear()
        self.email_input.clear()
        self.dob_input.clear()

    def on_cancel_click(self):
        self.go_to_client_entry_callback(self.table_id)

    def register_new_client(self):
        name = self.name_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()
        dob = self.dob_input.text()

        if not name or not dob:
            QMessageBox.warning(self, "Error", "Nombre y Fecha de Nacimiento son obligatorios.")
            return

        try:
            new_client_id = DB_GLOBAL.register_client_gui(name, phone, email, dob)
            if new_client_id:
                DB_GLOBAL.assign_table(self.table_id, new_client_id)
                QMessageBox.information(self, "Éxito",
                                        f"Cliente '{name}' registrado (ID: {new_client_id}) y asignado a la Mesa ID: {self.table_id}.")
                self.go_to_main_menu_callback()
            else:
                QMessageBox.critical(self, "Error", "No se pudo registrar al cliente en la base de datos.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {e}")