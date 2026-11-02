from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QFormLayout
)

# ----- showConfirmOrder -----
def showConfirmOrder(customerName, phone, source, breakdownText, totalText, parent=None):
    dialog = QDialog(parent)
    dialog.setWindowTitle("Confirm Order Submission")
    dialog.setMinimumWidth(360)
    
    # ----- Widgets -----
    titleLabel = QLabel("Confirm Your Order")
    
    infoCard = QFrame()
    nameLabel = QLabel("Customer Name:")
    phoneLabel = QLabel("Contact Number:")
    sourceLabel = QLabel("File Source:")
    
    priceTitleLabel = QLabel("Price Breakdown")
    breakdownLabel = QLabel(breakdownText)
    totalLabel = QLabel(totalText)
    
    cancelButton = QPushButton("Cancel")
    confirmButton = QPushButton("Confirm & Submit")
    
    # ----- Layout -----
    infoLayout = QFormLayout(infoCard)
    infoLayout.addRow(nameLabel, QLabel(customerName))
    infoLayout.addRow(phoneLabel, QLabel(phone))
    infoLayout.addRow(sourceLabel, QLabel(source))
    
    buttonLayout = QHBoxLayout()
    buttonLayout.addWidget(cancelButton)
    buttonLayout.addWidget(confirmButton)
    
    # ----- Main Layout -----
    dialogLayout = QVBoxLayout(dialog)
    dialogLayout.addWidget(titleLabel)
    dialogLayout.addWidget(infoCard)
    dialogLayout.addWidget(priceTitleLabel)
    dialogLayout.addWidget(breakdownLabel)
    dialogLayout.addWidget(totalLabel)
    dialogLayout.addLayout(buttonLayout)
    
    # ----- Signals -----
    cancelButton.clicked.connect(dialog.reject)
    confirmButton.clicked.connect(dialog.accept)
    
    # ----- Widget Styling -----
    titleLabel.setObjectName("dialogTitle")
    infoCard.setProperty("class", "card")
    nameLabel.setProperty("class", "field-label")
    phoneLabel.setProperty("class", "field-label")
    sourceLabel.setProperty("class", "field-label")
    priceTitleLabel.setProperty("class", "section")
    breakdownLabel.setProperty("class", "card")
    totalLabel.setObjectName("totalLabel")
    cancelButton.setProperty("class", "secondaryButton")
    confirmButton.setDefault(True)
    
    # Spacing
    infoLayout.setContentsMargins(14, 12, 14, 12)
    infoLayout.setSpacing(8)
    buttonLayout.setSpacing(8)
    dialogLayout.setContentsMargins(16, 16, 16, 16)
    dialogLayout.setSpacing(12)
    
    return dialog.exec()


# ----- showAlert -----
def showAlert(titleText, messageText, parent=None):
    dialog = QDialog(parent)
    dialog.setWindowTitle(titleText)
    dialog.setMinimumWidth(300)
    
    # ----- Widgets -----
    titleLabel = QLabel(titleText)
    messageLabel = QLabel(messageText)
    okButton = QPushButton("OK")
    
    # ----- Main Layout -----
    dialogLayout = QVBoxLayout(dialog)
    dialogLayout.addWidget(titleLabel)
    dialogLayout.addWidget(messageLabel)
    dialogLayout.addWidget(okButton)
    
    # ----- Signals -----
    okButton.clicked.connect(dialog.accept)
    
    # ----- Widget Styling -----
    titleLabel.setObjectName("dialogTitle")
    messageLabel.setWordWrap(True)
    okButton.setDefault(True)
    
    # Spacing
    dialogLayout.setContentsMargins(16, 16, 16, 16)
    dialogLayout.setSpacing(12)
    
    return dialog.exec()


# ----- showConfirmDelete -----
def showConfirmDelete(orderId, parent=None):
    dialog = QDialog(parent)
    dialog.setWindowTitle("Delete Order")
    dialog.setMinimumWidth(300)
    
    # ----- Widgets -----
    titleLabel = QLabel("Delete Order?")
    messageLabel = QLabel(f"Order {orderId} will be removed. This can't be undone.")
    
    cancelButton = QPushButton("Cancel")
    deleteButton = QPushButton("Delete")
    
    # ----- Layout -----
    buttonLayout = QHBoxLayout()
    buttonLayout.addWidget(cancelButton)
    buttonLayout.addWidget(deleteButton)
    
    # ----- Main Layout -----
    dialogLayout = QVBoxLayout(dialog)
    dialogLayout.addWidget(titleLabel)
    dialogLayout.addWidget(messageLabel)
    dialogLayout.addLayout(buttonLayout)
    
    # ----- Signals -----
    cancelButton.clicked.connect(dialog.reject)
    deleteButton.clicked.connect(dialog.accept)
    
    # ----- Widget Styling -----
    titleLabel.setObjectName("dialogTitle")
    messageLabel.setWordWrap(True)
    cancelButton.setProperty("class", "secondaryButton")
    cancelButton.setDefault(True)       # Enter = Cancel, so it's not deleted by accident
    
    # Spacing
    buttonLayout.setSpacing(8)
    dialogLayout.setContentsMargins(16, 16, 16, 16)
    dialogLayout.setSpacing(12)
    
    return dialog.exec()