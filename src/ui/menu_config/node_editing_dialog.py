from PyQt6.QtWidgets import (
    QVBoxLayout,
    QLineEdit,
    QDialog,
    QFormLayout,
    QDialogButtonBox,
)

class NodeEditDialog(QDialog):
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Düğüm Düzenle")
        self.setMinimumWidth(300)

        # Form layout oluştur
        form_layout = QFormLayout()

        # Başlık alanı
        self.title_edit = QLineEdit(title)
        form_layout.addRow("Başlık:", self.title_edit)

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
            "title": self.title_edit.text(),
        }