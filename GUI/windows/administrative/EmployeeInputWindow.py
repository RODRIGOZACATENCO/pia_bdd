from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QLineEdit, QMessageBox, QFormLayout, QComboBox, QDoubleSpinBox
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


class EmployeeInputWindow(QWidget):
    def __init__(self, go_back_callback):
        super().__init__()
        self.setObjectName("QueryWindow")
        self.go_back_callback = go_back_callback
        self.shifts = []
        self.puestos = []

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)

        back_button = QPushButton("Volver")
        back_button.setObjectName("back_button")
        back_button.clicked.connect(self.go_back_callback)
        main_layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignLeft)

        main_layout.addWidget(QLabel("Registrar Nuevo Empleado"))

        self.form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.salary_input = QDoubleSpinBox()
        self.salary_input.setMinimum(1.00)
        self.salary_input.setMaximum(100000.00)
        self.salary_input.setDecimals(2)
        self.shift_combo = QComboBox()
        self.position_combo = QComboBox()


        self.form_layout.addRow("Nombre:", self.name_input)
        self.form_layout.addRow("Salario:", self.salary_input)
        self.form_layout.addRow("Turno:", self.shift_combo)
        self.form_layout.addRow("Puesto:", self.position_combo)
        main_layout.addLayout(self.form_layout)

        self.register_button = QPushButton("Registrar Empleado")
        self.register_button.clicked.connect(self.register_employee)
        main_layout.addWidget(self.register_button, alignment=Qt.AlignmentFlag.AlignAbsolute)

        main_layout.addStretch()

        load_stylesheet(self, "query_windows.css")
        self.load_data()

    def load_data(self):
        try:
            self.shifts = DB_GLOBAL.get_shifts_list()
            self.shift_combo.clear()
            for shift_id, name in self.shifts:
                self.shift_combo.addItem(name, shift_id)

            self.puestos = DB_GLOBAL.get_puestos_list()
            self.position_combo.clear()
            for puesto_id, name in self.puestos:
                self.position_combo.addItem(name, puesto_id)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar la lista de turnos/puestos: {e}")

    def register_employee(self):
        name = self.name_input.text()
        salary = self.salary_input.value()
        shift_id = self.shift_combo.currentData()
        position_id = self.position_combo.currentData()

        if not name or salary <= 0 or shift_id is None or position_id is None:
            QMessageBox.warning(self, "Error", "Nombre, salario, turno y puesto son obligatorios.")
            return

        try:
            new_id = DB_GLOBAL.add_new_employee(shift_id, position_id, name, salary)
            if new_id:
                QMessageBox.information(self, "Éxito", f"Empleado '{name}' registrado con ID: {new_id}.")
                self.name_input.clear()
                self.salary_input.setValue(1.00)
                self.load_data()
            else:
                QMessageBox.critical(self, "Error", "No se pudo registrar al empleado.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {e}")