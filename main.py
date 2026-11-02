import os
import sys
from PyQt6.QtWidgets import QApplication

from admin_screen import AdminWindow
from user_screen import UserWindow


def main():
    app = QApplication(sys.argv)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    qss_path = os.path.join(base_dir, "style.qss")

    if os.path.exists(qss_path):
        with open(qss_path, "r") as f:
            app.setStyleSheet(f.read())
    else:
        print(f"Warning: Could not find QSS file at {qss_path}")

    screens = app.screens()
    user_win = UserWindow()
    admin_win = AdminWindow()
    user_win.admin_window = admin_win
    admin_win.user_window = user_win

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