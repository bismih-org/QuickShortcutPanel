from PyQt6.QtWidgets import (
    QVBoxLayout,
    QLineEdit,
    QDialog,
    QFormLayout,
    QDialogButtonBox,
    QComboBox,
)

from src.process.pro_types import Process_Type


class NodeEditDialog(QDialog):
    def __init__(
        self,
        title="",
        type_=Process_Type.BASH_COMMAND.value,
        description="",
        parent=None,
    ):
        super().__init__(parent)
        self.setWindowTitle("Düğüm Düzenle")
        self.setMinimumWidth(300)

        # Form layout oluştur
        form_layout = QFormLayout()

        # Başlık alanı
        self.title_edit = QLineEdit(title)
        self.cmb_type = QComboBox()
        for pro in Process_Type:
            self.cmb_type.addItem(pro.value, pro.name)
        self.cmb_type.setCurrentText(type_)
        self.lbe_description = QLineEdit(description)
        self.lbe_description.setToolTip("Açıklama giriniz")

        form_layout.addRow("Başlık:", self.title_edit)
        form_layout.addRow("Tür:", self.cmb_type)
        form_layout.addRow("Açıklama:", self.lbe_description)

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
            "type": self.cmb_type.currentData(),
            "description": self.lbe_description.text(),
        }
