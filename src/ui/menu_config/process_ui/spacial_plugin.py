from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
)
from src.process.pro_types import Process_Type


class SpacialPluginWidget(QWidget):
    def __init__(self, data={}):
        super().__init__()

        self.data = data
        data = self.data["data"]

        # Form layout oluştur
        form_layout = QVBoxLayout()
        lb_title = QLabel("Eklenti: " + data.get("title", ""))
        lb_description = QLabel("Açıklama: " + data.get("description", ""))
        ly_info = QHBoxLayout()
        lb_author = QLabel("Yazar: " + data.get("author", ""))
        lb_version = QLabel("Versiyon: " + data.get("version", ""))
        lb_license = QLabel("Lisans: " + data.get("license", ""))

        ly_info.addWidget(lb_author)
        ly_info.addWidget(lb_version)
        ly_info.addWidget(lb_license)

        lb_website = QLabel("Web sitesi: " + data.get("website", ""))
        lb_website.setOpenExternalLinks(True)
        lb_website.setText(f'<a href="{data.get("website", "")}">Web sitesi</a>')
        lb_website.setTextFormat(Qt.TextFormat.RichText)
        lb_website.setTextInteractionFlags(
            Qt.TextInteractionFlag.LinksAccessibleByMouse
        )
        lb_website.setOpenExternalLinks(True)
        lb_website.setCursor(Qt.CursorShape.PointingHandCursor)
        lb_website.setStyleSheet("color: blue; text-decoration: underline;")
        lb_website.setToolTip("Web sitesine gitmek için tıklayın.")

        lb_dependency = QLabel()
        dependencies = "Debian bağımlılıkları:\n"
        dep = dict(data.get("dependencies", {}))

        for dep_deb in dep.get("apt", []):
            dependencies = dep_deb + " " * 2

        dependencies += "\nFlatpak bağımlılıkları:\n"
        for dep_flatpak in dep.get("flatpak", []):
            dependencies += dep_flatpak + " " * 2

        lb_dependency.setText(dependencies)

        form_layout.addWidget(lb_title)
        form_layout.addWidget(lb_description)
        form_layout.addLayout(ly_info)
        form_layout.addWidget(lb_website)
        form_layout.addWidget(lb_dependency)
        form_layout.addStretch()

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)

        self.setLayout(main_layout)

    def get_data(self):
        return {
            "type": Process_Type.SPACIAL_PLUGINS.name,
            "data": self.data,
        }
