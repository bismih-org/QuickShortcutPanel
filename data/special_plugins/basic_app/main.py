import sys
from PyQt6.QtWidgets import QApplication
from basic_app import BasicApp


def run_plugin():
    app = QApplication(sys.argv)
    window = BasicApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run_plugin()
