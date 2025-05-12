import os
from xdg import DesktopEntry
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QComboBox,
    QLabel,
    QCompleter,
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize
from PyQt6.QtCore import Qt

from src.process.pro_types import Process_Type


class AppMenuViewer(QWidget):
    def __init__(self, data={}):
        super().__init__()

        form_layout = QVBoxLayout()
        lb_title = QLabel("Uygulama Seç")

        self.all_app = []
        self.selected_app = None
        self.cmb_apps = QComboBox()
        self.cmb_apps.setIconSize(QSize(32, 32))
        self.editable_combo(self.cmb_apps)

        form_layout.addWidget(lb_title)
        form_layout.addWidget(self.cmb_apps)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)

        self.setLayout(main_layout)
        self.load_apps_to_cmb()
        self.load_app(data)

    def editable_combo(self, cmb):
        cmb.setEditable(True)
        completer = QCompleter(cmb.model(), self)
        completer.setFilterMode(
            Qt.MatchFlag.MatchContains
        )  # Klavyeden yazılan kısmın elemanların herhangi bir yerinde geçmesi için
        completer.setCaseSensitivity(
            Qt.CaseSensitivity.CaseInsensitive
        )  # Büyük küçük harf hassasiyetini kapatarak aramayı yapar
        cmb.setCompleter(completer)

    def load_apps_to_cmb(self):
        desktop_dir = "/usr/share/applications/"
        for filename in os.listdir(desktop_dir):
            if filename.endswith(".desktop"):
                file_path = os.path.join(desktop_dir, filename)
                try:
                    entry = DesktopEntry.DesktopEntry(file_path)
                    if not entry.getHidden() and entry.getName() and entry.getExec():
                        item = f"{entry.getName()}"
                        self.all_app.append([entry.getName(), entry.getExec()])
                        icon_name = entry.getIcon()
                        self.cmb_apps.addItem(
                            QIcon.fromTheme(
                                icon_name,
                                QIcon("data/icons/quick_shortcut_panel.png"),
                            ),
                            item,
                        )
                except Exception as e:
                    print(f"Error loading {filename}: {e}")

    def load_app(self, data):
        if not data:
            return
        self.cmb_apps.clear()
        self.load_apps_to_cmb()
        app_name = data.get("name", "")
        for i in range(self.cmb_apps.count()):
            if self.cmb_apps.itemText(i) == app_name:
                self.cmb_apps.setCurrentIndex(i)
                break

    def get_data(self):
        if self.cmb_apps.currentText() == "":
            return None
        app_name = self.cmb_apps.currentText()
        app_exec = self.all_app[self.cmb_apps.currentIndex()][1]
        return {
            "type": Process_Type.RUN_APP.name,
            "data": {
                "name": app_name,
                "exec": app_exec,
            },
        }
