import csv
import os
from datetime import datetime

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QTableWidget, QFrame,
    QTabWidget, QTableWidgetItem, QHeaderView, QSpinBox,
    QPushButton, QFormLayout, QFileDialog, QMenu
)
from PyQt6.QtCore import Qt

from config import Prices, Statuses, pricesFile
from dialogs import showAlert, showConfirmDelete
from base_window import BaseWindow
from models import Order, orderFromRow

class AdminWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Screen")
        self.user_window = None
        self.orders = []            # Stores orders
        self.deletedOrders = []     # Stores deleted orders (for undo)
        self.init_ui()

    # ----- Menu bar and toolbar -----
    def setupMenus(self):
        loadAction = self.makeAction("Load Orders...", self.loadOrders)
        saveAction = self.makeAction("Save Orders Now", self.saveOrdersNow)
        self.undoAction = self.makeAction("Undo Delete", self.undoDelete)
        self.undoAction.setEnabled(False)
        exitAction = self.makeAction("Exit", self.close)
        aboutAction = self.makeAction("About PrintSync", self.showAbout)

        fileMenu = self.menuBar().addMenu("File")
        fileMenu.addAction(loadAction)
        fileMenu.addAction(saveAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

        editMenu = self.menuBar().addMenu("Edit")
        editMenu.addAction(self.undoAction)

        helpMenu = self.menuBar().addMenu("Help")
        helpMenu.addAction(aboutAction)

        toolbar = self.addToolBar("Main Toolbar")
        toolbar.setMovable(False)
        toolbar.addAction(loadAction)
        toolbar.addAction(saveAction)
        toolbar.addSeparator()
        toolbar.addAction(self.undoAction)

    def init_ui(self):
        # ----- Widgets -----
        central_widget = QWidget()
        self.adminWindowTabs = QTabWidget()
        
        # Metric cards
        salesCard = QFrame()
        salesTitleLabel = QLabel("Sales Today")
        self.salesLabel = QLabel("Sales Today")     # Placeholder
        
        ordersCard = QFrame()
        ordersTitleLabel = QLabel("Total Orders")
        self.ordersLabel = QLabel("Total Orders")   # Placeholder
        
        jobsCard = QFrame()
        jobsTitleLabel = QLabel("Open Jobs")
        self.jobsLabel = QLabel("Open Jobs")        # Placeholder
        
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
        self.loadButton = QPushButton("Load Orders")    # Button for loading previous order history
        self.undoButton = QPushButton("Undo Delete")
        
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
        filterLayout.addWidget(self.loadButton)
        filterLayout.addWidget(self.undoButton)
        
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
        self.loadButton.clicked.connect(self.loadOrders)
        self.undoButton.clicked.connect(self.undoDelete)
        
        self.ordersTable.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ordersTable.customContextMenuRequested.connect(self.showOrderMenu)
        
        self.refreshTable()
        
        # ----- Widget Styling -----
        # Metric cards
        salesCard.setProperty("class", "metric-card")
        salesTitleLabel.setProperty("class", "metric-title")
        self.salesLabel.setProperty("class", "metric-value")
        salesLayout.setContentsMargins(16, 12 ,16, 12)
        salesLayout.setSpacing(2)
        
        ordersCard.setProperty("class", "metric-card")
        ordersTitleLabel.setProperty("class", "metric-title")
        self.ordersLabel.setProperty("class", "metric-value")
        ordersLayout.setContentsMargins(16, 12 ,16, 12)
        ordersLayout.setSpacing(2)
        
        jobsCard.setProperty("class", "metric-card")
        jobsTitleLabel.setProperty("class", "metric-title")
        self.jobsLabel.setProperty("class", "metric-value")
        jobsLayout.setContentsMargins(16, 12 ,16, 12)
        jobsLayout.setSpacing(2)
        
        # Orders heading
        ordersTitle.setProperty("class", "section")
        ordersSubtitle.setObjectName("subtitle")
        
        # Orders table
        self.ordersTable.setAlternatingRowColors(True)
        self.ordersTable.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        # Spacing
        adminwindowLayout.setContentsMargins(12, 12, 12, 12)
        adminwindowLayout.setSpacing(12)
        
        # Load Order Button
        self.loadButton.setProperty("class", "secondaryButton")
        
        # Undo Delete Button
        self.undoButton.setProperty("class", "secondaryButton")
        self.undoButton.setEnabled(False)
        
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
            
    # ----- Manage Orders -----
    def showOrderMenu(self, pos):
        row = self.ordersTable.rowAt(pos.y())
        if row < 0: return
        
        self.ordersTable.selectRow(row)
        orderId = self.ordersTable.item(row, 0).text()
        
        menu = QMenu(self)
        deleteOrderAction = menu.addAction("Delete Order")
        selected = menu.exec(self.ordersTable.viewport().mapToGlobal(pos))
        
        if selected == deleteOrderAction:   self.deleteOrder(orderId)
        
    def deleteOrder(self, orderId):
        if not showConfirmDelete(orderId, self):    return
        
        for index in range(len(self.orders)):
            if self.orders[index]["id"] == orderId:
                removeOrder = self.orders.pop(index)

                # Removes the der from the user's status table
                orderInUserScreen = False
                if self.user_window is not None:
                    orderInUserScreen = self.user_window.removeStatusRow(orderId)
        
                self.deletedOrders.append({
                    "order": removeOrder,
                    "index": index,
                    "orderInUserScreen": orderInUserScreen,
                })
                break
        
        self.refreshTable()
        self.updateUndoState()

    # ----- undoDelete -----
    def undoDelete(self):
        if len(self.deletedOrders) == 0: return
        
        deletedOrder = self.deletedOrders.pop()
        order = deletedOrder["order"]

        if not any(existing["id"] == order["id"] for existing in self.orders):
            self.orders.insert(min(deletedOrder["index"], len(self.orders)), order)
            
            if self.user_window is not None and deletedOrder["orderInUserScreen"]:
                self.user_window.addStatusRow(order["id"], order["job"], order["status"])

        self.refreshTable()
        self.updateUndoState()
        
    # ----- updateUndoState -----
    def updateUndoState(self):
        canUndo = len(self.deletedOrders) > 0
        self.undoButton.setEnabled(canUndo)
        self.undoAction.setEnabled(canUndo)
        
    # ----- refreshTable -----
    def refreshTable(self):
        search = self.text_search.text().strip().lower()
        status = self.filterCombo.currentText()
        
        self.ordersTable.setRowCount(0)
        sales = 0
        open_jobs = 0
        
        for order in self.orders:
            # Order counter (does not count Cancelled orders)
            if order.countsAsSale():
                sales += order["amount"]
                
             # Open jobs counter (does not count cancelled and completed jobs/orders)   
            if order.isOpen():
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
        
        priceCard = QFrame()
        priceFormLayout = QFormLayout(priceCard)
        self.priceSpins = []
        
        # Paper (Letter / Short and A4)
        paperLabel = QLabel(Prices[0][0])
        paperLabel.setProperty("class", "field-label")
        paperSpin = QSpinBox()
        paperSpin.setRange(0, 999)
        paperSpin.setPrefix("₱")
        paperSpin.setValue(Prices[0][1])
        paperSpin.setFixedWidth(120)
        priceFormLayout.addRow(paperLabel, paperSpin)
        self.priceSpins.append(paperSpin)
        
        # Legal / Long
        legalLabel = QLabel(Prices[1][0])
        legalLabel.setProperty("class", "field-label")
        legalSpin = QSpinBox()
        legalSpin.setRange(0, 999)
        legalSpin.setPrefix("₱")
        legalSpin.setValue(Prices[1][1])
        legalSpin.setFixedWidth(120)
        priceFormLayout.addRow(legalLabel, legalSpin)
        self.priceSpins.append(legalSpin)
        
        # Photo Paper
        photoLabel = QLabel(Prices[2][0])
        photoLabel.setProperty("class", "field-label")
        photoSpin = QSpinBox()
        photoSpin.setRange(0, 999)
        photoSpin.setPrefix("₱")
        photoSpin.setValue(Prices[2][1])
        photoSpin.setFixedWidth(120)
        priceFormLayout.addRow(photoLabel, photoSpin)
        self.priceSpins.append(photoSpin)
        
        # Black and White
        bwLabel = QLabel(Prices[3][0])
        bwLabel.setProperty("class", "field-label")
        bwSpin = QSpinBox()
        bwSpin.setRange(0, 999)
        bwSpin.setPrefix("₱")
        bwSpin.setValue(Prices[3][1])
        bwSpin.setFixedWidth(120)
        priceFormLayout.addRow(bwLabel, bwSpin)
        self.priceSpins.append(bwSpin)
        
        # Full Color
        colorLabel = QLabel(Prices[4][0])
        colorLabel.setProperty("class", "field-label")
        colorSpin = QSpinBox()
        colorSpin.setRange(0, 999)
        colorSpin.setPrefix("₱")
        colorSpin.setValue(Prices[4][1])
        colorSpin.setFixedWidth(120)
        priceFormLayout.addRow(colorLabel, colorSpin)
        self.priceSpins.append(colorSpin)
        
        # Binding
        bindingLabel = QLabel(Prices[5][0])
        bindingLabel.setProperty("class", "field-label")
        bindingSpin = QSpinBox()
        bindingSpin.setRange(0, 999)
        bindingSpin.setPrefix("₱")
        bindingSpin.setValue(Prices[5][1])
        bindingSpin.setFixedWidth(120)
        priceFormLayout.addRow(bindingLabel, bindingSpin)
        self.priceSpins.append(bindingSpin)
        
        # Lamination
        laminationLabel = QLabel(Prices[6][0])
        laminationLabel.setProperty("class", "field-label")
        laminationSpin = QSpinBox()
        laminationSpin.setRange(0, 999)
        laminationSpin.setPrefix("₱")
        laminationSpin.setValue(Prices[6][1])
        laminationSpin.setFixedWidth(120)
        priceFormLayout.addRow(laminationLabel, laminationSpin)
        self.priceSpins.append(laminationSpin)
        
        saveButton = QPushButton("Save Prices")
        
        # ----- Layout -----
        pricePageLayout = QVBoxLayout(pricePageWidget)
        pricePageLayout.addWidget(pricePageTitle)
        pricePageLayout.addWidget(pricePageSubtitle)
        pricePageLayout.addWidget(priceCard)
        pricePageLayout.addWidget(saveButton)
        pricePageLayout.addStretch()
        
        # ----- Signals -----
        saveButton.clicked.connect(self.savePrices)
        
        # ----- Widget Styling -----
        pricePageTitle.setObjectName("title")
        pricePageSubtitle.setObjectName("subtitle")
        priceCard.setProperty("class", "card")
        saveButton.setObjectName("savePricesButton")
        
        priceFormLayout.setContentsMargins(16, 12, 16, 12)
        priceFormLayout.setSpacing(10)
        pricePageLayout.setContentsMargins(12, 12, 12, 12)
        pricePageLayout.setSpacing(12)
        
        return pricePageWidget
    
    # ----- savePrices -----
    def savePrices(self):
        values = []
        values.append(self.priceSpins[0].value())
        values.append(self.priceSpins[1].value())
        values.append(self.priceSpins[2].value())
        values.append(self.priceSpins[3].value())
        values.append(self.priceSpins[4].value())
        values.append(self.priceSpins[5].value())
        values.append(self.priceSpins[6].value())
        self.user_window.setPrices(*values)
        
        with open(pricesFile, "w") as file:
            file.write("\n".join(str(v) for v in values))
    
    # ----- loadOrders -----
    def loadOrders(self):
        ordersFolder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "orders")
        path, _ = QFileDialog.getOpenFileName(self, "Load Orders", ordersFolder, "CSV Files (*.csv)")

        if not path: return
        
        loadedOrders = 0
        try:
            with open(path, "r", newline="", encoding="utf-8-sig") as file:
                fileReader = csv.DictReader(file)
                for row in fileReader:
                    orderId = row["Order Number"]
                
                    if any(order["id"] == orderId for order in self.orders): continue
                    
                    self.orders.append(orderFromRow(row))
                    
                    loadedOrders += 1
                    
                    if self.user_window is not None:
                        self.user_window.addStatusRow(orderId, row["Job Details"], row["Status"])
            
        except Exception:
            return showAlert("Load Failed", "Couldn't read the file.", self)
        
        self.refreshTable()
        showAlert("Orders Loaded", f"Loaded {loadedOrders} order(s).", self)
               
    # ----- saveOrdersNow (menu / toolbar) -----
    def saveOrdersNow(self):
        path = self.saveOrdersToCSV()
        if path:
            showAlert("Orders Saved", f"Saved {len(self.orders)} order(s) to:\n{os.path.basename(path)}", self)
        else:
            showAlert("Nothing Saved", "There are no orders to save yet.", self)  
                
    # ----- saveOrdersToCSV -----
    def saveOrdersToCSV(self):
        rows = [order.toRow() for order in self.orders]
        if not rows:
            print("No orders to save.")      # No empty file is created
            return None
        
        try:
            folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "orders")
            os.makedirs(folder, exist_ok=True)
            now = datetime.now()
            path = os.path.join(folder, now.strftime("%Y-%m-%d_%H-%M-%S") + ".csv")
            
            # utf-8-sig so Excel shows the characters correctly
            with open(path, "w", newline="", encoding="utf-8-sig") as file:
                writer = csv.writer(file)
                writer.writerow(Order.headerCSV)
                writer.writerows(rows)
                
            print(f"Saved {len(rows)} order(s) to: {path}")
            return path
        
        except Exception:
            print(f"Failed to save the file D:")  
            return None
    
