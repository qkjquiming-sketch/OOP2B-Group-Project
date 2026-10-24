from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QSpinBox, QCheckBox, QPushButton, QTableWidget
)


class UserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Screen")
        self.last_order_id = None
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        user_layout = QVBoxLayout(central_widget)
        user_layout.setContentsMargins(20, 20, 20, 20)
        user_layout.setSpacing(15)

    def place_order(self):
        pass