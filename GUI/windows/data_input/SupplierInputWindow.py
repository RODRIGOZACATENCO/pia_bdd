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


class SupplierInputWindow(QWidget):
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

        main_layout.addWidget(QLabel("Registrar Nuevo Proveedor"))

        self.form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()

        self.form_layout.addRow("Nombre:", self.name_input)
        self.form_layout.addRow("Teléfono:", self.phone_input)
        self.form_layout.addRow("Correo:", self.email_input)
        main_layout.addLayout(self.form_layout)

        self.register_button = QPushButton("Registrar Proveedor")
        self.register_button.clicked.connect(self.register_supplier)
        main_layout.addWidget(self.register_button, alignment=Qt.AlignmentFlag.AlignAbsolute)

        main_layout.addStretch() # <--- LÍNEA AÑADIDA

        load_stylesheet(self, "query_windows.css")

    def register_supplier(self):
        name = self.name_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()

        if not name:
            QMessageBox.warning(self, "Error", "El nombre es obligatorio.")
            return

        try:
            new_id = DB_GLOBAL.add_new_supplier(name, phone, email)
            if new_id:
                QMessageBox.information(self, "Éxito", f"Proveedor '{name}' registrado con ID: {new_id}.")
                self.name_input.clear()
                self.phone_input.clear()
                self.email_input.clear()
            else:
                QMessageBox.critical(self, "Error", "No se pudo registrar al proveedor.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {e}")