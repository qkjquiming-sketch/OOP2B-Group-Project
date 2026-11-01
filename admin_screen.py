from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QTableWidget, QFrame,
    QTabWidget, QTableWidgetItem, QHeaderView, QSpinBox,
    QPushButton, QFormLayout,
)

from dialogs import CustomAlertDialog
from config import Prices, Statuses


class AdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Screen")
        self.user_window = None
        self.orders = [] 
        self.init_ui()

    def init_ui(self):
        # ----- Widgets -----
        central_widget = QWidget()
        self.adminWindowTabs = QTabWidget()
        
        # Metric cards
        salesCard = QFrame()
        salesTitleLabel = QLabel("Sales Today")
        self.salesLabel = QLabel("Sales Today")    # Placeholder
        
        ordersCard = QFrame()
        ordersTitleLabel = QLabel("Total Orders")
        self.ordersLabel = QLabel("Total Orders")  # Placeholder
        
        jobsCard = QFrame()
        jobsTitleLabel = QLabel("Open Jobs")
        self.jobsLabel = QLabel("Open Jobs")   # Placeholder
        
        # Orders heading
        ordersTitle = QLabel("Orders")
        ordersSubtitle = QLabel(
            "Jobs queue and transaction history."
        )
        
        # Search and filter
        self.text_search = QLineEdit()
        self.text_search.setPlaceholderText(
            "Enter customer name or order code here."       # Placeholder for seach bar
            )
        
        self.filterCombo = QComboBox()
        self.filterCombo.addItems(["All Status"] + Statuses)
        
        # Orders Table
        self.ordersTable = QTableWidget()
        self.ordersTable.setColumnCount(6)
        self.ordersTable.setHorizontalHeaderLabels([
            "Order Number",
            "Customer Info", 
            "Job Details",
            "Source",
            "Amount",
            "Status"
        ])
        
        self.ordersTable.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers) # read only
        self.ordersTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch) # Stretches the columns to fill the width :D
          
        # ----- Layout -----
        
        # Tabs: Main Window and Change Prices
        self.setCentralWidget(self.adminWindowTabs)
        self.adminWindowTabs.addTab(central_widget, "Main Window")
        self.adminWindowTabs.addTab(self.pricePage(), "Change Prices")
        
        # Sales
        salesLayout = QVBoxLayout(salesCard)
        salesLayout.addWidget(salesTitleLabel)
        salesLayout.addWidget(self.salesLabel)
        
        # Orders
        ordersLayout = QVBoxLayout(ordersCard)
        ordersLayout.addWidget(ordersTitleLabel)
        ordersLayout.addWidget(self.ordersLabel)
        
        # Jobs
        jobsLayout = QVBoxLayout(jobsCard)
        jobsLayout.addWidget(jobsTitleLabel)
        jobsLayout.addWidget(self.jobsLabel)
        
        # Metrics
        metricsLayout = QHBoxLayout()
        metricsLayout.setSpacing(12)
        metricsLayout.addWidget(salesCard)
        metricsLayout.addWidget(ordersCard)
        metricsLayout.addWidget(jobsCard)
        
        # Search box
        filterLayout = QHBoxLayout()
        filterLayout.setSpacing(10)
        filterLayout.addWidget(self.text_search, 1)
        filterLayout.addWidget(self.filterCombo)
        
        # ----- Main Layout -----
        adminwindowLayout = QVBoxLayout(central_widget)
        
        adminwindowLayout.addLayout(metricsLayout)
        adminwindowLayout.addWidget(ordersTitle)
        adminwindowLayout.addWidget(ordersSubtitle)
        adminwindowLayout.addLayout(filterLayout)
        adminwindowLayout.addWidget(self.ordersTable)
        
        # ----- Signals -----
        self.text_search.textChanged.connect(self.refreshTable)
        self.filterCombo.currentIndexChanged.connect(self.refreshTable)
        
        self.refreshTable()
        
    # ---- Add Order -----
    def addOrder(self, order):
        self.orders.append(order)
        self.refreshTable()
        
    # ----- updateStatus -----
    def updateStatus(self, orderId, newStatus):
        for order in self.orders:
            if order["id"] == orderId:
                order["status"] = newStatus
                
        self.refreshTable()
        
        if self.user_window is not None:
            self.user_window.updateStatusRow(orderId, newStatus)
    
    # ----- refreshTable -----
    def refreshTable(self):
        search = self.text_search.text().strip().lower()
        status = self.filterCombo.currentText()
        
        self.ordersTable.setRowCount(0)
        sales = 0
        open_jobs = 0
        
        for order in self.orders:
            # Order counter (does not count Cancelled orders)
            if order["status"] != "Cancelled":
                sales += order["amount"]
                
             # Open jobs counter (does not count cancelled and completed jobs/orders)   
            if order["status"] not in ("Completed", "Cancelled"):
                open_jobs += 1
                
            matchesSearch = search in order["name"].lower() or search in order["id"].lower()    # Match name/id
            matchesStatus = status == "All Status" or order["status"] == status                 # Match status
            
            if matchesSearch and matchesStatus:
                row = self.ordersTable.rowCount()
                self.ordersTable.insertRow(row)
                price = f"₱{order['amount']:.0f}"
                
                customer = "\n".join([
                    order["name"],
                    order["phone"],
                    order["account"]
                    ])
                
                cells = [
                    order["id"],
                    customer,
                    order["job"],
                    order["source"],
                    price,
                    order["status"]
                ]
                
                self.ordersTable.setItem(row, 0, QTableWidgetItem(order["id"]))
                self.ordersTable.setItem(row, 1, QTableWidgetItem(customer))
                self.ordersTable.setItem(row, 2, QTableWidgetItem(order["job"]))
                self.ordersTable.setItem(row, 3, QTableWidgetItem(order["source"]))
                self.ordersTable.setItem(row, 4, QTableWidgetItem(price))
                
                # Status dropdown (column 5)
                statusCombo = QComboBox()
                statusCombo.addItems(Statuses)
                statusCombo.setCurrentText(order["status"])
                statusCombo.currentTextChanged.connect(lambda newStatus, orderId=order["id"]: self.updateStatus(orderId, newStatus))
                self.ordersTable.setCellWidget(row, 5, statusCombo)
                
        sales = f"₱{sales:.0f}"
        orders = f"{len(self.orders)}"
        open_jobs = f"{open_jobs}"
        
        self.ordersTable.resizeRowsToContents()     # Fits the customer info
        self.salesLabel.setText(sales)
        self.ordersLabel.setText(orders)
        self.jobsLabel.setText(open_jobs)
                
    # ----- Price Tab -----
    def pricePage(self):
        # ----- Widgets -----
        pricePageWidget = QWidget()
        pricePageTitle = QLabel("Change Prices")
        pricePageSubtitle = QLabel("Click SAVE PRICES to use the new prices.")
        
        priceFormLayout = QFormLayout()
        self.priceSpins = []
        
        for label, value in Prices:
            spin = QSpinBox()
            spin.setRange(0, 999)
            spin.setPrefix("₱")
            spin.setValue(value)
            
            priceFormLayout.addRow(QLabel(label), spin)
            self.priceSpins.append(spin)
        
        saveButton = QPushButton("Save Prices")
        
        # ----- Layout -----
        pricePageLayout = QVBoxLayout(pricePageWidget)
        pricePageLayout.addWidget(pricePageTitle)
        pricePageLayout.addWidget(pricePageSubtitle)
        pricePageLayout.addLayout(priceFormLayout)
        pricePageLayout.addWidget(saveButton)
        pricePageLayout.addStretch()
        
        # ----- Signals -----
        saveButton.clicked.connect(self.savePrices)
        return pricePageWidget
    
    # ----- savePrices -----
    def savePrices(self):
        values = []
        for priceSpin in self.priceSpins:
            values.append(priceSpin.value())
        self.user_window.setPrices(*values)