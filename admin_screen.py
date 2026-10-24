from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QTableWidget
)


class AdminWindow(QMainWindow):
    COLUMNS = ["# Order", "Customer Info", "Job Details", "Source", "Amount", "Status", "Action"]

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Screen")
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        admin_layout = QVBoxLayout(central_widget)

        # Metrics
        metrics_layout = QHBoxLayout()
        
        self.label_sales = QLabel("Sales")
        self.label_orders = QLabel("Orders")
        self.label_jobs = QLabel("Open Jobs")
        
        # Orders table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "# Order",
            "Customer Info",
            "Job Details",
            "Source",
            "Amount",
            "Status",
            "Action",
             ])
    
    # Layout [AdminWindow]
        admin_layout.addLayout(metrics_layout)
        admin_layout.addWidget(self.table)

    def refresh_table(self):
        pass