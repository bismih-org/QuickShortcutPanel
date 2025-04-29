from PyQt6.QtWidgets import (
    QVBoxLayout,
    QDialog,
    QDialogButtonBox,
    QCheckBox,
    QLineEdit,
)


class CommandRunnerDialog(QDialog):
    def __init__(self, data):
        super().__init__()

        self.setWindowTitle("Komut ekle")
        self.resize(350, 150)
        self.setMinimumSize(100, 100)

        # Form layout oluştur
        form_layout = QVBoxLayout()
        self.lb_command = QLineEdit(data[0]["command"])
        self.lb_command.setPlaceholderText("Komut girin")

        self.chkb_is_terminal = QCheckBox("Terminalde çalıştır")
        self.chkb_is_terminal.setChecked(data[0]["is_terminal"])

        form_layout.addWidget(self.lb_command)
        form_layout.addWidget(self.chkb_is_terminal)

        # Butonlar
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        # Ana layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(button_box)

        self.setLayout(main_layout)

    def get_data(self):
        return [
            {
                "command": self.lb_command.text(),
                "is_terminal": self.chkb_is_terminal.isChecked(),
            }
        ]
