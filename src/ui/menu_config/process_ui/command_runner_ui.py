from PyQt6.QtWidgets import (
    QVBoxLayout,
    QDialog,
    QDialogButtonBox,
    QCheckBox,
    QLineEdit,
)


class CommandRunnerDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Komut ekle")
        self.setMinimumWidth(300)

        # Form layout oluştur
        form_layout = QVBoxLayout()
        self.lb_command = QLineEdit()
        self.lb_command.setPlaceholderText("Komut girin")

        self.chkb_is_terminal = QCheckBox("Terminalde çalıştır")

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
