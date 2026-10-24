from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QSpinBox, QCheckBox, QPushButton, QTableWidget, QFrame,
    QButtonGroup
    
)

# USER SCREEN
class UserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Screen")
        self.setStyleSheet("backround-color: #0d1117; color: #cd9d1d9; font-family: 'Segou UI', sans-serif; font-size: 13px;")
        self.init_ui()


    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(8, 8, 8, 8)

        title = QLabel("New Print Order Form")
        header.setStyleSheet("font size: 20px; font-weight: bold; color: #ffffff; padding-bottom: 8px;")
        title.setObjectName("title")
        root.addWidget(title)
        
        subtitle = QLabel("Select options below to compute total price. ")
        subtitle.setObjectName("subtitle")
        root.addWidget(subtitle)

        columns = QHBoxLayout()
        columns.addLayout(self.build_form(), 1)
        columns.addLayout(self.build_right_panel(), 1)
        root.addLayout(columns)
    
    # Makes 2 columns for Line 1
    def labeled(self, text, widget, style_class="field-label"):
        column = QVBoxLayout()
        column.setSpacing(6)
        label = QLabel(text)
        label.setStyleSheet("font-size: 12px; font-weight: 600; color: #8b949e;")
        label.setProperty("class", style_class)
        column.addWidget(label)
        column.addWidget(widget)
        return column

    # Left Side : Order form
    def build_form(self):
        form = QVBoxLayout()

        input_style = "backround-color: #21262d; border: 1px solid #30363d; border-radius: #f0f6fc; padding: 6px 10px;"
        
    # ----- Line 1 : Customer name and phone number -----
        # Customer name
        self.txt_name = QLineEdit()
        self.txt_name.setPlaceholderText("e.g. Juan Dela Cruz")
        # Phone number
        self.txt_phone = QLineEdit()
        self.txt_phone.setPlaceholderText("0917-XXX-XXXX")

        customer_info = QHBoxLayout()
        customer_info.setSpacing(16)
        customer_info.addLayout(self.labeled("Customer Name *", self.txt_name), 1)
        customer_info.addLayout(self.labeled("Contact Number", self.txt_phone), 1)
        form.addLayout(customer_info)       # Move this later
      
    # ----- Line 2 : File Source -----
        file_source = QLabel("File Source: ")
        file_source.setStyleSheet("font-size: 12px; font-weight: 600; color: #8b949e;")
        file_source.setProperty("class", "field-label")
        
        # Layout
        source_row = QHBoxLayout()
        form.addLayout(source_row)
        source_row.setSpacing(8)
        source_row.addWidget(file_source)
        self.source_group = QButtonGroup(self)
        self.source_group.setExclusive(True)
        
        
        self.button_gmail = QPushButton("Gmail")
        self.button_fb = QPushButton("Facebook/Messenger")

        style_unselected = "background-color: #21262d; color: #8b949e; border: 1px solid #30363d; border-radius: 6px; padding: 8px 16px; font-weight: 600;"
        style_selected = "background-color: #238636; color: #ffffff; border: none; border-radius: 6px; padding: 8px 16px; font-weight: bold;"

        
        for button in (self.button_gmail, self.button_fb):
            button.setProperty("class", "segment")
            button.setCheckable(True)
            button.setFixedHeight(40)
            self.source_group.addButton(button)
            source_row.addWidget(button, 1)
            
        def update_selected(clicked):
            for button in self.source_group.buttons():
                button.setStyleSheet(style_selected if button is clicked else style_unselected)
                button.setProperty("class", "primary" if button is clicked else "segment")
                button.style().unpolish(button)
                button.style().polish(button)
                  
        
        self.source_group.buttonClicked.connect(update_selected)
        
        # Set default selection
        self.button_gmail.setChecked(True)
        update_selected(self.button_gmail)





        form.addStretch()
        return form


    # RIGHT: price + status
    def build_right_panel(self):
        panel = QVBoxLayout()


        panel.addWidget(QLabel("Price Breakdown"))
        self.lbl_breakdown = QLabel()
        panel.addWidget(self.lbl_breakdown)


        self.lbl_total = QLabel()
        panel.addWidget(self.lbl_total)


        self.btn_place_order = QPushButton("Place Order")
        self.btn_place_order.clicked.connect(self.place_order)
        panel.addWidget(self.btn_place_order)


        panel.addWidget(QLabel("Order Status"))
        self.status_table = QTableWidget()
        self.status_table.setColumnCount(3)
        self.status_table.setHorizontalHeaderLabels(["Order", "Job", "Status"])
        panel.addWidget(self.status_table)

        bl_price = QLabel("Price Breakdown")
        lbl_price.setStyleSheet("font-size: 14px; font-weight: bold; color: #ffffff;")
        panel.addWidget(lbl_price)

        self.lbl_breakdown = QLabel()
        panel.addWidget(self.lbl_breakdown)

        self.lbl_total = QLabel()
        panel.addWidget(self.lbl_total)

        self.btn_place_order = QPushButton("Place Order")
        self.btn_place_order.setStyleSheet("background-color: #238636; color: #ffffff; font-weight: bold; border-radius: 6px; padding: 8px 16px;")
        self.btn_place_order.clicked.connect(self.place_order)
        panel.addWidget(self.btn_place_order)

        lbl_status = QLabel("Order Status")
        lbl_status.setStyleSheet("font-size: 14px; font-weight: bold; color: #ffffff;")
        panel.addWidget(lbl_status)

        self.status_table = QTableWidget()
        self.status_table.setColumnCount(3)
        self.status_table.setHorizontalHeaderLabels(["Order", "Job", "Status"])
        self.status_table.setStyleSheet("""
            QTableWidget {
                background-color: #161b22;
                border: 1px solid #30363d;
                gridline-color: #21262d;
                color: #c9d1d9;
            }
            QHeaderView::section {
                background-color: #21262d;
                color: #8b949e;
                font-weight: bold;
                border: none;
                border-bottom: 1px solid #30363d;
            }
        """)
        panel.addWidget(self.status_table)

        return panel

    def place_order(self):
        pass


        return panel


    def place_order(self):
        pass
