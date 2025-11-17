from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QLineEdit, QMessageBox, QFormLayout, QSpinBox
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


class TableInputWindow(QWidget):
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

        main_layout.addWidget(QLabel("Registrar Nueva Mesa"))

        self.form_layout = QFormLayout()
        self.capacity_input = QSpinBox()
        self.capacity_input.setMinimum(1)
        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("Ej: Terraza, Centro, Ventana")

        self.form_layout.addRow("Capacidad:", self.capacity_input)
        self.form_layout.addRow("Ubicación:", self.location_input)
        main_layout.addLayout(self.form_layout)

        self.register_button = QPushButton("Registrar Mesa")
        self.register_button.clicked.connect(self.register_table)
        main_layout.addWidget(self.register_button, alignment=Qt.AlignmentFlag.AlignAbsolute)

        main_layout.addStretch() # <--- LÍNEA AÑADIDA

        load_stylesheet(self, "query_windows.css")

    def register_table(self):
        capacity = self.capacity_input.value()
        location = self.location_input.text()

        if not location:
            QMessageBox.warning(self, "Error", "La ubicación es obligatoria.")
            return

        try:
            new_id = DB_GLOBAL.add_new_table(capacity, location)
            if new_id:
                QMessageBox.information(self, "Éxito", f"Mesa registrada con ID: {new_id} en {location}.")
                self.capacity_input.setValue(1)
                self.location_input.clear()
            else:
                QMessageBox.critical(self, "Error", "No se pudo registrar la mesa.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {e}")