from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QCheckBox,
    QLineEdit,
    QWidget,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
)
from PyQt6.QtCore import Qt
import ast

from src.process.pro_types import Process_Type


class LinkOpenerWidget(QWidget):
    def __init__(self, data={}):
        super().__init__()

        # Form layout oluştur
        form_layout = QVBoxLayout()
        lb_title = QLabel("Link Açıcı")

        self.lst_links = QListWidget()
        self.lbe_link = QLineEdit()
        self.btn_add_link = QPushButton("Link Ekle")
        self.btn_remove_link = QPushButton("Link Kaldır")

        self.btn_add_link.clicked.connect(self.on_add_link)
        self.btn_remove_link.clicked.connect(self.on_remove_link)
        self.btn_add_link.setToolTip("Linki eklemek için tıklayın.")
        self.btn_remove_link.setToolTip("Seçili linki kaldırmak için tıklayın.")

        form_layout.addWidget(lb_title)
        ly_btn = QHBoxLayout()
        ly_btn.addWidget(self.btn_add_link)
        ly_btn.addWidget(self.btn_remove_link)
        form_layout.addLayout(ly_btn)
        form_layout.addWidget(QLabel("Linki buraya yazın:"))
        form_layout.addWidget(self.lbe_link)
        form_layout.addWidget(QLabel("Açılacak linkler:"))
        form_layout.addWidget(self.lst_links)

        # Ana layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)

        self.setLayout(main_layout)

        self.load_links(data.get("links", "[]"))

    def load_links(self, links):
        if not links:
            return
        self.lst_links.clear()

        for link in links:
            item = QListWidgetItem(link)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.lst_links.addItem(item)
        self.lbe_link.clear()

    def on_add_link(self):
        link = self.lbe_link.text()
        if link:
            item = QListWidgetItem(link)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.lst_links.addItem(item)
            self.lbe_link.clear()
        else:
            print("Link boş olamaz!")

    def on_remove_link(self):
        selected_items = self.lst_links.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            self.lst_links.takeItem(self.lst_links.row(item))

    def get_data(self):
        links = []
        for i in range(self.lst_links.count()):
            item = self.lst_links.item(i)
            links.append(item.text())
        return {
            "type": Process_Type.OPEN_LINK.name,
            "data": {
                "links": links,
            },
        }
