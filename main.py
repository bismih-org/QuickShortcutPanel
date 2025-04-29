from PyQt6.QtWidgets import QApplication
import sys

from src.ui.panel.main_panel import MainPanel

if __name__ == "__main__":
    app = QApplication(sys.argv)
    print(sys.argv)
    window = MainPanel(int(sys.argv[1]), int(sys.argv[2]))
    window.show()
    sys.exit(app.exec())
