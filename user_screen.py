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
        self.init_ui()


    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(8, 8, 8, 8)

        title = QLabel("New Print Order Form")
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
        label.setProperty("class", style_class)
        column.addWidget(label)
        column.addWidget(widget)
        return column

    # Left Side : Order form
    def build_form(self):
        form = QVBoxLayout()

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
        
        for button in (self.button_gmail, self.button_fb):
            button.setProperty("class", "segment")
            button.setCheckable(True)
            button.setFixedHeight(40)
            self.source_group.addButton(button)
            source_row.addWidget(button, 1)
            
        def update_selected(clicked):
            for button in self.source_group.buttons():
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


        return panel


    def place_order(self):
        pass