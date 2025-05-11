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
from src.ui.menu_config.process_ui.spacial_plugin import SpacialPluginWidget
from src.process.plugin_manager import (
    get_plugins,
    save_plugin_data,
    get_special_plugins,
)


class ConfigDialog(QDialog):
    def __init__(self, title="", description="", proc_data=[], parent=None):
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
        self.cmb_plugins = QComboBox()
        self.cmb_spacial_plugins = QComboBox()
        self.btn_save_prepared = QPushButton("Eklenti olarak kaydet")

        self.cmb_plugins.setVisible(False)
        self.cmb_spacial_plugins.setVisible(False)
        self.btn_add.clicked.connect(self.on_add_widget)
        self.btn_save_prepared.clicked.connect(self.on_save_plugin)
        self.btn_delete.clicked.connect(self.delete_widget)
        for pro in Process_Type:
            self.cmb_type.addItem(pro.value, pro.name)

        for p, data in get_plugins():
            self.cmb_plugins.addItem(p, data)

        self.cmb_type.setCurrentIndex(0)
        self.cmb_type.setToolTip("Aksiyon türünü seçin")
        self.cmb_type.currentIndexChanged.connect(self.on_cmb_type_changed)

        self.ly_btn.addWidget(self.btn_add)
        self.ly_btn.addWidget(self.btn_delete)
        self.ly_btn.addWidget(self.cmb_type)
        self.ly_btn.addWidget(self.cmb_plugins)
        self.ly_btn.addWidget(self.cmb_spacial_plugins)
        self.ly_btn.addWidget(self.btn_save_prepared)

    def on_cmb_type_changed(self):
        if self.cmb_type.currentText() == Process_Type.PREPARED_PLUGINS.value:
            self.cmb_plugins.setVisible(True)
            self.cmb_spacial_plugins.setVisible(False)
            self.cmb_plugins.clear()
            for p, data in get_plugins():
                self.cmb_plugins.addItem(p, data)
        elif self.cmb_type.currentText() == Process_Type.SPACIAL_PLUGINS.value:
            self.cmb_spacial_plugins.setVisible(True)
            self.cmb_plugins.setVisible(False)
            self.cmb_spacial_plugins.clear()
            for p in get_special_plugins():
                self.cmb_spacial_plugins.addItem(p["data"]["title"], p)
        else:
            self.cmb_plugins.setVisible(False)
            self.cmb_spacial_plugins.setVisible(False)

    def add_widget(self, type_, data=None):
        item = QListWidgetItem()
        if type_ == Process_Type.BASH_COMMAND.name:
            if data is None:
                widget = CommandRunnerWidget()
            else:
                widget = CommandRunnerWidget(data)
        elif type_ == Process_Type.KEYBOARD_SHORTCUT.name:
            if data is None:
                widget = ShortCutSelector()
            else:
                widget = ShortCutSelector(data)
        elif type_ == Process_Type.PREPARED_PLUGINS.name:
            self.load_data(self.cmb_plugins.currentData())
            return
        elif type_ == Process_Type.SPACIAL_PLUGINS.name:
            print(self.cmb_spacial_plugins.currentData())
            if data is None:
                widget = SpacialPluginWidget(self.cmb_spacial_plugins.currentData())
            else:
                widget = SpacialPluginWidget(data)
        else:
            return

        item.setSizeHint(widget.sizeHint())
        self.lst_widgets.addItem(item)
        # iteme widget ekleme
        self.lst_widgets.setItemWidget(item, widget)

    def on_add_widget(self):
        process_type = self.cmb_type.currentText()
        self.add_widget(Process_Type(process_type).name)

    def delete_widget(self):
        current_row = self.lst_widgets.currentRow()
        if current_row != -1:
            self.lst_widgets.takeItem(current_row)

    def load_data(self, data):
        self.lbe_title.setText(self.title)
        self.lbe_description.setText(self.description)
        for item in data:
            self.add_widget(item["type"], item["data"])

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

    def on_save_plugin(self):
        data = self.get_data()
        if not data["title"]:
            return
        if not data["description"]:
            return
        if not data["data"]:
            return

        # Eklenti kaydetme işlemleri
        save_plugin_data(plugin_name=data["title"], data=data["data"])
