from PyQt6.QtWidgets import (
    QVBoxLayout,
    QDialog,
    QDialogButtonBox,
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QComboBox,
)


class ShortCutSelectorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Düğüm Düzenle")
        self.setMinimumWidth(300)

        self.all_data = []

        # Form layout oluştur
        form_layout = QVBoxLayout()
        shortcut_layout = QHBoxLayout()

        self.title_label = QLabel("Kısayolu Seçin:")
        form_layout.addWidget(self.title_label)

        # Modifier checkboxes
        self.ctrl_checkbox = QCheckBox("Ctrl")
        self.alt_checkbox = QCheckBox("Alt")
        self.shift_checkbox = QCheckBox("Shift")
        self.meta_checkbox = QCheckBox("Win/Meta")

        shortcut_layout.addWidget(self.ctrl_checkbox)
        shortcut_layout.addWidget(self.alt_checkbox)
        shortcut_layout.addWidget(self.shift_checkbox)
        shortcut_layout.addWidget(self.meta_checkbox)

        # Key dropdown
        self.key_combo = QComboBox()
        for k in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
            self.key_combo.addItem(k)

        # Add function keys
        for i in range(1, 13):
            self.key_combo.addItem(f"F{i}")

        # Add special keys
        for k in [
            "Esc",
            "Tab",
            "Space",
            "Enter",
            "Delete",
            "Home",
            "End",
            "PgUp",
            "PgDn",
            "Up",
            "Down",
            "Left",
            "Right",
        ]:
            self.key_combo.addItem(k)
        shortcut_layout.addWidget(self.key_combo)

        form_layout.addLayout(shortcut_layout)

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
        return {
            "ctrl": self.ctrl_checkbox.isChecked(),
            "alt": self.alt_checkbox.isChecked(),
            "shift": self.shift_checkbox.isChecked(),
            "meta": self.meta_checkbox.isChecked(),
            "key": self.key_combo.currentText().lower(),
        }


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    dialog = ShortCutSelectorDialog()
    if dialog.exec() == QDialog.DialogCode.Accepted:
        data = dialog.get_data()
        print(data)
    sys.exit(app.exec())