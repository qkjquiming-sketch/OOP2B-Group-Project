from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QSpinBox, QCheckBox, QPushButton, QTableWidget, QFrame,
    
)


def make_label(text, style_class=""):
    label = QLabel(text)
    if style_class:
        label.setProperty("class", style_class)
    return label

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
        
        # Header
        user_header = QLabel("New Print Order")
        user_header.setObjectName("Title")

        # Columns
        user_columns = QHBoxLayout()
        user_columns.setSpacing(16)

        # Layout
        user_layout.addWidget(user_header)
        user_columns.addWidget(self.left_panel(), 5)
        user_columns.addLayout(self.right_panel(), 4)
        user_layout.addLayout(user_columns, 1)
        
        # >> To-Do 

        # self.get_total_price()
        # self.refresh_status()
        
    def left_panel(self):
        left_card = QFrame()
        left_card.setProperty("class", "card")
        
        # Left Card Layout
        left_card_layout = QVBoxLayout(left_card)
        left_card_layout.setContentsMargins(16, 16, 16, 16)
        left_card_layout.setSpacing(8)
        
        # Customer Info Section
        left_card_layout.addWidget(make_label("Customer Information", "section"))
        
        left_card_layout.addWidget(make_label("Customer Name", "field-label"))
        

    def right_panel(self):
        pass
        
    def get_total_price():
        pass
    
    def refresh_status():
        pass
    
    
    def place_order(self):
        pass