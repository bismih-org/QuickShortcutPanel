from PyQt6.QtWidgets import (
    QVBoxLayout,
    QCheckBox,
    QLineEdit,
    QWidget,
    QLabel,
)
from src.process.pro_types import Process_Type


class CommandRunnerWidget(QWidget):
    def __init__(self, data={"command": "", "is_terminal": False}):
        super().__init__()

        # Form layout oluştur
        form_layout = QVBoxLayout()
        lb_title = QLabel("Komut:")
        self.lb_command = QLineEdit(data["command"])

        self.chkb_is_terminal = QCheckBox("Terminalde çalıştır")
        self.chkb_is_terminal.setChecked(data["is_terminal"])

        form_layout.addWidget(lb_title)
        form_layout.addWidget(self.lb_command)
        form_layout.addWidget(self.chkb_is_terminal)

        # Ana layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)

        self.setLayout(main_layout)

    def get_data(self):
        return {
            "type": Process_Type.BASH_COMMAND.name,
            "data": {
                "command": self.lb_command.text(),
                "is_terminal": self.chkb_is_terminal.isChecked(),
            },
        }
