from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit,
    QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout, QMessageBox
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


class NumericTableWidgetItem(QTableWidgetItem):
    def __init__(self, value, is_float=False):
        super().__init__(str(value))
        self.value = value
        self.is_float = is_float

    def __lt__(self, other):
        try:
            # Forcing numeric comparison for sorting
            if self.is_float:
                return float(self.value) < float(other.value)
            return int(self.value) < int(other.value)
        except ValueError:
            # Fallback to string comparison if not a valid number
            return super().__lt__(other)


class ClientQueryWindow(QWidget):
    def __init__(self, go_back_callback):
        super().__init__()
        self.setObjectName("QueryWindow")
        self.go_back_callback = go_back_callback
        self.edit_mode = False
        self.pending_changes = {}
        self.header_map = {
            "ID": "cliente_id",
            "Nombre": "nombre",
            "Teléfono": "telefono",
            "Correo": "correo",
            "Fecha Nacimiento": "fecha_nacimiento"
        }
        self.column_to_header_map = {v: k for k, v in self.header_map.items()}

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)

        top_layout = QHBoxLayout()
        back_button = QPushButton("Volver")
        back_button.setObjectName("back_button")
        back_button.clicked.connect(self.go_back_callback)
        top_layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignLeft)

        self.edit_toggle_button = QPushButton("Habilitar Edición")
        self.edit_toggle_button.setObjectName("edit_toggle_button")
        self.edit_toggle_button.clicked.connect(self.toggle_edit_mode)

        self.confirm_button = QPushButton("Confirmar Cambios")
        self.confirm_button.setObjectName("confirm_button")
        self.confirm_button.clicked.connect(self.confirm_changes)
        self.confirm_button.setVisible(False)

        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.setObjectName("cancel_button")
        self.cancel_button.clicked.connect(self.cancel_changes)
        self.cancel_button.setVisible(False)

        top_layout.addStretch()
        top_layout.addWidget(self.edit_toggle_button)
        top_layout.addWidget(self.confirm_button)
        top_layout.addWidget(self.cancel_button)
        main_layout.addLayout(top_layout)

        main_layout.addWidget(QLabel("Consultar Clientes (Vista)"))

        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Buscar por:"))
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Nombre, teléfono o correo...")
        search_layout.addWidget(self.search_box)

        search_button = QPushButton("Buscar")
        search_button.clicked.connect(self.load_client_search)
        search_layout.addWidget(search_button)
        main_layout.addLayout(search_layout)

        self.results_table = QTableWidget()
        self.setup_table()
        main_layout.addWidget(self.results_table)

        load_stylesheet(self, "query_windows.css")
        self.load_client_search()

    def setup_table(self):
        self.results_table.setSortingEnabled(True)
        self.results_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.results_table.setAlternatingRowColors(True)
        self.results_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.results_table.verticalHeader().setVisible(False)
        self.results_table.cellChanged.connect(self.on_cell_changed)

    def load_client_search(self):
        self.results_table.cellChanged.disconnect()
        search_term = self.search_box.text()
        headers = ["ID", "Nombre", "Teléfono", "Correo"]

        if not search_term:
            results = DB_GLOBAL.get_vista_clientes()
        else:
            results = DB_GLOBAL.search_client(search_term)

        self.populate_table(headers, results)

        if results:
            self.results_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
            self.results_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
            self.results_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
            self.results_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)

        self.results_table.cellChanged.connect(self.on_cell_changed)
        self.pending_changes.clear()

    def populate_table(self, headers, data):
        self.results_table.setSortingEnabled(False)
        self.results_table.setRowCount(0)
        self.results_table.setColumnCount(len(headers))
        self.results_table.setHorizontalHeaderLabels(headers)

        if not data:
            self.results_table.setSortingEnabled(True)
            return

        self.results_table.setRowCount(len(data))
        for row_num, row_data in enumerate(data):
            for col_num, item in enumerate(row_data):
                if col_num == 0:  # ID column is numeric
                    table_item = NumericTableWidgetItem(str(item))
                    table_item.setFlags(table_item.flags() & ~Qt.ItemIsEditable)
                else:
                    table_item = QTableWidgetItem(str(item))

                self.results_table.setItem(row_num, col_num, table_item)

        self.results_table.resizeRowsToContents()
        self.results_table.setSortingEnabled(True)

    def toggle_edit_mode(self):
        self.edit_mode = not self.edit_mode
        if self.edit_mode:
            self.results_table.setEditTriggers(QTableWidget.AllEditTriggers)
            self.edit_toggle_button.setText("Deshabilitar Edición")
            self.confirm_button.setVisible(True)
            self.cancel_button.setVisible(True)
        else:
            self.results_table.setEditTriggers(QTableWidget.NoEditTriggers)
            self.edit_toggle_button.setText("Habilitar Edición")
            self.confirm_button.setVisible(False)
            self.cancel_button.setVisible(False)
            self.cancel_changes()

    def on_cell_changed(self, row, column):
        if not self.edit_mode:
            return

        id_item = self.results_table.item(row, 0)
        if not id_item:
            return

        primary_key = int(id_item.text())
        header_text = self.results_table.horizontalHeaderItem(column).text()

        new_value = self.results_table.item(row, column).text()

        self.pending_changes[primary_key] = {
            "column_header": header_text,
            "value": new_value,
            "row": row,
            "col": column
        }

        self.results_table.item(row, column).setBackground(QColor(255, 255, 224))

    def confirm_changes(self):
        if not self.pending_changes:
            QMessageBox.information(self, "Sin Cambios", "No hay cambios pendientes para guardar.")
            return

        summary = "Se aplicarán los siguientes cambios:\n\n"
        for pk, change in self.pending_changes.items():
            summary += f"Cliente ID {pk}, Columna '{change['column_header']}': Nuevo Valor '{change['value']}'\n"

        reply = QMessageBox.question(self, "Confirmar Cambios", summary,
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.save_changes_to_db()

    def save_changes_to_db(self):
        try:
            for pk, change in self.pending_changes.items():
                DB_GLOBAL.update_client(pk, change['column_header'], change['value'])

            QMessageBox.information(self, "Éxito", "Cambios guardados exitosamente.")
            self.pending_changes.clear()
            self.toggle_edit_mode()
            self.load_client_search()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron guardar los cambios: {e}")

    def cancel_changes(self):
        self.pending_changes.clear()
        self.load_client_search()
        if self.edit_mode:
            self.toggle_edit_mode()