from PyQt6.QtWidgets import (
    QVBoxLayout,
    QDialog,
    QDialogButtonBox,
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QListWidget,
    QListWidgetItem,
)


class ShortCutSelectorDialog(QDialog):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Düğüm Düzenle")
        self.resize(350, 150)
        self.setMinimumSize(100, 100)

        self.all_data = []

        # Form layout oluştur
        form_layout = QVBoxLayout()
        btn_layout = QHBoxLayout()
        shortcut_layout = QHBoxLayout()

        self.title_label = QLabel("Kısayolu Seçin:")
        form_layout.addWidget(self.title_label)
        self.lst_shortcut = QListWidget()
        self.lst_shortcut.setAlternatingRowColors(True)
        self.lst_shortcut.setSelectionMode(QListWidget.SelectionMode.SingleSelection)

        # Modifier checkboxes
        self.ctrl_checkbox = QCheckBox("Ctrl")
        self.alt_checkbox = QCheckBox("Alt")
        self.shift_checkbox = QCheckBox("Shift")
        self.meta_checkbox = QCheckBox("Win/Meta")

        btn_add_shortcut = QPushButton("Kısayol Ekle")
        btn_add_shortcut.clicked.connect(self.add_shortcut)
        btn_delete_shortcut = QPushButton("Kısayol Sil")
        btn_delete_shortcut.clicked.connect(self.delete_shortcut)

        shortcut_layout.addWidget(self.ctrl_checkbox)
        shortcut_layout.addWidget(self.alt_checkbox)
        shortcut_layout.addWidget(self.shift_checkbox)
        shortcut_layout.addWidget(self.meta_checkbox)

        btn_layout.addWidget(btn_delete_shortcut)
        btn_layout.addWidget(btn_add_shortcut)

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
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.lst_shortcut)
        main_layout.addWidget(button_box)

        self.setLayout(main_layout)

        self.load_shortcut(data)
        self.lst_shortcut.setCurrentRow(0)

    def add_shortcut(self):
        self.all_data.append(
            {
                "ctrl": self.ctrl_checkbox.isChecked(),
                "alt": self.alt_checkbox.isChecked(),
                "shift": self.shift_checkbox.isChecked(),
                "meta": self.meta_checkbox.isChecked(),
                "key": self.key_combo.currentText().lower(),
            }
        )

    def delete_shortcut(self):
        current_row = self.lst_shortcut.currentRow()
        if current_row != -1:
            self.lst_shortcut.takeItem(current_row)
            del self.all_data[current_row]
        else:
            print("No item selected to delete.")

    def load_shortcut(self, data):
        self.all_data = data
        self.lst_shortcut.clear()
        for shortcut in data:
            item = QListWidgetItem(
                f"{'Ctrl+' if shortcut['ctrl'] else ''}"
                f"{'Alt+' if shortcut['alt'] else ''}"
                f"{'Shift+' if shortcut['shift'] else ''}"
                f"{'Meta+' if shortcut['meta'] else ''}"
                f"{shortcut['key']}"
            )
            self.lst_shortcut.addItem(item)
        self.lst_shortcut.setCurrentRow(0)

    def get_data(self):
        return self.all_data


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    dialog = ShortCutSelectorDialog()
    if dialog.exec() == QDialog.DialogCode.Accepted:
        data = dialog.get_data()
        print(data)
    sys.exit(app.exec())
