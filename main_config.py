from PyQt6.QtWidgets import QApplication
import sys

from src.ui.menu_config.config_ui import ConfigPanel

if __name__ == "__main__":
    app = QApplication(sys.argv)
    print(sys.argv)
    window = ConfigPanel()
    window.show()
    sys.exit(app.exec())
