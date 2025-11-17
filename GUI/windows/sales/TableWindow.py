from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QGridLayout,
    QPushButton, QButtonGroup, QHBoxLayout, QLabel
)
from PySide6.QtCore import QDateTime, QTimer, Qt
from PySide6.QtGui import QFont
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


class TableWindow(QWidget):
    def __init__(self, go_to_client_entry_callback, go_to_occupied_table_callback, go_to_query_hub_callback,
                 go_to_data_input_hub_callback):
        super().__init__()
        self.go_to_client_entry_callback = go_to_client_entry_callback
        self.go_to_occupied_table_callback = go_to_occupied_table_callback
        self.go_to_query_hub_callback = go_to_query_hub_callback
        self.go_to_data_input_hub_callback = go_to_data_input_hub_callback
        self.employee_name = "N/A"

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.setup_dashboard()
        main_layout.addWidget(self.dashboard_widget)

        self.setup_tables_tab()
        main_layout.addWidget(self.tables_widget)

        self.setup_timer()
        self.update_total_orders()
        load_stylesheet(self, "main_window.css")

    def setup_tables_tab(self):
        self.tables_widget = QWidget()
        tables_layout = QVBoxLayout(self.tables_widget)
        tables_layout.setContentsMargins(0, 0, 0, 0)

        self.table_buttons_group = QButtonGroup()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        tables_layout.addWidget(scroll)

        container = QWidget()
        container.setObjectName("botones_mesa")
        scroll.setWidget(container)
        buttons_layout = QGridLayout(container)

        self.tables = DB_GLOBAL.tables
        self.button_widgets = []

        for i, table in enumerate(self.tables):
            button = QPushButton()
            self.button_widgets.append(button)
            self.table_buttons_group.addButton(button, table.table_id)

            row, col = divmod(i, 3)
            buttons_layout.addWidget(button, row, col)

        self.update_table_buttons()
        self.table_buttons_group.idClicked.connect(self.handle_table_click)

    def setup_dashboard(self):
        self.dashboard_widget = QWidget()
        self.dashboard_widget.setObjectName("dashboard")
        dashboard_layout = QHBoxLayout(self.dashboard_widget)

        logo_label = QLabel("LOGO")
        logo_label.setObjectName("logo")
        logo_label.setFixedSize(100, 50)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dashboard_layout.addWidget(logo_label)

        bar_title = QLabel("BISONBAR")
        bar_title.setObjectName("bar_title")
        dashboard_layout.addWidget(bar_title)

        dashboard_layout.addStretch()

        nav_layout = QHBoxLayout()
        self.queries_button = QPushButton("Consultas")
        self.queries_button.setObjectName("nav_button")
        self.queries_button.clicked.connect(self.go_to_query_hub_callback)

        self.data_input_button = QPushButton("Ingreso de Datos")
        self.data_input_button.setObjectName("nav_button")
        self.data_input_button.clicked.connect(self.go_to_data_input_hub_callback)

        nav_layout.addWidget(self.queries_button)
        nav_layout.addWidget(self.data_input_button)
        dashboard_layout.addLayout(nav_layout)

        dashboard_layout.addStretch()

        stats_widget = QWidget()
        stats_layout = QVBoxLayout(stats_widget)
        stats_layout.setContentsMargins(0, 0, 0, 0)

        self.time_label = QLabel()
        self.time_label.setObjectName("stat_label")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.orders_label = QLabel()
        self.orders_label.setObjectName("stat_label")
        self.orders_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.employee_label = QLabel(f"Empleado: {self.employee_name}")
        self.employee_label.setObjectName("stat_label")
        self.employee_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        stats_layout.addWidget(self.time_label)
        stats_layout.addWidget(self.orders_label)
        stats_layout.addWidget(self.employee_label)

        dashboard_layout.addWidget(stats_widget)

    def setup_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

    def update_time(self):
        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        self.time_label.setText(current_time)

    def set_employee_name(self, name):
        self.employee_name = name
        self.employee_label.setText(f"Empleado: {self.employee_name}")

    def update_total_orders(self):
        total_orders = DB_GLOBAL.get_total_orders_today()
        self.orders_label.setText(f"Ventas de Hoy: {total_orders}")

    def update_table_buttons(self):
        self.update_total_orders()
        for i, table in enumerate(self.tables):
            button = self.button_widgets[i]
            text = f"Mesa: {table.table_id}: {table.table_name}"

            if table.is_occupied:
                text += f"\nCliente ID: {table.client_id} | Venta ID: {table.sale_id}"
                button.setProperty("ocupada", "true")
            else:
                button.setProperty("ocupada", "false")

            button.setText(text)

            button.style().unpolish(button)
            button.style().polish(button)

    def handle_table_click(self, table_id):
        table = DB_GLOBAL.get_table_by_id(table_id)
        if table:
            if table.is_occupied:
                self.go_to_occupied_table_callback(table_id)
            else:
                self.go_to_client_entry_callback(table_id)