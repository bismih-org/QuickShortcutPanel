from PyQt6.QtWidgets import QApplication
import sys

from ui.test import QuickShortcutPanel

if __name__ == "__main__":
    app = QApplication(sys.argv)
    print(sys.argv)
    window = QuickShortcutPanel(sys.argv[1],sys.argv[2])
    window.show()
    sys.exit(app.exec())