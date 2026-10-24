import sys
from PyQt6.QtWidgets import QApplication

from user_screen import UserWindow
from admin_screen import AdminWindow

def main():
    app = QApplication(sys.argv)

    screens = app.screens()
    user_win = UserWindow()
    admin_win = AdminWindow()

    if len(screens) >= 2:
        user_win.setScreen(screens[0])
        user_win.showMaximized()
        admin_win.setScreen(screens[1])
        admin_win.showMaximized()
    else:
        user_win.show()
        admin_win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()