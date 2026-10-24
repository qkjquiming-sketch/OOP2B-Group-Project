from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QComboBox, QFrame, QFormLayout
)


class ConfirmOrderDialog(QDialog):
    
    def __init__(self, customer_name: str, phone: str, source: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Confirm Order Submission")
        self.setMinimumWidth(360)
        self.setStyleSheet("background-color: #0d1117; color: #c9d1d9; font-family: 'Segoe UI', sans-serif; font-size: 13px;")
        
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        
        title = QLabel("Confirm Your Order")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #ffffff;")
        layout.addWidget(title)
        
        card = QFrame()
        card.setStyleSheet("background-color: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 12px;")
        card_layout = QFormLayout(card)
        card_layout.setSpacing(8)
        
        card_layout.addRow(self._label("Customer Name:"), QLabel(customer_name))
        card_layout.addRow(self._label("Contact Number:"), QLabel(phone))
        card_layout.addRow(self._label("File Source:"), QLabel(source))
        
        layout.addWidget(card)
        
        btn_layout = QHBoxLayout()
        btn_cancel = QPushButton("Cancel")
        btn_cancel.setStyleSheet("background-color: #21262d; color: #c9d1d9; border: 1px solid #30363d; border-radius: 6px; padding: 6px 12px;")
        btn_cancel.clicked.connect(self.reject)
        
        btn_confirm = QPushButton("Confirm & Submit")
        btn_confirm.setStyleSheet("background-color: #238636; color: #ffffff; font-weight: bold; border-radius: 6px; padding: 6px 12px;")
        btn_confirm.clicked.connect(self.accept)
        
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_confirm)
        layout.addLayout(btn_layout)

    def _label(self, text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setStyleSheet("font-size: 12px; font-weight: 600; color: #8b949e;")
        return lbl


class CustomAlertDialog(QDialog):
    
    def __init__(self, title_text: str, message_text: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title_text)
        self.setMinimumWidth(300)
        self.setStyleSheet("background-color: #0d1117; color: #c9d1d9; font-family: 'Segoe UI', sans-serif; font-size: 13px;")
        
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        
        lbl_title = QLabel(title_text)
        lbl_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff;")
        layout.addWidget(lbl_title)
        
        lbl_msg = QLabel(message_text)
        lbl_msg.setWordWrap(True)
        lbl_msg.setStyleSheet("color: #c9d1d9;")
        layout.addWidget(lbl_msg)
        
        btn_ok = QPushButton("OK")
        btn_ok.setStyleSheet("background-color: #238636; color: #ffffff; font-weight: bold; border-radius: 6px; padding: 6px 12px;")
        btn_ok.clicked.connect(self.accept)
        layout.addWidget(btn_ok)


class UpdateStatusDialog(QDialog):
    
    def __init__(self, order_id: str, current_status: str = "Pending", parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Update Order {order_id}")
        self.setMinimumWidth(320)
        self.setStyleSheet("background-color: #0d1117; color: #c9d1d9; font-family: 'Segoe UI', sans-serif; font-size: 13px;")
        
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        
        title = QLabel(f"Order #{order_id}")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff;")
        layout.addWidget(title)
        
        form = QFormLayout()
        lbl_status = QLabel("Set Status:")
        lbl_status.setStyleSheet("font-size: 12px; font-weight: 600; color: #8b949e;")
        
        self.combo_status = QComboBox()
        self.combo_status.addItems(["Pending", "Printing", "Ready for Pickup", "Completed", "Cancelled"])
        self.combo_status.setCurrentText(current_status)
        self.combo_status.setStyleSheet("background-color: #21262d; color: #f0f6fc; border: 1px solid #30363d; border-radius: 6px; padding: 6px;")
        
        form.addRow(lbl_status, self.combo_status)
        layout.addLayout(form)
        
        btn_layout = QHBoxLayout()
        btn_cancel = QPushButton("Cancel")
        btn_cancel.setStyleSheet("background-color: #21262d; color: #c9d1d9; border: 1px solid #30363d; border-radius: 6px; padding: 6px 12px;")
        btn_cancel.clicked.connect(self.reject)
        
        btn_save = QPushButton("Save")
        btn_save.setStyleSheet("background-color: #238636; color: #ffffff; font-weight: bold; border-radius: 6px; padding: 6px 12px;")
        btn_save.clicked.connect(self.accept)
        
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_save)
        layout.addLayout(btn_layout)

    def get_selected_status(self) -> str:
        return self.combo_status.currentText()
