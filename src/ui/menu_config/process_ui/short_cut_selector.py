from PyQt6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QComboBox,
)
from src.process.pro_types import Process_Type


class ShortCutSelector(QWidget):
    def __init__(self, data={}, parent=None):
        super().__init__(parent)

        # Form layout oluştur
        form_layout = QVBoxLayout()
        shortcut_layout = QHBoxLayout()

        title_label = QLabel("Kısayolu Seçin:")
        form_layout.addWidget(title_label)

        self.ctrl_checkbox = QCheckBox("Ctrl")
        self.alt_checkbox = QCheckBox("Alt")
        self.shift_checkbox = QCheckBox("Shift")
        self.meta_checkbox = QCheckBox("Meta")

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

        self.load_shortcut(data)
        self.setLayout(form_layout)

    def load_shortcut(self, data):
        self.ctrl_checkbox.setChecked(data.get("ctrl", False))
        self.alt_checkbox.setChecked(data.get("alt", False))
        self.shift_checkbox.setChecked(data.get("shift", False))
        self.meta_checkbox.setChecked(data.get("meta", False))
        self.key_combo.setCurrentText(data.get("key", "A"))

    def get_data(self):
        return {
            "type": Process_Type.KEYBOARD_SHORTCUT.name,
            "data": {
                "ctrl": self.ctrl_checkbox.isChecked(),
                "alt": self.alt_checkbox.isChecked(),
                "shift": self.shift_checkbox.isChecked(),
                "meta": self.meta_checkbox.isChecked(),
                "key": self.key_combo.currentText(),
            },
        }
