from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QInputDialog
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


class OccupiedTableWindow(QWidget):
    def __init__(self, on_main_menu, on_add_order):
        super().__init__()
        self.setObjectName("QueryWindow")
        self.on_main_menu = on_main_menu
        self.on_add_order = on_add_order
        self.table_id = -1
        self.sale_id = -1

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QWidget()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(20)
        card_layout.setContentsMargins(40, 40, 40, 40)

        self.title = QLabel("Mesa Ocupada")
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self.title)

        self.add_order_button = QPushButton("Agregar Orden")
        self.add_order_button.setObjectName("add_order_button")
        self.add_order_button.clicked.connect(self._on_add_order_click)
        card_layout.addWidget(self.add_order_button)

        self.finalize_button = QPushButton("Finalizar Venta")
        self.finalize_button.setObjectName("finalize_button")
        self.finalize_button.clicked.connect(self._finalize_sale)
        card_layout.addWidget(self.finalize_button)

        self.return_button = QPushButton("Volver al Menú Principal")
        self.return_button.setObjectName("return_button")
        self.return_button.clicked.connect(self.on_main_menu)
        card_layout.addWidget(self.return_button)

        self.layout.addWidget(card)

        load_stylesheet(self, "occupied_table_window.css")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.on_main_menu()
        else:
            super().keyPressEvent(event)

    def set_data(self, table_id):
        self.table_id = table_id
        table = DB_GLOBAL.get_table_by_id(table_id)
        if table:
            self.sale_id = table.sale_id
            self.title.setText(f"Mesa {table.table_id}: {table.table_name}")
        else:
            self.sale_id = -1
            self.title.setText("Mesa Ocupada")

    def _on_add_order_click(self):
        if self.sale_id != -1 and self.table_id != -1:
            self.on_add_order(self.sale_id, self.table_id)

    def format_ticket(self, total, payment_method, data):
        header = f"""BISONBAR S.A. de C.V
Pedro de Alba, Niños Héroes, Ciudad Universitaria, 66451 San Nicolás de los Garza, N.L.
Telefono: 81 8329 4030
------------------------------------
------------------------------------
ID VENTA: {data['venta_id']}
{data['fecha']} {data['hora']}
EMPLEADO ATENDIENDO: {data['empleado_nombre']}
------------------------------------
"""

        details = f"\n{'PRODUCTO'.ljust(20)} {'CANT.'.rjust(5)} {'PRECIO'.rjust(8)}\n"

        for product_name, quantity, price in data['orden_detalles']:
            product_name_padded = product_name[:20].ljust(20)
            quantity_str = str(quantity).rjust(5)
            price_str = f"${price:.2f}".rjust(8)
            details += f"{product_name_padded} {quantity_str} {price_str}\n"

        footer = f"""
------------------------------------
TOTAL: {''.ljust(20)} ${total:.2f}

TIPO PAGO: {payment_method}
"""
        return header + details + footer

    def _finalize_sale(self):
        if self.sale_id != -1:
            payment_methods = ["Efectivo", "Tarjeta"]
            payment_method, ok = QInputDialog.getItem(
                self,
                "Método de Pago",
                "Seleccione el método de pago:",
                payment_methods,
                0,
                False
            )

            if not ok or not payment_method:
                return

            try:
                total = DB_GLOBAL.finalize_sale(self.sale_id)
                ticket_data = DB_GLOBAL.get_sale_data_for_ticket(self.sale_id)

                if not ticket_data:
                    QMessageBox.critical(self, "Error",
                                         "Venta finalizada, pero no se pudieron obtener los detalles del ticket.")
                else:
                    ticket_message = self.format_ticket(total, payment_method, ticket_data)

                    msg_box = QMessageBox(self)
                    msg_box.setWindowTitle("Venta Finalizada")
                    msg_box.setText(f"Venta {self.sale_id} finalizada. Total: ${total:.2f}")
                    msg_box.setInformativeText("Ticket de Venta:")
                    msg_box.setDetailedText(ticket_message)
                    msg_box.setTextFormat(
                        Qt.PlainText)
                    msg_box.setIcon(QMessageBox.Information)
                    msg_box.exec()

                self.on_main_menu()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo finalizar la venta: {e}")