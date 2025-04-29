from PyQt6.QtWidgets import (
    QVBoxLayout,
    QLineEdit,
    QDialog,
    QFormLayout,
    QDialogButtonBox,
    QComboBox,
    QPushButton,
)

from src.process.pro_types import Process_Type
from src.ui.menu_config.process_ui.command_runner_ui import CommandRunnerDialog
from src.ui.menu_config.process_ui.short_cut_selector import ShortCutSelectorDialog


class NodeEditDialog(QDialog):
    def __init__(
        self,
        title="",
        type_=Process_Type.BASH_COMMAND.value,
        description="",
        proc_data=[],
        parent=None,
    ):
        super().__init__(parent)
        self.setWindowTitle("Düğüm Düzenle")
        self.setMinimumWidth(300)

        # Form layout oluştur
        form_layout = QFormLayout()

        self.proc_data = proc_data

        # Başlık alanı
        self.title_edit = QLineEdit(title)
        self.cmb_type = QComboBox()
        for pro in Process_Type:
            self.cmb_type.addItem(pro.value, pro.name)
        print(type_)
        self.cmb_type.setCurrentText(Process_Type.get_name(type_))
        self.lbe_description = QLineEdit(description)
        self.lbe_description.setToolTip("Açıklama giriniz")

        btn_proc_settings = QPushButton("Menü Aksiyonu Ayarla")
        btn_proc_settings.clicked.connect(self.set_data)

        form_layout.addRow("Başlık:", self.title_edit)
        form_layout.addRow("Tür:", self.cmb_type)
        form_layout.addRow("Açıklama:", self.lbe_description)
        form_layout.addRow("Aksiyon:", btn_proc_settings)

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

    def set_data(self):
        if self.cmb_type.currentText() == Process_Type.BASH_COMMAND.value:
            dialog = CommandRunnerDialog(self.proc_data)
        elif self.cmb_type.currentText() == Process_Type.KEYBOARD_SHORTCUT.value:
            dialog = ShortCutSelectorDialog(self.proc_data)

        if dialog.exec():
            data = dialog.get_data()
            self.proc_data = data

    def get_data(self):
        return {
            "title": self.title_edit.text(),
            "type": self.cmb_type.currentData(),
            "description": self.lbe_description.text(),
            "data": self.proc_data,
        }
