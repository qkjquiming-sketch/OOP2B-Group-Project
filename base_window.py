from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtGui import QAction

from dialogs import showAlert

class BaseWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupMenus()
    
    # ----- Menu Bar -----
    def setupMenus(self):
        fileMenu = self.menuBar().addMenu("File")
        fileMenu.addAction(self.makeAction("Exit", self.close))
        
        helpMenu = self.menuBar().addMenu("Help")
        helpMenu.addAction(self.makeAction("About PrintSync", self.showAbout))
        
    def makeAction(self, text, slot):
        action = QAction(text, self)
        action.triggered.connect(slot)
        return action
    
    def showAbout(self):
        showAlert("About PrintSync", "PrintSync - Printing Shop Order and Queue Management System", self)
        
    def closeEvent(self, event):
        # If one window closes, the other one closes too
        QApplication.quit()
        event.accept()