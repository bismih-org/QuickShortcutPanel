from PyQt6.QtWidgets import QApplication
import sys

from src.ui.panel.main_panel import MainPanel
from src.ui.test import QuickShortcutPanel

if __name__ == "__main__":
    app = QApplication(sys.argv)
    print(sys.argv)
    window = MainPanel(sys.argv[1],sys.argv[2])
    window.show()
    sys.exit(app.exec())