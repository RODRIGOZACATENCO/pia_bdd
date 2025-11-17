from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QLineEdit, QMessageBox, QFormLayout, QTimeEdit, QSpinBox
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


class ShiftInputWindow(QWidget):
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

        main_layout.addWidget(QLabel("Registrar Nuevo Turno"))

        self.form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ej: Matutino, Vespertino, Nocturno")
        self.start_time_input = QTimeEdit()
        self.end_time_input = QTimeEdit()
        self.employee_count_input = QSpinBox()
        self.employee_count_input.setMinimum(0)

        self.form_layout.addRow("Nombre Turno:", self.name_input)
        self.form_layout.addRow("Hora Inicio:", self.start_time_input)
        self.form_layout.addRow("Hora Fin:", self.end_time_input)
        self.form_layout.addRow("N. Empleados:", self.employee_count_input)
        main_layout.addLayout(self.form_layout)

        self.register_button = QPushButton("Registrar Turno")
        self.register_button.clicked.connect(self.register_shift)
        main_layout.addWidget(self.register_button, alignment=Qt.AlignmentFlag.AlignAbsolute)

        main_layout.addStretch()

        load_stylesheet(self, "query_windows.css")

    def register_shift(self):
        name = self.name_input.text()
        start_time = self.start_time_input.time().toString("hh:mm:ss")
        end_time = self.end_time_input.time().toString("hh:mm:ss")
        employee_count = self.employee_count_input.value()

        if not name:
            QMessageBox.warning(self, "Error", "El nombre del turno es obligatorio.")
            return

        try:
            new_id = DB_GLOBAL.add_new_shift(name, start_time, end_time, employee_count)
            if new_id:
                QMessageBox.information(self, "Éxito", f"Turno '{name}' registrado con ID: {new_id}.")
                self.name_input.clear()
            else:
                QMessageBox.critical(self, "Error", "No se pudo registrar el turno.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {e}")