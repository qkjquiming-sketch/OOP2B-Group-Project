from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QTableWidget, QFrame
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
        metrics_layout.setSpacing(12)

        card_sales = QFrame()
        card_sales.setStyleSheet("background-color: #0d1712; border: 1px solid #1a2e23; border-radius: 8px; padding: 10px;")
        layout_sales = QVBoxLayout(card_sales)
        lbl_sales_title = QLabel("Sales Today")
        lbl_sales_title.setStyleSheet("font-size: 11px; color: #8b949e;")
        self.label_sales = QLabel("₱1,090")
        self.label_sales.setStyleSheet("font-size: 22px; font-weight: bold; color: #ffffff;")
        layout_sales.addWidget(lbl_sales_title)
        layout_sales.addWidget(self.label_sales)

        card_orders = QFrame()
        card_orders.setStyleSheet("background-color: #0d1712; border: 1px solid #1a2e23; border-radius: 8px; padding: 10px;")
        layout_orders = QVBoxLayout(card_orders)
        lbl_orders_title = QLabel("Total Orders")
        lbl_orders_title.setStyleSheet("font-size: 11px; color: #8b949e;")
        self.label_orders = QLabel("6")
        self.label_orders.setStyleSheet("font-size: 22px; font-weight: bold; color: #ffffff;")
        layout_orders.addWidget(lbl_orders_title)
        layout_orders.addWidget(self.label_orders)

        card_jobs = QFrame()
        card_jobs.setStyleSheet("background-color: #0d1712; border: 1px solid #1a2e23; border-radius: 8px; padding: 10px;")
        layout_jobs = QVBoxLayout(card_jobs)
        lbl_jobs_title = QLabel("Open Jobs")
        lbl_jobs_title.setStyleSheet("font-size: 11px; color: #8b949e;")
        self.label_jobs = QLabel("4")
        self.label_jobs.setStyleSheet("font-size: 22px; font-weight: bold; color: #ffffff;")
        layout_jobs.addWidget(lbl_jobs_title)
        layout_jobs.addWidget(self.label_jobs)

        metrics_layout.addWidget(card_sales)
        metrics_layout.addWidget(card_orders)
        metrics_layout.addWidget(card_jobs)

        # Orders Section Title & Subtitle
        title_orders = QLabel("Orders")
        title_orders.setStyleSheet("font-size: 18px; font-weight: bold; color: #ffffff; margin-top: 8px;")

        subtitle_orders = QLabel("Live job queue and transaction history in one place. Use the filter to focus on a stage.")
        subtitle_orders.setStyleSheet("font-size: 12px; color: #8b949e;")

        # Search Bar & Status Filter
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(10)

        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Search name or order code...")

        self.combo_filter = QComboBox()
        self.combo_filter.addItems(["All Statuses", "Pending", "Processing", "Ready", "Completed", "Cancelled"])

        filter_layout.addWidget(self.txt_search, 1)
        filter_layout.addWidget(self.combo_filter)

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
        admin_layout.addWidget(title_orders)
        admin_layout.addWidget(subtitle_orders)
        admin_layout.addLayout(filter_layout)
        admin_layout.addWidget(self.table)

    def refresh_table(self):
        pass
