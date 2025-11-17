import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout,
    QTabWidget, QScrollArea, QGridLayout, QPushButton, QButtonGroup,
    QHBoxLayout, QLabel, QMessageBox
)
from PySide6.QtGui import QFont
from PySide6.QtCore import QDateTime, QTimer, Qt
from app.bar_db import DB_GLOBAL

# --- Environment Setup ---
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# --- Window Imports ---
from windows.sales.LoginWindow import LoginWindow
from windows.sales.ClientEntryWindow import ClientEntryWindow
from windows.sales.NewClientWindow import NewClientWindow
from windows.sales.OccupiedTableWindow import OccupiedTableWindow
from windows.sales.AddOrderWindow import AddOrderWindow
from windows.queries import (
    ClientQueryWindow, ProductQueryWindow, SaleQueryWindow,
    ProveedorQueryWindow, PromocionQueryWindow, TurnoQueryWindow
)
from windows.data_input import (
    ClientInputWindow, TableInputWindow, PurchaseOrderInputWindow,
    SupplierInputWindow, ProductTypeInputWindow
)
from windows.administrative import (
    PromotionInputWindow as AdminPromotionInputWindow,
    ShiftInputWindow as AdminShiftInputWindow,
    UserInputWindow as AdminUserInputWindow,
    EmployeeInputWindow,
    UserQueryWindow,
    EmployeeQueryWindow
)


def load_stylesheet(widget, css_file_name):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        resources_dir = os.path.join(current_dir, '..', 'resources')
        file_path = os.path.join(resources_dir, css_file_name)

        with open(file_path, 'r', encoding='utf-8') as f:
            style = f.read()
            widget.setStyleSheet(style)
    except Exception as e:
        print(f"Error loading stylesheet {css_file_name}: {e}")


class MainApp(QMainWindow):
    def __init__(self):

        super().__init__()
        self.employee_label = None
        self.user_input_window = None
        self.orders_label = None
        self.time_label = None
        self.supplier_input_window = None
        self.dashboard_widget = None
        self.shift_input_window = None
        self.product_type_input_window = None
        self.client_input_window = None
        self.promotion_input_window = None
        self.purchase_order_input_window = None
        self.table_input_window = None
        self.data_input_hub = None
        self.query_hub = None
        self.table_buttons_group = None
        self.button_widgets = None
        self.query_stack = None
        self.client_query_window = None
        self.product_query_window = None
        self.sale_query_window = None
        self.data_input_stack = None
        self.employee_query_window = None
        self.proveedor_query_window = None
        self.turno_query_window = None
        self.promocion_query_window = None
        self.timer = None
        self.tables = None
        self.administrative_tab = None
        self.admin_tab_index = None
        self.administrative_hub = None
        self.administrative_stack = None
        self.employee_input_window = None
        self.user_query_window = None
        self.queries_dashboard = None
        self.data_input_dashboard = None
        self.admin_dashboard = None

        self.setWindowTitle("BISONBAR")
        self.setMinimumSize(800, 600)

        self.current_role = None
        self.current_employee_name = None

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.login_window = LoginWindow(self.attempt_login)

        # ADDED: Relocated EmployeeQueryWindow instantiation
        self.employee_query_window = EmployeeQueryWindow(self.go_to_administrative_hub)

        self.main_app_widget = QWidget()
        main_app_layout = QVBoxLayout(self.main_app_widget)
        main_app_layout.setContentsMargins(0, 0, 0, 0)
        main_app_layout.setSpacing(0)

        self.employee_name = "N/A"
        self.setup_dashboard()
        main_app_layout.addWidget(self.dashboard_widget)

        self.tab_widget = QTabWidget()
        main_app_layout.addWidget(self.tab_widget)

        self.tables_tab = QWidget()
        self.setup_tables_tab()
        self.mesas_tab_index = self.tab_widget.addTab(self.tables_tab, "Mesas")

        self.queries_tab = QWidget()
        self.setup_queries_tab()
        self.consultas_tab_index = self.tab_widget.addTab(self.queries_tab, "Consultas")

        self.data_input_tab = QWidget()
        self.setup_data_input_tab()
        self.datos_tab_index = self.tab_widget.addTab(self.data_input_tab, "Ingreso de Datos")

        self.administrative_tab = QWidget()
        self.setup_administrative_tab()
        self.admin_tab_index = self.tab_widget.addTab(self.administrative_tab, "Administración")

        self.setup_timer()
        self.update_total_orders()
        load_stylesheet(self.main_app_widget, "main_window.css")

        self.client_entry_window = ClientEntryWindow(self.show_main_window, self.go_to_new_client)
        self.new_client_window = NewClientWindow(self.show_main_window, self.go_to_client_entry)
        self.occupied_table_window = OccupiedTableWindow(self.show_main_window, self.go_to_add_order)
        self.add_order_window = AddOrderWindow(self.go_to_occupied_table)

        self.stack.addWidget(self.login_window)
        self.stack.addWidget(self.main_app_widget)
        self.stack.addWidget(self.client_entry_window)
        self.stack.addWidget(self.new_client_window)
        self.stack.addWidget(self.occupied_table_window)
        self.stack.addWidget(self.add_order_window)

        self.stack.setCurrentIndex(0)

    def attempt_login(self):
        username = self.login_window.user_input.text()
        password = self.login_window.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Usuario y contraseña no pueden estar vacíos.")
            return

        employee_name, position_name = DB_GLOBAL.authenticate_user(username, password)

        if employee_name is None:
            QMessageBox.warning(self, "Error", "Credenciales incorrectas.")
            self.login_window.password_input.clear()
        elif position_name == "Limpieza":
            QMessageBox.critical(self, "Acceso Denegado", "Este usuario no tiene permisos para acceder al sistema.")
            self.login_window.password_input.clear()
        else:
            print(f"Usuario valido: {employee_name}, Puesto: {position_name}")
            self.current_employee_name = employee_name
            self.current_role = position_name
            self.set_employee_name(self.current_employee_name)
            self.show_main_window()

            self.login_window.user_input.clear()
            self.login_window.password_input.clear()

    def apply_role_permissions(self):

        self.tab_widget.setTabEnabled(self.mesas_tab_index, True)
        self.tab_widget.setTabEnabled(self.consultas_tab_index, True)
        self.tab_widget.setTabEnabled(self.datos_tab_index, True)
        self.tab_widget.setTabEnabled(self.admin_tab_index, True)

        self.client_query_window.edit_toggle_button.setVisible(True)
        self.proveedor_query_window.edit_toggle_button.setVisible(True)
        self.promocion_query_window.edit_toggle_button.setVisible(True)
        self.turno_query_window.edit_toggle_button.setVisible(True)

        # EmployeeQueryWindow is now in Admin and should not be editable
        self.employee_query_window.edit_toggle_button.setVisible(True)
        self.employee_query_window.edit_toggle_button.setEnabled(False)

        if self.current_role == "Mesero" or self.current_role == "Cajero":

            print("Aplicando rol: Ventas")
            self.tab_widget.setTabEnabled(self.consultas_tab_index, False)
            self.tab_widget.setTabEnabled(self.datos_tab_index, False)
            self.tab_widget.setTabEnabled(self.admin_tab_index, False)
            self.tab_widget.setCurrentIndex(self.mesas_tab_index)

        elif self.current_role == "Cocinero":

            print("Aplicando rol: Consultas")
            self.tab_widget.setTabEnabled(self.mesas_tab_index, False)
            self.tab_widget.setTabEnabled(self.datos_tab_index, False)
            self.tab_widget.setTabEnabled(self.admin_tab_index, False)
            self.tab_widget.setCurrentIndex(self.consultas_tab_index)

            self.client_query_window.edit_toggle_button.setVisible(False)
            self.proveedor_query_window.edit_toggle_button.setVisible(False)
            self.promocion_query_window.edit_toggle_button.setVisible(False)
            self.turno_query_window.edit_toggle_button.setVisible(False)

            self.sale_query_window.edit_toggle_button.setVisible(False)

        elif self.current_role == "Administrador":

            print("Aplicando rol: Administrador")

            self.tab_widget.setCurrentIndex(self.admin_tab_index)

        else:

            print(f"Aplicando rol por defecto (Ventas) para: {self.current_role}")
            self.tab_widget.setTabEnabled(self.consultas_tab_index, False)
            self.tab_widget.setTabEnabled(self.datos_tab_index, False)
            self.tab_widget.setTabEnabled(self.admin_tab_index, False)
            self.tab_widget.setCurrentIndex(self.mesas_tab_index)

    def show_main_window(self):

        self.apply_role_permissions()
        self.update_table_buttons()
        self.stack.setCurrentWidget(self.main_app_widget)

    def go_to_client_entry(self, table_id):
        self.client_entry_window.set_table(table_id)
        self.stack.setCurrentWidget(self.client_entry_window)

    def go_to_new_client(self, table_id):
        self.new_client_window.set_data(table_id)
        self.stack.setCurrentWidget(self.new_client_window)

    def go_to_occupied_table(self, table_id):
        self.occupied_table_window.set_data(table_id)
        self.stack.setCurrentWidget(self.occupied_table_window)

    def go_to_add_order(self, sale_id, table_id):
        self.add_order_window.set_data(sale_id, table_id)
        self.stack.setCurrentWidget(self.add_order_window)

    def setup_tables_tab(self):
        tables_layout = QVBoxLayout(self.tables_tab)
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

    def handle_table_click(self, table_id):
        table = DB_GLOBAL.get_table_by_id(table_id)
        if table:
            if table.is_occupied:
                self.go_to_occupied_table(table_id)
            else:
                self.go_to_client_entry(table_id)

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

    def setup_queries_tab(self):
        queries_main_layout = QVBoxLayout(self.queries_tab)

        # ADDED: Dashboard for Queries Tab
        self.queries_dashboard = QLabel()
        self.queries_dashboard.setObjectName("tab_dashboard_label")
        queries_main_layout.addWidget(self.queries_dashboard)
        self.update_queries_dashboard()

        self.query_stack = QStackedWidget()
        queries_main_layout.addWidget(self.query_stack)

        self.query_hub = QWidget()
        self.query_hub.setObjectName("query_hub_widget")
        hub_layout = QGridLayout(self.query_hub)
        hub_layout.setSpacing(20)
        hub_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        product_button = QPushButton("Consultas de Productos")
        client_button = QPushButton("Consultas de Clientes")
        sale_button = QPushButton("Consultas de Ventas")
        # employee_button removed due to relocation
        proveedor_button = QPushButton("Consultas de Proveedores")
        promocion_button = QPushButton("Consultas de Promociones")
        turno_button = QPushButton("Consultas de Turnos")

        hub_layout.addWidget(product_button, 0, 0)
        hub_layout.addWidget(client_button, 0, 1)
        hub_layout.addWidget(sale_button, 1, 0)
        hub_layout.addWidget(proveedor_button, 1, 1)
        hub_layout.addWidget(promocion_button, 2, 0)
        hub_layout.addWidget(turno_button, 2, 1)

        self.product_query_window = ProductQueryWindow(self.go_to_query_hub)
        self.client_query_window = ClientQueryWindow(self.go_to_query_hub)
        self.sale_query_window = SaleQueryWindow(self.go_to_query_hub)
        # self.employee_query_window is moved to admin hub
        self.proveedor_query_window = ProveedorQueryWindow(self.go_to_query_hub)
        self.promocion_query_window = PromocionQueryWindow(self.go_to_query_hub)
        self.turno_query_window = TurnoQueryWindow(self.go_to_query_hub)

        self.query_stack.addWidget(self.query_hub)
        self.query_stack.addWidget(self.product_query_window)
        self.query_stack.addWidget(self.client_query_window)
        self.query_stack.addWidget(self.sale_query_window)
        # self.query_stack.addWidget(self.employee_query_window) # REMOVED
        self.query_stack.addWidget(self.proveedor_query_window)
        self.query_stack.addWidget(self.promocion_query_window)
        self.query_stack.addWidget(self.turno_query_window)

        product_button.clicked.connect(self.go_to_product_query)
        client_button.clicked.connect(self.go_to_client_query)
        sale_button.clicked.connect(self.go_to_sale_query)
        # employee_button.clicked.connect(self.go_to_employee_query) # REMOVED
        proveedor_button.clicked.connect(self.go_to_proveedor_query)
        promocion_button.clicked.connect(self.go_to_promocion_query)
        turno_button.clicked.connect(self.go_to_turno_query)

        load_stylesheet(self.query_hub, "query_windows.css")
        self.query_stack.setCurrentWidget(self.query_hub)

    def go_to_product_query(self):
        self.product_query_window.load_product_search()
        self.query_stack.setCurrentWidget(self.product_query_window)

    def go_to_client_query(self):
        self.client_query_window.load_client_search()
        self.query_stack.setCurrentWidget(self.client_query_window)

    def go_to_sale_query(self):
        self.sale_query_window.load_sales_by_date()
        self.query_stack.setCurrentWidget(self.sale_query_window)

    # Removed go_to_employee_query from here due to relocation

    def go_to_proveedor_query(self):
        self.proveedor_query_window.load_data()
        self.query_stack.setCurrentWidget(self.proveedor_query_window)

    def go_to_promocion_query(self):
        self.promocion_query_window.load_data()
        self.query_stack.setCurrentWidget(self.promocion_query_window)

    def go_to_turno_query(self):
        self.turno_query_window.load_data()
        self.query_stack.setCurrentWidget(self.turno_query_window)

    def go_to_query_hub(self):
        self.query_stack.setCurrentWidget(self.query_hub)
        self.update_queries_dashboard()  # ADDED: Update dashboard on return

    def setup_data_input_tab(self):
        data_input_main_layout = QVBoxLayout(self.data_input_tab)

        # ADDED: Dashboard for Data Input Tab
        self.data_input_dashboard = QLabel()
        self.data_input_dashboard.setObjectName("tab_dashboard_label")
        data_input_main_layout.addWidget(self.data_input_dashboard)
        self.update_data_input_dashboard()

        self.data_input_stack = QStackedWidget()
        data_input_main_layout.addWidget(self.data_input_stack)

        self.data_input_hub = QWidget()
        self.data_input_hub.setObjectName("query_hub_widget")
        hub_layout = QGridLayout(self.data_input_hub)
        hub_layout.setSpacing(20)
        hub_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        client_button = QPushButton("Agregar Cliente")
        table_button = QPushButton("Agregar Mesa")
        purchase_order_button = QPushButton("Agregar Orden de Compra")
        supplier_button = QPushButton("Agregar Proveedor")
        product_type_button = QPushButton("Agregar Tipo de Producto")

        hub_layout.addWidget(client_button, 0, 0)
        hub_layout.addWidget(table_button, 0, 1)
        hub_layout.addWidget(purchase_order_button, 1, 0)
        hub_layout.addWidget(supplier_button, 1, 1)
        hub_layout.addWidget(product_type_button, 2, 0)

        self.client_input_window = ClientInputWindow(self.go_to_data_input_hub)
        self.table_input_window = TableInputWindow(self.go_to_data_input_hub)
        self.purchase_order_input_window = PurchaseOrderInputWindow(self.go_to_data_input_hub)
        self.supplier_input_window = SupplierInputWindow(self.go_to_data_input_hub)
        self.product_type_input_window = ProductTypeInputWindow(self.go_to_data_input_hub)

        self.data_input_stack.addWidget(self.data_input_hub)
        self.data_input_stack.addWidget(self.client_input_window)
        self.data_input_stack.addWidget(self.table_input_window)
        self.data_input_stack.addWidget(self.purchase_order_input_window)
        self.data_input_stack.addWidget(self.supplier_input_window)
        self.data_input_stack.addWidget(self.product_type_input_window)

        client_button.clicked.connect(lambda: self.data_input_stack.setCurrentWidget(self.client_input_window))
        table_button.clicked.connect(lambda: self.data_input_stack.setCurrentWidget(self.table_input_window))
        purchase_order_button.clicked.connect(self.go_to_purchase_order_input)
        supplier_button.clicked.connect(lambda: self.data_input_stack.setCurrentWidget(self.supplier_input_window))
        product_type_button.clicked.connect(
            lambda: self.data_input_stack.setCurrentWidget(self.product_type_input_window))

        load_stylesheet(self.data_input_hub, "query_windows.css")
        self.data_input_stack.setCurrentWidget(self.data_input_hub)

    def go_to_data_input_hub(self):
        self.data_input_stack.setCurrentWidget(self.data_input_hub)
        self.update_data_input_dashboard()  # ADDED: Update dashboard on return

    def go_to_purchase_order_input(self):
        self.purchase_order_input_window.load_data()
        self.data_input_stack.setCurrentWidget(self.purchase_order_input_window)

    def setup_administrative_tab(self):
        administrative_main_layout = QVBoxLayout(self.administrative_tab)

        # ADDED: Dashboard for Administration Tab
        self.admin_dashboard = QLabel()
        self.admin_dashboard.setObjectName("tab_dashboard_label")
        administrative_main_layout.addWidget(self.admin_dashboard)
        self.update_admin_dashboard()

        self.administrative_stack = QStackedWidget()
        administrative_main_layout.addWidget(self.administrative_stack)

        self.administrative_hub = QWidget()
        self.administrative_hub.setObjectName("query_hub_widget")
        hub_layout = QGridLayout(self.administrative_hub)
        hub_layout.setSpacing(20)
        hub_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        promotion_button = QPushButton("Agregar Promoción")
        shift_button = QPushButton("Agregar Turno")
        user_button = QPushButton("Agregar Usuario")
        employee_button = QPushButton("Agregar Empleado")
        user_query_button = QPushButton("Consulta de Usuarios")
        employee_query_button = QPushButton("Consultas de Personal")  # ADDED RELOCATED QUERY

        hub_layout.addWidget(promotion_button, 0, 0)
        hub_layout.addWidget(shift_button, 0, 1)
        hub_layout.addWidget(user_button, 1, 0)
        hub_layout.addWidget(employee_button, 1, 1)
        hub_layout.addWidget(user_query_button, 2, 0)
        hub_layout.addWidget(employee_query_button, 2, 1)  # ADDED RELOCATED QUERY

        self.promotion_input_window = AdminPromotionInputWindow(self.go_to_administrative_hub)
        self.shift_input_window = AdminShiftInputWindow(self.go_to_administrative_hub)
        self.user_input_window = AdminUserInputWindow(self.go_to_administrative_hub)
        self.employee_input_window = EmployeeInputWindow(self.go_to_administrative_hub)
        self.user_query_window = UserQueryWindow(self.go_to_administrative_hub)
        # self.employee_query_window is instantiated in __init__

        self.administrative_stack.addWidget(self.administrative_hub)
        self.administrative_stack.addWidget(self.promotion_input_window)
        self.administrative_stack.addWidget(self.shift_input_window)
        self.administrative_stack.addWidget(self.user_input_window)
        self.administrative_stack.addWidget(self.employee_input_window)
        self.administrative_stack.addWidget(self.user_query_window)
        self.administrative_stack.addWidget(self.employee_query_window)  # ADDED RELOCATED QUERY

        promotion_button.clicked.connect(self.go_to_admin_promotion_input)
        shift_button.clicked.connect(self.go_to_admin_shift_input)
        user_button.clicked.connect(self.go_to_admin_user_input)
        employee_button.clicked.connect(self.go_to_admin_employee_input)
        user_query_button.clicked.connect(self.go_to_admin_user_query)
        employee_query_button.clicked.connect(self.go_to_employee_query_admin)  # ADDED RELOCATED QUERY METHOD

        load_stylesheet(self.administrative_hub, "query_windows.css")
        self.administrative_stack.setCurrentWidget(self.administrative_hub)

    def go_to_admin_promotion_input(self):
        self.promotion_input_window.load_product_data()
        self.administrative_stack.setCurrentWidget(self.promotion_input_window)

    def go_to_admin_shift_input(self):

        self.administrative_stack.setCurrentWidget(self.shift_input_window)

    def go_to_admin_user_input(self):
        self.user_input_window.load_employees()
        self.administrative_stack.setCurrentWidget(self.user_input_window)

    def go_to_admin_employee_input(self):
        self.employee_input_window.load_data()
        self.administrative_stack.setCurrentWidget(self.employee_input_window)

    def go_to_admin_user_query(self):
        self.user_query_window.load_data()
        self.administrative_stack.setCurrentWidget(self.user_query_window)

    def go_to_employee_query_admin(self):  # ADDED RELOCATED QUERY METHOD
        self.employee_query_window.load_personal_list()
        self.administrative_stack.setCurrentWidget(self.employee_query_window)

    def go_to_administrative_hub(self):
        self.administrative_stack.setCurrentWidget(self.administrative_hub)
        self.update_admin_dashboard()  # ADDED: Update dashboard on return

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

    # ADDED: Dashboard Update Methods
    def update_queries_dashboard(self):
        total_products = DB_GLOBAL.get_total_products()
        self.queries_dashboard.setText(f"Estadísticas - Total de Productos: {total_products}")

    def update_data_input_dashboard(self):
        total_suppliers = DB_GLOBAL.get_total_suppliers()
        self.data_input_dashboard.setText(f"Estadísticas - Total de Proveedores: {total_suppliers}")

    def update_admin_dashboard(self):
        total_employees = DB_GLOBAL.get_total_employees()
        self.admin_dashboard.setText(f"Estadísticas - Total de Empleados: {total_employees}")

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


# --- Main Execution ---
if __name__ == "__main__":
    DB_GLOBAL.start_connection(
        host="localhost",
        user="root",
        password="",
        database_name="BAR"
    )

    app = QApplication(sys.argv)
    app.setFont(QFont("Arial", 14))
    window = MainApp()
    window.show()
    sys.exit(app.exec())