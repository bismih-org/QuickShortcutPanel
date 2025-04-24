from PyQt6.QtWidgets import QApplication
import sys

from src.ui.panel.main_panel import MainPanel
from src.ui.test import QuickShortcutPanel
from src.ui.menu_config.config_ui import ConfigPanel

if __name__ == "__main__":
    app = QApplication(sys.argv)
    print(sys.argv)
    window = MainPanel(sys.argv[1],sys.argv[2])
    # window = ConfigPanel()
    window.show()
    sys.exit(app.exec())
