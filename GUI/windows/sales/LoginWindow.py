from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Qt
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





class LoginWindow(QWidget):
    def __init__(self, go_to_main_window_callback):
        super().__init__()
        self.setObjectName("LoginWindow")

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QWidget()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(20)

        title = QLabel("BISONBAR\nSISTEMA DE VENTAS Y CONSULTAS")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(title)

        user_row = QHBoxLayout()
        user_label = QLabel("Usuario:")
        user_label.setObjectName("label")
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Ingrese su usuario")
        user_row.addWidget(user_label)
        user_row.addWidget(self.user_input)
        card_layout.addLayout(user_row)

        pass_row = QHBoxLayout()
        pass_label = QLabel("Contraseña:")
        pass_label.setObjectName("label")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Ingrese su contraseña")
        self.password_input.returnPressed.connect(go_to_main_window_callback)
        pass_row.addWidget(pass_label)
        pass_row.addWidget(self.password_input)
        card_layout.addLayout(pass_row)

        login_button = QPushButton("Ingresar")
        login_button.setObjectName("login_button")
        login_button.clicked.connect(go_to_main_window_callback)
        card_layout.addWidget(login_button)

        main_layout.addWidget(card)

        load_stylesheet(self, "login_window.css")







