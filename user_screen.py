from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QSpinBox, QCheckBox, QPushButton, QTableWidget, QTableWidgetItem,
    QButtonGroup, QHeaderView
)
from dialogs import ConfirmOrderDialog, CustomAlertDialog


class UserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.admin_window = None
        self.order_count = 1000
        self.price_paper = 2
        self.price_legal = 3
        self.price_photo_paper = 25
        self.price_bw = 2
        self.price_color = 3
        self.price_binding = 30
        self.price_lamination = 15
        self.setWindowTitle("PrintSync - User Screen")
        self.setStyleSheet("color: #c9d1d9; font-family: 'Segoe UI', sans-serif; font-size: 13px;")
        self.init_ui()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(12)

        title = QLabel("New Print Order Form")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #ffffff; padding-bottom: 4px;")
        title.setObjectName("title")
        root.addWidget(title)

        subtitle = QLabel("Select options below to compute total price.")
        subtitle.setObjectName("subtitle")
        subtitle.setStyleSheet("color: #8b949e;")
        root.addWidget(subtitle)

        columns = QHBoxLayout()
        columns.setSpacing(16)
        columns.addLayout(self.build_form(), 1)
        columns.addLayout(self.build_right_panel(), 1)
        root.addLayout(columns)

    def labeled(self, text, widget):
        column = QVBoxLayout()
        column.setSpacing(6)
        label = QLabel(text)
        label.setStyleSheet("font-size: 12px; font-weight: 600; color: #8b949e;")
        column.addWidget(label)
        column.addWidget(widget)
        return column

    def build_form(self):
        form = QVBoxLayout()
        form.setSpacing(12)

        self.txt_name = QLineEdit()
        self.txt_name.setPlaceholderText("e.g. Juan Dela Cruz")
        self.txt_name.setStyleSheet("font-size: 12px; font-weight: 600; color: #000000;")

        self.txt_phone = QLineEdit()
        self.txt_phone.setPlaceholderText("0917-XXX-XXXX")
        self.txt_phone.setStyleSheet("font-size: 12px; font-weight: 600; color: #000000;")

        self.txt_account = QLineEdit()
        self.txt_account.setPlaceholderText("Email or FB Username")
        self.txt_account.setStyleSheet("font-size: 12px; font-weight: 600; color: #000000;")

        customer_info = QHBoxLayout()
        customer_info.setSpacing(12)
        customer_info.addLayout(self.labeled("Customer Name *", self.txt_name), 1)
        customer_info.addLayout(self.labeled("Contact Number", self.txt_phone), 1)
        form.addLayout(customer_info)

        form.addLayout(self.labeled("Email / FB Account", self.txt_account))
    
        file_source = QLabel("File Submission Source:")
        file_source.setStyleSheet("font-size: 12px; font-weight: 600; color: #8b949e;")

        source_row = QHBoxLayout()
        source_row.setSpacing(8)
        self.source_group = QButtonGroup(self)
        self.source_group.setExclusive(True)

        self.button_gmail = QPushButton("Gmail")
        self.button_fb = QPushButton("Facebook / Messenger")

        style_unselected = "background-color: #21262d; color: #8b949e; border: 1px solid #30363d; border-radius: 6px; padding: 8px 16px; font-weight: 600;"
        style_selected = "background-color: #238636; color: #ffffff; border: none; border-radius: 6px; padding: 8px 16px; font-weight: bold;"

        for button in (self.button_gmail, self.button_fb):
            button.setCheckable(True)
            button.setFixedHeight(36)
            self.source_group.addButton(button)
            source_row.addWidget(button, 1)

        def update_selected(clicked):
            for button in self.source_group.buttons():
                button.setStyleSheet(style_selected if button is clicked else style_unselected)

        self.source_group.buttonClicked.connect(update_selected)
        self.button_gmail.setChecked(True)
        update_selected(self.button_gmail)

        form.addWidget(file_source)
        form.addLayout(source_row)

        lbl_print_spec = QLabel("Print Specifications")
        lbl_print_spec.setStyleSheet("font-size: 14px; font-weight: bold; color: #ffffff; margin-top: 10px;")
        form.addWidget(lbl_print_spec)

        self.combo_color = QComboBox()
        self.combo_color.addItems([
            "Black and White — +₱2.00/pg",
            "Full Color — +₱3.00/pg",

        ])
        self.combo_color.currentIndexChanged.connect(self.calculate_total)
        self.combo_color.setStyleSheet("font-size: 12px; font-weight: 600; color: #000000;")

        self.combo_size = QComboBox()
        self.combo_size.addItems([
            "Letter / Short — ₱2.00/pg",
            "A4 — ₱2.00/pg",
            "Legal / Long — ₱3.00/pg",
            "Photo Paper — ₱25.00/pg"            
        ])
        self.combo_size.currentIndexChanged.connect(self.calculate_total)
        self.combo_size.setStyleSheet("font-size: 12px; font-weight: 600; color: #000000;")

        spec_row1 = QHBoxLayout()
        spec_row1.setSpacing(12)
        spec_row1.addLayout(self.labeled("Color Mode", self.combo_color), 1)
        spec_row1.addLayout(self.labeled("Paper Size", self.combo_size), 1)
        form.addLayout(spec_row1)

        self.spin_pages = QSpinBox()
        self.spin_pages.setRange(1, 1000)
        self.spin_pages.setValue(10)
        self.spin_pages.valueChanged.connect(self.calculate_total)
        self.spin_pages.setStyleSheet("font-size: 12px; font-weight: 600; color: #000000;")

        self.spin_copies = QSpinBox()
        self.spin_copies.setRange(1, 100)
        self.spin_copies.setValue(1)
        self.spin_copies.valueChanged.connect(self.calculate_total)
        self.spin_copies.setStyleSheet("font-size: 12px; font-weight: 600; color: #000000;")

        spec_row2 = QHBoxLayout()
        spec_row2.setSpacing(12)
        spec_row2.addLayout(self.labeled("Pages", self.spin_pages), 1)
        spec_row2.addLayout(self.labeled("Copies", self.spin_copies), 1)
        form.addLayout(spec_row2)

        self.chk_binding = QCheckBox("Binding (+₱30)")
        self.chk_binding.toggled.connect(self.calculate_total)

        self.chk_lamination = QCheckBox("Lamination (+₱15)")
        self.chk_lamination.toggled.connect(self.calculate_total)

        addons_row = QHBoxLayout()
        addons_row.setSpacing(16)
        addons_row.addWidget(self.chk_binding)
        addons_row.addWidget(self.chk_lamination)
        form.addLayout(addons_row)

        form.addStretch()
        return form

    def build_right_panel(self):
        panel = QVBoxLayout()
        panel.setSpacing(12)

        lbl_price = QLabel("Price Breakdown")
        lbl_price.setStyleSheet("font-size: 14px; font-weight: bold; color: #ffffff;")
        panel.addWidget(lbl_price)

        self.lbl_breakdown = QLabel()
        self.lbl_breakdown.setStyleSheet("color: #8b949e; background-color: #161b22; padding: 10px; border-radius: 6px; border: 1px solid #30363d;")
        panel.addWidget(self.lbl_breakdown)

        self.lbl_total = QLabel("₱40")
        self.lbl_total.setStyleSheet("font-size: 22px; font-weight: bold; color: #238636;")
        panel.addWidget(self.lbl_total)

        self.btn_place_order = QPushButton("Place Order")
        self.btn_place_order.setStyleSheet("background-color: #238636; color: #ffffff; font-weight: bold; border-radius: 6px; padding: 10px 16px;")
        self.btn_place_order.clicked.connect(self.place_order)
        panel.addWidget(self.btn_place_order)

        lbl_status = QLabel("Order Status")
        lbl_status.setStyleSheet("font-size: 14px; font-weight: bold; color: #ffffff; margin-top: 8px;")
        panel.addWidget(lbl_status)

        self.status_table = QTableWidget()
        self.status_table.setColumnCount(3)
        self.status_table.setHorizontalHeaderLabels(["Order", "Job", "Status"])
        self.status_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.status_table.setStyleSheet(
            "QTableWidget {"
            "    background-color: #161b22;"
            "    border: 1px solid #30363d;"
            "    gridline-color: #21262d;"
            "    color: #c9d1d9;"
            "}"
            "QHeaderView::section {"
            "    background-color: #21262d;"
            "    color: #8b949e;"
            "    font-weight: bold;"
            "    border: none;"
            "    border-bottom: 1px solid #30363d;"
            "}"
        )
        panel.addWidget(self.status_table)

        self.calculate_total()
        return panel

    def calculate_total(self) -> float:
        paper_text = self.combo_size.currentText()
        if "legal" in paper_text:
            paper_cost = self.price_legal
        elif "Photo Paper" in paper_text:
            paper_cost = self.price_photo_paper
        else:
            paper_cost = self.price_paper

        color_text = self.combo_color.currentText()
        if "Full Color" in color_text:
            color_name, print_cost = "Full Color", self.price_color
        else:
            color_name, print_cost = "B&W", self.price_bw

        pages = self.spin_pages.value()
        copies = self.spin_copies.value()

        base_paper_total = pages * paper_cost
        color_total = pages * print_cost

        addon_cost = 0.00
        addons_list = []
        if self.chk_binding.isChecked():
            addon_cost += self.price_binding
            addons_list.append("Binding")
        if self.chk_lamination.isChecked():
            addon_cost += self.price_lamination
            addons_list.append("Lamination")

        subtotal_per_copy = base_paper_total + color_total + addon_cost
        total_price = subtotal_per_copy * copies

        addons_str = ", ".join(addons_list) if addons_list else "None"

        self.lbl_breakdown.setText(
            f"• Base Paper ({paper_text.split(' — ')[0]}): {pages} pgs × ₱{paper_cost:.2f} = ₱{base_paper_total:.2f}\n"
            f"• Color Option ({color_name}): {pages} pgs × ₱{print_cost:.2f} = ₱{color_total:.2f}\n"
            f"• Add-ons: {addons_str} = ₱{addon_cost:.2f}\n"
            f"• Multiplier: ₱{subtotal_per_copy:.2f} × {copies} copy"
        )
        self.lbl_total.setText(f"₱{total_price:.0f}")
        return total_price

    def place_order(self):
        name = self.txt_name.text().strip()
        phone = self.txt_phone.text().strip()
        account = self.txt_account.text().strip()
        source = self.source_group.checkedButton().text()

        if not name:
            CustomAlertDialog("Missing Info", "Please enter the customer name.", self).exec()
            return

        if not ConfirmOrderDialog(name, phone, source, self).exec():
            return

        self.order_count += 1
        order_id = "PS-" + str(self.order_count)

        pages = self.spin_pages.value()
        copies = self.spin_copies.value()
        size = self.combo_size.currentText().split(" — ")[0]
        color = "Full Color" if "Full Color" in self.combo_color.currentText() else "B&W"
        extras = [text for text, box in (("Binding", self.chk_binding), ("Lamination", self.chk_lamination)) if box.isChecked()]
        job = ", ".join([f"{pages} pgs", color, size, f"{copies} copy"] + extras)
        order = {
            "id": order_id,
            "name": name,
            "phone": phone,
            "account": account,
            "source": source,
            "job": job,
            "amount": self.calculate_total(),
            "status": "Pending",
        }
        self.admin_window.add_order(order)

        row = self.status_table.rowCount()
        self.status_table.insertRow(row)
        for column, text in enumerate((order_id, job, "Pending")):
            self.status_table.setItem(row, column, QTableWidgetItem(text))

        CustomAlertDialog("Order Placed", f"Your order {order_id} was submitted.", self).exec()
        for box in (self.txt_name, self.txt_phone, self.txt_account):
            box.clear()

    def update_status_row(self, order_id, status):
        for row in range(self.status_table.rowCount()):
            if self.status_table.item(row, 0).text() == order_id:
                self.status_table.item(row, 2).setText(status)

    def set_prices(self, paper, legal, photo_paper, bw, color, binding, lamination):
        self.price_paper = paper
        self.price_legal = legal
        self.price_photo_paper = photo_paper
        self.price_bw = bw
        self.price_color = color
        self.price_binding = binding
        self.price_lamination = lamination
        self.combo_size.setItemText(0, f"Short — ₱{paper:.2f}/pg")
        self.combo_size.setItemText(1, f"A4 — ₱{paper:.2f}/pg")
        self.combo_size.setItemText(2, f"Legal / Long — ₱{legal:.2f}/pg")
        self.combo_size.setItemText(3, f"Photo Paper — ₱{photo_paper:.2f}/pg")
        self.combo_color.setItemText(0, f"B&W — +₱{bw:.2f}/pg")
        self.combo_color.setItemText(1, f"Colored — +₱{color:.2f}/pg")
        self.chk_binding.setText(f"Binding (+₱{binding})")
        self.chk_lamination.setText(f"Lamination (+₱{lamination})")
        self.calculate_total()