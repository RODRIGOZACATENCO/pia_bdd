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


class ClientInputWindow(QWidget):
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

        main_layout.addWidget(QLabel("Registrar Nuevo Cliente"))

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
        main_layout.addLayout(self.form_layout)

        self.register_button = QPushButton("Registrar Cliente")
        self.register_button.clicked.connect(self.register_client)
        main_layout.addWidget(self.register_button, alignment=Qt.AlignmentFlag.AlignAbsolute)

        main_layout.addStretch() # <--- LÍNEA AÑADIDA

        load_stylesheet(self, "query_windows.css")

    def register_client(self):
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
                QMessageBox.information(self, "Éxito", f"Cliente '{name}' registrado con ID: {new_client_id}.")
                self.name_input.clear()
                self.phone_input.clear()
                self.email_input.clear()
                self.dob_input.clear()
            else:
                QMessageBox.critical(self, "Error", "No se pudo registrar al cliente en la base de datos.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {e}")