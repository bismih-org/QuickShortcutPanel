import os
from xdg import DesktopEntry
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QListWidget,
    QListWidgetItem,
    QDialog,
    QDialogButtonBox,
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize


class AppMenuViewer(QDialog):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Uygulama Seç")
        self.resize(350, 550)
        self.setMinimumSize(100, 100)

        self.selected_index = 0
        self.all_app = []

        self.app_list = QListWidget()
        self.app_list.setIconSize(QSize(32, 32))
        self.app_list.setAlternatingRowColors(True)
        self.app_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.app_list.itemClicked.connect(self.on_item_clicked)

        # Butonlar
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.app_list)
        main_layout.addWidget(button_box)

        self.setLayout(main_layout)
        self.load_applications()

    def on_item_clicked(self, item):
        self.selected_index = self.app_list.row(item)

    def load_applications(self):
        desktop_dir = "/usr/share/applications/"
        for filename in os.listdir(desktop_dir):
            if filename.endswith(".desktop"):
                file_path = os.path.join(desktop_dir, filename)
                try:
                    entry = DesktopEntry.DesktopEntry(file_path)
                    if not entry.getHidden() and entry.getName() and entry.getExec():
                        item = QListWidgetItem(f"{entry.getName()}")
                        self.all_app.append([entry.getName(), entry.getExec()])
                        icon_name = entry.getIcon()
                        item.setIcon(
                            QIcon.fromTheme(
                                icon_name,
                                QIcon.fromTheme("application-x-executable"),
                            )
                        )
                        self.app_list.addItem(item)
                except Exception as e:
                    print(f"Error loading {filename}: {e}")

    def get_data(self):
        return {
            "selected_app": self.all_app[self.selected_index][0],
            "selected_app_exec": self.all_app[self.selected_index][1],
        }
