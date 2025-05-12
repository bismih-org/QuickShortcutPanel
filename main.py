from PyQt6.QtWidgets import QApplication
import sys

from src.ui.panel.main_panel import MainPanel
from PyQt6.QtGui import QIcon
import os

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Set application icon
    app_icon_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "data/icons/quick_shortcut_panel.png",
    )
    if os.path.exists(app_icon_path):
        app_icon = QIcon(app_icon_path)
        app.setWindowIcon(app_icon)
    print(sys.argv)
    window = MainPanel(int(sys.argv[1]), int(sys.argv[2]))
    window.show()
    sys.exit(app.exec())
