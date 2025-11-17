from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QLineEdit, QMessageBox, QFormLayout, QComboBox
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


class UserInputWindow(QWidget):
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

        main_layout.addWidget(QLabel("Registrar Nuevo Usuario del Sistema"))

        self.form_layout = QFormLayout()

        self.employee_combo = QComboBox()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.form_layout.addRow("Empleado:", self.employee_combo)
        self.form_layout.addRow("Nombre de Usuario:", self.username_input)
        self.form_layout.addRow("Contraseña:", self.password_input)
        main_layout.addLayout(self.form_layout)

        self.register_button = QPushButton("Registrar Usuario")
        self.register_button.clicked.connect(self.register_user)
        main_layout.addWidget(self.register_button, alignment=Qt.AlignmentFlag.AlignAbsolute)

        main_layout.addStretch()

        load_stylesheet(self, "query_windows.css")
        self.load_employees()

    def load_employees(self):

        self.employee_combo.clear()
        try:
            employees = DB_GLOBAL.get_employees_without_user_account()
            if not employees:
                self.employee_combo.addItem("No hay empleados sin cuenta", None)
                self.register_button.setEnabled(False)
                return

            self.register_button.setEnabled(True)
            for emp_id, name, puesto in employees:
                self.employee_combo.addItem(f"{name} ({puesto})", emp_id)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar la lista de empleados: {e}")

    def register_user(self):
        empleado_id = self.employee_combo.currentData()
        username = self.username_input.text()
        password = self.password_input.text()

        if empleado_id is None:
            QMessageBox.warning(self, "Error", "No hay empleados seleccionables.")
            return

        if not username or not password:
            QMessageBox.warning(self, "Error", "El nombre de usuario y la contraseña no pueden estar vacíos.")
            return

        try:
            success, message = DB_GLOBAL.create_system_user(empleado_id, username, password)
            if success:
                QMessageBox.information(self, "Éxito", message)

                self.username_input.clear()
                self.password_input.clear()
                self.load_employees()
            else:
                QMessageBox.critical(self, "Error", message)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error inesperado: {e}")