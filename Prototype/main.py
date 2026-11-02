import os
import sys
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from admin_screen import AdminWindow
from user_screen import UserWindow


def main():
    app = QApplication(sys.argv)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    if getattr(sys, "_MEIPASS", None):
        base_dir = sys._MEIPASS

    qss_path = os.path.join(base_dir, "style.qss")
    price_path = os.path.join(base_dir, "price.txt")
    background_path = os.path.join(base_dir, "darkwindows.png")
    background_url = background_path.replace("\\", "/")
    icon_path = os.path.join(base_dir, "Print icon.png")

    if os.path.exists(qss_path):
        with open(qss_path, "r", encoding="utf-8") as f:
            qss = f.read().replace("url(darkwindows.png)", f'url("{background_url}")')
            app.setStyleSheet(qss)
    else:
        print(f"Warning: Could not find QSS file at {qss_path}")

    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    screens = app.screens()
    user_win = UserWindow()
    admin_win = AdminWindow()
    user_win.admin_window = admin_win
    admin_win.user_window = user_win

    if os.path.exists(icon_path):
        user_win.setWindowIcon(QIcon(icon_path))
        admin_win.setWindowIcon(QIcon(icon_path))

    if os.path.exists(price_path):
        try:
            with open(price_path, "r", encoding="utf-8") as f:
                saved_values = [int(line.strip()) for line in f if line.strip()]
                if len(saved_values) == 7:
                    user_win.set_prices(*saved_values)
        except Exception:
            pass

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