from src.ui.menu_config.process_ui.config_dialog import ConfigDialog


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    dialog = ConfigDialog([])
    dialog.show()
    sys.exit(app.exec())