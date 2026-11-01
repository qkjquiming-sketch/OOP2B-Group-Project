from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QComboBox, QSpinBox, QCheckBox, QPushButton,
    QTableWidget, QTableWidgetItem, QButtonGroup, QHeaderView
)
from dialogs import ConfirmOrderDialog, CustomAlertDialog
from config import Prices

class UserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PrintSync - User Screen")
        self.admin_window = None
        self.orderCount = 1000
        
        # Prices
        self.pricePaper = Prices[0][1]
        self.priceLegal = Prices[1][1]
        self.pricePhotoPaper = Prices[2][1]
        self.priceBw = Prices[3][1]
        self.priceColor = Prices[4][1]
        self.priceBinding = Prices[5][1]
        self.priceLamination = Prices[6][1]
        
        self.init_ui()
        
    def init_ui(self):
        # ----- Widgets -----
        central_widget = QWidget()
        
        # Heading
        titleLabel = QLabel("New Print Order Form")
        titleLabel.setObjectName("title")
        
        subtitleLabel = QLabel("Select options below to compute for total price.")
        subtitleLabel.setObjectName("subtitle")
        
        # Customer info
        customerNameLabel = QLabel("Customer Name *")
        self.customerNameInput = QLineEdit()
        self.customerNameInput.setPlaceholderText("e.g. Juan Dela Cruz")
        
        customerPhoneLabel = QLabel("Contact Number")
        self.customerPhoneInput = QLineEdit()
        self.customerPhoneInput.setPlaceholderText("09XX XXXX XXXX")
        
        customerAccountLabel = QLabel("Email / Facebook Account")
        self.customerAccountInput = QLineEdit()
        self.customerAccountInput.setPlaceholderText("Email or FB Username")
        
        # File Source
        fileSourceLabel = QLabel("File Submission Source:")
        self.fileSourceGroup = QButtonGroup(self)
        self.fileSourceGroup.setExclusive(True)     # Makes it so that only one of the buttons can be selected
        
        self.gmailButton = QPushButton("Gmail")
        self.gmailButton.setCheckable(True)
        self.gmailButton.setFixedHeight(36)
        
        self.facebookButton = QPushButton("Facebook / Messenger")
        self.facebookButton.setCheckable(True)
        self.facebookButton.setFixedHeight(36)
        
        self.fileSourceGroup.addButton(self.gmailButton)
        self.fileSourceGroup.addButton(self.facebookButton)
        self.gmailButton.setChecked(True)           # Sets the default to Gmail\
            
            
            
        # Print specifications
        printSpecsLabel = QLabel("Print Specification")
        
        # Color
        colorLabel = QLabel("Colored")
        self.colorCombo = QComboBox()
        self.colorCombo.addItems([
            f"Black and White — +₱{self.priceBw}/pg",
            f"Full Color — +₱{self.priceColor}/pg"
        ])
        
        # Size
        sizeLabel = QLabel("Paper Size")
        self.sizeCombo = QComboBox()
        self.sizeCombo.addItems([
            f"Letter / Short — ₱{self.pricePaper}/pg",
            f"A4 — ₱{self.pricePaper}/pg",
            f"Legal / Long — ₱{self.priceLegal}/pg",
            f"Photo Paper — ₱{self.pricePhotoPaper}/pg"
        ])
        
        # Pages
        pagesLabel = QLabel("Pages")
        self.pagesSpin = QSpinBox()
        self.pagesSpin.setRange(1, 1000)
        self.pagesSpin.setValue(10)
        
        # Compies
        copiesLabel = QLabel("Copies")
        self.copiesSpin = QSpinBox()
        self.copiesSpin.setRange(1, 100)
        self.copiesSpin.setValue(1)
        
        # Binding
        self.bindingCheck = QCheckBox(f"Binding (+₱{self.priceBinding})")
        
        # Lamination
        self.laminationCheck = QCheckBox(f"Lamination (+₱{self.priceLamination})")
        
        # Price breakdown
        priceBreakdownLabel = QLabel("Price Breakdown")
        self.breakdownLabel = QLabel()
        self.totalLabel = QLabel()
        self.placeOrderButton =  QPushButton("Place Order")
        
        # Order status table
        orderStatusLabel = QLabel("Order Status")
        self.statusTable = QTableWidget()
        self.statusTable.setColumnCount(3)
        self.statusTable.setHorizontalHeaderLabels(["Order", "Job", "Status"])
        self.statusTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        # ----- Layout -----
        self.setCentralWidget(central_widget)
        
        # ----- Customer Info ( Name and Contact Number )
        customerNameLayout = QVBoxLayout()
        customerNameLayout.setSpacing(6)
        customerNameLayout.addWidget(customerNameLabel)
        customerNameLayout.addWidget(self.customerNameInput)
        
        customerPhoneLayout = QVBoxLayout()
        customerPhoneLayout.setSpacing(6)
        customerPhoneLayout.addWidget(customerPhoneLabel)
        customerPhoneLayout.addWidget(self.customerPhoneInput)
        
        customerInfoLayout = QHBoxLayout()
        customerInfoLayout.setSpacing(12)
        customerInfoLayout.addLayout(customerNameLayout, 1)
        customerInfoLayout.addLayout(customerPhoneLayout, 1)
        
        # ----- Account -----
        accountLayout = QVBoxLayout()
        accountLayout.setSpacing(6)
        accountLayout.addWidget(customerAccountLabel)
        accountLayout.addWidget(self.customerAccountInput)
        
        # ----- File Source Buttons -----
        fileSourceLayout = QHBoxLayout()
        fileSourceLayout.setSpacing(8)
        fileSourceLayout.addWidget(self.gmailButton, 1)
        fileSourceLayout.addWidget(self.facebookButton, 1)
        
        # ----- Colored and Paper Size -----
        colorLayout = QVBoxLayout()
        colorLayout.setSpacing(6)
        colorLayout.addWidget(colorLabel)
        colorLayout.addWidget(self.colorCombo)
        
        sizeLayout = QVBoxLayout()
        sizeLayout.setSpacing(6)
        sizeLayout.addWidget(sizeLabel)
        sizeLayout.addWidget(self.sizeCombo)
        
        specsRow1Layout = QHBoxLayout()
        specsRow1Layout.setSpacing(12)
        specsRow1Layout.addLayout(colorLayout ,1)
        specsRow1Layout.addLayout(sizeLayout ,1)
        
        # ----- Pages and Copies -----
        
        pagesLayout = QVBoxLayout()
        pagesLayout.setSpacing(6)
        pagesLayout.addWidget(pagesLabel)
        pagesLayout.addWidget(self.pagesSpin)
        
        copiesLayout = QVBoxLayout()
        copiesLayout.setSpacing(6)
        copiesLayout.addWidget(copiesLabel)
        copiesLayout.addWidget(self.copiesSpin)
        
        specsRow2Layout = QHBoxLayout()
        specsRow2Layout.setSpacing(12)
        specsRow2Layout.addLayout(pagesLayout, 1)
        specsRow2Layout.addLayout(copiesLayout, 1)
        
        # ----- Add-ons -----
        addonsLayout = QHBoxLayout()
        addonsLayout.setSpacing(16)
        addonsLayout.addWidget(self.bindingCheck)
        addonsLayout.addWidget(self.laminationCheck)
        
        # ----- Left Side Layout -----
        leftPanelLayout = QVBoxLayout()
        leftPanelLayout.setSpacing(12)
        leftPanelLayout.addLayout(customerInfoLayout)
        leftPanelLayout.addLayout(accountLayout)
        leftPanelLayout.addWidget(fileSourceLabel)
        leftPanelLayout.addLayout(fileSourceLayout)
        leftPanelLayout.addWidget(printSpecsLabel)
        leftPanelLayout.addLayout(specsRow1Layout)
        leftPanelLayout.addLayout(specsRow2Layout)
        leftPanelLayout.addLayout(addonsLayout)
        leftPanelLayout.addStretch()
        
        # ----- Right Side -----
        rightPanelLayout = QVBoxLayout()
        rightPanelLayout.setSpacing(12)
        rightPanelLayout.addWidget(priceBreakdownLabel)
        rightPanelLayout.addWidget(self.breakdownLabel)
        rightPanelLayout.addWidget(self.totalLabel)
        rightPanelLayout.addWidget(self.placeOrderButton)
        rightPanelLayout.addWidget(orderStatusLabel)
        rightPanelLayout.addWidget(self.statusTable)
        
        # ----- Combine Left and Right -----
        panelsLayout = QHBoxLayout()
        panelsLayout.setSpacing(16)
        panelsLayout.addLayout(leftPanelLayout, 1)
        panelsLayout.addLayout(rightPanelLayout, 1)
        
        # ----- Main Layout -----
        UserWindowLayout = QVBoxLayout(central_widget)
        UserWindowLayout.setContentsMargins(12, 12, 12, 12)
        UserWindowLayout.setSpacing(12)
        
        UserWindowLayout.addWidget(titleLabel)
        UserWindowLayout.addWidget(subtitleLabel)
        UserWindowLayout.addLayout(panelsLayout)
        
        # ----- Signals -----
        self.colorCombo.currentIndexChanged.connect(self.calculateTotal)
        self.sizeCombo.currentIndexChanged.connect(self.calculateTotal)
        self.pagesSpin.valueChanged.connect(self.calculateTotal)
        self.copiesSpin.valueChanged.connect(self.calculateTotal)
        self.bindingCheck.toggled.connect(self.calculateTotal)
        self.laminationCheck.toggled.connect(self.calculateTotal)
        
        self.placeOrderButton.clicked.connect(self.placeOrder)
        
        self.calculateTotal()       
        
        # ----- Widget Styling -----
        customerNameLabel.setProperty("class", "field-label")
        customerPhoneLabel.setProperty("class", "field-label")
        customerAccountLabel.setProperty("class", "field-label")
        fileSourceLabel.setProperty("class", "field-label")
        colorLabel.setProperty("class", "field-label")
        sizeLabel.setProperty("class", "field-label")
        pagesLabel.setProperty("class", "field-label")
        copiesLabel.setProperty("class", "field-label")

        printSpecsLabel.setProperty("class", "section")
        priceBreakdownLabel.setProperty("class", "section")
        orderStatusLabel.setProperty("class", "section")

        self.breakdownLabel.setProperty("class", "card")
        self.totalLabel.setObjectName("totalLabel")
        self.placeOrderButton.setObjectName("placeOrderButton")

        self.gmailButton.setProperty("class", "sourceButton")
        self.facebookButton.setProperty("class", "sourceButton")
        
    # ----- calculateTotal -----
    def calculateTotal(self) -> float:
        # Price of the paper
        paperText = self.sizeCombo.currentText()
        
        # Sets price to 3 if Legal / Long is selected
        if "Legal" in paperText:            
            paperCost = self.priceLegal
            
        # Sets price to 25 if Photo Paper is selected
        elif "Photo Paper" in paperText:
            paperCost = self.pricePhotoPaper
            
        # Sets price to 2 if Letter / Short / A4 is selected
        else:
            paperCost = self.pricePaper
            
        #  Print Price
        
        # Full Color price
        colorText = self.colorCombo.currentText()
        if "Full Color" in colorText:
            colorName = "Full Color"
            printCost = self.priceColor
            
        # Black and White
        else:
            colorName = "Black and White"
            printCost = self.priceBw
            
        pages = self.pagesSpin.value()
        copies = self.copiesSpin.value()
        
        paperTotal = pages * paperCost
        colorTotal = pages * printCost
        
        # Add-ons prices
        addonsCost = 0
        addonsText = "None"
        
        if self.bindingCheck.isChecked():
            addonsCost += self.priceBinding
            addonsText = "Binding"

        if self.laminationCheck.isChecked():
            addonsCost += self.priceLamination
            if addonsText == "None":
                addonsText = "Lamination"
            else:
                addonsText += ", Lamination"
                
        subtotalPerCopy = paperTotal + colorTotal + addonsCost
        totalPrice = subtotalPerCopy * copies
        
        self.breakdownLabel.setText(
            f"- Base Paper ({paperText.split(' — ')[0]}): {pages} pgs * ₱{paperCost} = ₱{paperTotal}\n"
            f"- Color Option ({colorName}): {pages} pgs * ₱{printCost} = ₱{colorTotal}\n"
            f"- Add-ons: {addonsText} = ₱{addonsCost}\n"
            f"- Multiplier: ₱{subtotalPerCopy} × {copies} copy"
        )
        self.totalLabel.setText(f"₱{totalPrice}")
        return totalPrice
    
    # ----- placeOrder -----
    def placeOrder(self):

        name = self.customerNameInput.text().strip()
        phone = self.customerPhoneInput.text().strip()
        account = self.customerAccountInput.text().strip()
        
        # source: 
        if self.gmailButton.isChecked():
            source = "Gmail"
        else:
            source = "Facebook / Messenger"        
            
        # Makes it so that Name is a field that requires to be filled out
        if not name:
            CustomAlertDialog(
                "Missing Info",
                "Please enter your name.",
                self).exec()
            return
        
        # Prompts the cutomer for confirmation
        if not ConfirmOrderDialog(name, phone, source, self).exec():
            return
        
        self.orderCount += 1
        orderId = "PS-" + str(self.orderCount)
        
        # Job description builder
        pages = self.pagesSpin.value()
        copies = self.copiesSpin.value()
        size = self.sizeCombo.currentText().split(" — ")[0]
        if "Full Color" in self.colorCombo.currentText():
            color = "Full Color"
        else:
            color = "Black and White"
            
        job = f"{pages} pages, {color}, {size}, {copies} copies"
        if self.bindingCheck.isChecked():
            job += ", Binding"
        if self.laminationCheck.isChecked():
            job += ", Lamination"
            
        order = {
            "id": orderId,
            "name": name,
            "phone": phone,
            "account": account,
            "source": source,
            "job": job,
            "amount": self.calculateTotal(),
            "status": "Pending",
        }
        
        # Sends the order to the admin screen
        if self.admin_window is not None:
            self.admin_window.addOrder(order)
        
        # Add the order to the status table
        row = self.statusTable.rowCount()
        self.statusTable.insertRow(row)
        self.statusTable.setItem(row, 0, QTableWidgetItem(orderId))
        self.statusTable.setItem(row, 1, QTableWidgetItem(job))
        self.statusTable.setItem(row, 2, QTableWidgetItem("Pending"))
        
        CustomAlertDialog("Order Placed!", f"Your order({orderId}) was successfully submitted.", self). exec()
        
        # Clears the form for the next customer
        self.customerNameInput.clear()
        self.customerPhoneInput.clear()
        self.customerAccountInput.clear()
        
        
    # ----- updateStatusRow -----
    def updateStatusRow(self, orderId, status):
        for row in range(self.statusTable.rowCount()):
            if self.statusTable.item(row, 0).text() == orderId:
                self.statusTable.item(row, 2).setText(status)
                
    # ----- update/set Prices -----
    def setPrices(self, paper, legal, photoPaper, bw, color, binding, lamination):
        self.pricePaper = paper
        self.priceLegal = legal
        self.pricePhotoPaper = photoPaper
        self.priceBw = bw
        self.priceColor = color
        self.priceBinding = binding
        self.priceLamination = lamination
        
        self.sizeCombo.setItemText(0, f"Letter / Short — ₱{paper}/pg")
        self.sizeCombo.setItemText(1, f"A4 — ₱{paper}/pg")
        self.sizeCombo.setItemText(2, f"Legal / Long — ₱{legal}/pg")
        self.sizeCombo.setItemText(3, f"Photo Paper — ₱{photoPaper}/pg")
        self.colorCombo.setItemText(0, f"Black and White — +₱{bw}/pg")
        self.colorCombo.setItemText(1, f"Full Color — +₱{color}/pg")
        self.bindingCheck.setText(f"Binding (+₱{binding})")
        self.laminationCheck.setText(f"Lamination (+₱{lamination})")

        self.calculateTotal()
                
        