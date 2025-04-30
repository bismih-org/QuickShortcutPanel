from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QDialog,
    QDialogButtonBox,
    QPushButton,
    QComboBox,
    QLineEdit,
    QLabel,
    QListWidget,
    QListWidgetItem,
)

from src.process.pro_types import Process_Type
from src.ui.menu_config.process_ui.command_runner_ui import CommandRunnerWidget
from src.ui.menu_config.process_ui.short_cut_selector import ShortCutSelector


class ConfigDialog(QDialog):
    def __init__(self, title = "", description="", proc_data={}, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Aksiyon ekle")
        self.resize(750, 450)

        self.title = title
        self.description = description

        self.ly_btn = QHBoxLayout()
        self.lst_widgets = QListWidget()
        self.lst_widgets.setAlternatingRowColors(True)
        self.lst_widgets.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.lst_widgets.setSelectionBehavior(QListWidget.SelectionBehavior.SelectRows)

        self.btn_layout()

        # Butonlar
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        # Ana layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.title_ui())
        main_layout.addLayout(self.ly_btn)
        main_layout.addWidget(self.lst_widgets)
        main_layout.addWidget(button_box)

        self.setLayout(main_layout)

        self.load_data(proc_data)

    def title_ui(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        self.lbe_title = QLineEdit()
        self.lbe_description = QLineEdit()

        layout.addWidget(QLabel("Başlık:"))
        layout.addWidget(self.lbe_title)
        layout.addWidget(QLabel("Açıklama:"))
        layout.addWidget(self.lbe_description)

        return layout



    def btn_layout(self):

        self.btn_add = QPushButton("Ekle")
        self.btn_delete = QPushButton("Sil")
        self.cmb_type = QComboBox()

        self.btn_add.clicked.connect(self.on_add_widget)
        self.btn_delete.clicked.connect(self.delete_widget)
        for pro in Process_Type:
            self.cmb_type.addItem(pro.value, pro.name)

        self.cmb_type.setCurrentIndex(0)
        self.cmb_type.setToolTip("Aksiyon türünü seçin")

        self.ly_btn.addWidget(self.btn_add)
        self.ly_btn.addWidget(self.btn_delete)
        self.ly_btn.addWidget(self.cmb_type)

    def add_widget(self, type_, data=None):
        item = QListWidgetItem()
        if type_ == Process_Type.BASH_COMMAND.value:
            if data is None:
                widget = CommandRunnerWidget()
            else:
                widget = CommandRunnerWidget(data)
        elif type_ == Process_Type.KEYBOARD_SHORTCUT.value:
            if data is None:
                widget = ShortCutSelector()
            else:
                widget = ShortCutSelector(data)

        item.setSizeHint(widget.sizeHint())
        self.lst_widgets.addItem(item)
        # iteme widget ekleme
        self.lst_widgets.setItemWidget(item, widget)

    def on_add_widget(self):
        process_type = self.cmb_type.currentText()
        self.add_widget(process_type)

    def delete_widget(self):
        current_row = self.lst_widgets.currentRow()
        if current_row != -1:
            self.lst_widgets.takeItem(current_row)

    def load_data(self, data):
        self.lbe_title.setText(self.title)
        self.lbe_description.setText(self.description)
        self.lst_widgets.clear()
        for item in data:
            if item["type"] == Process_Type.BASH_COMMAND.name:
                widget = CommandRunnerWidget(item["data"])
            elif item["type"] == Process_Type.KEYBOARD_SHORTCUT.name:
                widget = ShortCutSelector(item["data"])
            else:
                continue

            list_item = QListWidgetItem()
            list_item.setSizeHint(widget.sizeHint())
            self.lst_widgets.addItem(list_item)
            self.lst_widgets.setItemWidget(list_item, widget)

    def get_data(self):
        data = []
        for i in range(self.lst_widgets.count()):
            item = self.lst_widgets.item(i)
            widget = self.lst_widgets.itemWidget(item)
            data.append(widget.get_data())
        return {
            "title": self.lbe_title.text(),
            "description": self.lbe_description.text(),
            "data": data,
        }
