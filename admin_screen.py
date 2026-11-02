from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QTableWidget, QFrame,
    QTabWidget, QTableWidgetItem, QHeaderView, QSpinBox, QPushButton, QFormLayout
)
from dialogs import UpdateStatusDialog, CustomAlertDialog


class AdminWindow(QMainWindow):
    COLUMNS = ["# Order", "Customer Info", "Job Details", "Source", "Amount", "Status", "Action"]

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Screen")
        self.user_window = None
        self.orders = []
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.tabs.addTab(central_widget, "Main")
        self.tabs.addTab(self.build_price_page(), "Change Prices")
        self.tabs.tabBar().setDrawBase(False)
        self.tabs.setStyleSheet(
            "QTabWidget::pane { border: none; }"
            "QTabBar::tab { background-color: #f6f8fa; color: #57606a; border: 1px solid #d0d7de; border-radius: 15px; padding: 6px 18px; margin: 4px 6px 8px 0px; font-weight: bold; }"
            "QTabBar::tab:selected { background-color: #1f883d; color: #ffffff; border: 1px solid #1f883d; }"
        )
        admin_layout = QVBoxLayout(central_widget)

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

        title_orders = QLabel("Orders")
        title_orders.setStyleSheet("font-size: 18px; font-weight: bold; color: #ffffff; margin-top: 8px;")

        subtitle_orders = QLabel("Live job queue and transaction history in one place. Use the filter to focus on a stage.")
        subtitle_orders.setStyleSheet("font-size: 12px; color: #8b949e;")

        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(10)

        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Search name or order code...")

        self.combo_filter = QComboBox()
        self.combo_filter.addItems(["All Statuses", "Pending", "Printing", "Ready for Pickup", "Completed", "Cancelled"])

        filter_layout.addWidget(self.txt_search, 1)
        filter_layout.addWidget(self.combo_filter)

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

        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.txt_search.textChanged.connect(self.refresh_table)
        self.combo_filter.currentIndexChanged.connect(self.refresh_table)
        self.table.cellClicked.connect(self.cell_clicked)

        admin_layout.addLayout(metrics_layout)
        admin_layout.addWidget(title_orders)
        admin_layout.addWidget(subtitle_orders)
        admin_layout.addLayout(filter_layout)
        admin_layout.addWidget(self.table)
        self.refresh_table()

    def add_order(self, order):
        self.orders.append(order)
        self.refresh_table()

    def refresh_table(self):
        search = self.txt_search.text().strip().lower()
        status = self.combo_filter.currentText()
        self.table.setRowCount(0)
        sales = 0
        open_jobs = 0

        for order in self.orders:
            if order["status"] != "Cancelled":
                sales += order["amount"]
            if order["status"] not in ("Completed", "Cancelled"):
                open_jobs += 1

            matches_search = search in order["name"].lower() or search in order["id"].lower()
            matches_status = status == "All Statuses" or order["status"] == status
            if matches_search and matches_status:
                row = self.table.rowCount()
                self.table.insertRow(row)
                customer = "\n".join([order["name"], order["phone"], order["account"]])
                cells = [order["id"], customer, order["job"], order["source"], f"₱{order['amount']:.0f}", order["status"], "Update"]
                for column, text in enumerate(cells):
                    self.table.setItem(row, column, QTableWidgetItem(text))

        self.table.resizeRowsToContents()
        self.label_sales.setText(f"₱{sales:.0f}")
        self.label_orders.setText(str(len(self.orders)))
        self.label_jobs.setText(str(open_jobs))

    def cell_clicked(self, row, column):
        if column == 6:
            order_id = self.table.item(row, 0).text()
            self.update_status(order_id)

    def update_status(self, order_id):
        for order in self.orders:
            if order["id"] == order_id:
                dialog = UpdateStatusDialog(order_id, order["status"], self)
                if dialog.exec() == 1:
                    order["status"] = dialog.get_selected_status()
                    self.refresh_table()
                    self.user_window.update_status_row(order_id, order["status"])

    def build_price_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("Change Prices")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #ffffff;")
        subtitle = QLabel("Press Save to use the new prices on the user screen.")
        subtitle.setStyleSheet("font-size: 18px; font-weight: bold; color: #ffffff; margin-top: 8px;")

        prices = [
            ("Letter / Short and A4 paper per page", 2),
            ("Legal / Long paper per page", 3),
            ("Photo Paper per page", 25),
            ("Black and White print per page", 2),
            ("Full Color print per page", 3),
            ("Binding", 30),
            ("Lamination", 15),
        ]
        form = QFormLayout()
        self.price_spins = []
        for label, value in prices:
            spin = QSpinBox()
            spin.setRange(0, 999)
            spin.setPrefix("₱")
            spin.setValue(value)
            label_widget = QLabel(label)
            label_widget.setStyleSheet("color: #ffffff;")
            form.addRow(label_widget, spin)
            self.price_spins.append(spin)

        btn_save = QPushButton("Save Prices")
        btn_save.clicked.connect(self.save_prices)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(form)
        layout.addWidget(btn_save)
        layout.addStretch()
        return page

    def save_prices(self):
        self.user_window.set_prices(*[spin.value() for spin in self.price_spins])
        CustomAlertDialog("Prices Saved", "The user screen now uses the new prices.", self).exec()