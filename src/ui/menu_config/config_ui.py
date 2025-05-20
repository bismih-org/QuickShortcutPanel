from PyQt6.QtWidgets import (
    QMainWindow,
    QTreeWidget,
    QTreeWidgetItem,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QMessageBox,
)
from PyQt6.QtCore import Qt
import json

from src.ui.menu_config.piece_node import build_tree, PieceNode
from src.ui.menu_config.process_ui.config_dialog import ConfigDialog
from src.static.config import Configs as cfg
from src.ui.theme.theme_manager import ThemeManager


class ConfigPanel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menu Configurator")
        self.setGeometry(100, 100, 800, 500)
        self.theme_manager = ThemeManager()
        self.theme_manager.apply_theme(dark_mode=False)  # Aydınlık tema başlangıçta

        self.init_variables()
        self.main_ui()

    def init_variables(self):
        self.data_path = cfg.menu_json_path
        with open(self.data_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.root = build_tree(data[0])

        self.menu_count = 1

    def main_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout(self.central_widget)

        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(["Menü", "ID", "Açıklama", "Veri"])
        self.tree_widget.setColumnWidth(0, 200)
        self.tree_widget.setColumnWidth(1, 50)
        self.tree_widget.setMinimumWidth(300)
        self.tree_widget.setMinimumHeight(400)
        self.tree_widget.setAlternatingRowColors(True)

        self.load_data()
        self.tree_widget.expandAll()
        self.main_layout.addWidget(self.tree_widget)

        self.button_ui()

    def button_ui(self):
        self.button_layout = QVBoxLayout()

        self.btn_add = QPushButton("Menü Ekle")
        self.btn_edit = QPushButton("Menü Düzenle")
        self.btn_delete = QPushButton("Menü Sil")
        self.btn_save = QPushButton("Kaydet")
        
        # Tema değiştirme
        self.btn_toggle_theme = QPushButton()
        self.btn_toggle_theme.setObjectName("btn_toggle_theme")
        # Tema düğmesinin metnini güncelle
        self._update_theme_button_text()
        self.btn_toggle_theme.clicked.connect(self.toggle_theme)


        self.btn_add.clicked.connect(self.add_child_node)
        self.btn_edit.clicked.connect(self.edit_child_node)
        self.btn_delete.clicked.connect(self.delete_child_node)
        self.btn_save.clicked.connect(self.save_json)

        self.button_layout.addWidget(self.btn_add)
        self.button_layout.addWidget(self.btn_edit)
        self.button_layout.addWidget(self.btn_delete)
        self.button_layout.addWidget(self.btn_save)
        self.button_layout.addWidget(self.btn_toggle_theme)

        self.main_layout.addLayout(self.button_layout)

    def _update_theme_button_text(self):
        """Tema düğmesinin metnini günceller."""
        is_dark = getattr(self.theme_manager, "is_dark_mode", True)
        theme_text = "Aydınlık Tema" if is_dark else "Karanlık Tema"
        self.btn_toggle_theme.setText(f"{theme_text}'ya Geç")


    def toggle_theme(self):
        """Aydınlık/karanlık tema arasında geçiş yap"""
        is_dark = self.theme_manager.toggle_theme()
        theme_text = "Aydınlık Tema" if is_dark else "Karanlık Tema"
        self.btn_toggle_theme.setText(f"{theme_text}'ya Geç")

    def add_child_node(self):
        selected_items = self.tree_widget.selectedItems()

        if not selected_items:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir menü seçin.")
            return

        selected_item = selected_items[0]
        parent_node = selected_item.data(0, Qt.ItemDataRole.UserRole)
        dialog = ConfigDialog(parent=self)

        if dialog.exec():
            node_data = dialog.get_data()
            if not node_data["title"]:
                QMessageBox.warning(self, "Uyarı", "Başlık boş olamaz.")
                return

            new_node = PieceNode(
                node_data["title"],
                self.menu_count,
                node_data["description"],
                node_data["data"],
            )
            self.menu_count += 1
            parent_node.children.append(new_node)  # Update data model

            # Create and add the new item to the tree widget
            new_item = self.node_on_tree(new_node)

            selected_item.addChild(new_item)  # Add item to the tree view
            selected_item.setExpanded(True)

    def edit_child_node(self):
        selected_items = self.tree_widget.selectedItems()
        if not selected_items:
            return

        selected_item = selected_items[0]
        node = selected_item.data(0, Qt.ItemDataRole.UserRole)

        dialog = ConfigDialog(
            title=node.title,
            description=node.description,
            proc_data=node.data,
            parent=self,
        )
        if dialog.exec():
            node_data = dialog.get_data()

            # Düğümü güncelle
            node.title = node_data["title"]
            node.description = node_data["description"]
            node.data = node_data["data"]

            # Görünümü güncelle
            self.node_on_tree(node, selected_item)
            selected_item.setExpanded(True)

    def delete_child_node(self):
        selected_items = self.tree_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir menü seçin.")
            return

        selected_item = selected_items[0]
        parent_item = selected_item.parent()

        if not parent_item:
            QMessageBox.warning(self, "Uyarı", "Kök düğüm silinemez.")
            return

        # Onay iste
        reply = QMessageBox.question(
            self,
            "Onay",
            "Bu ögeyi ve tüm alt ögelerini silmek istediğinizden emin misiniz?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.No:
            return

        # Düğümü sil
        parent_node = parent_item.data(0, Qt.ItemDataRole.UserRole)
        node = selected_item.data(0, Qt.ItemDataRole.UserRole)

        # Ebeveyn düğümün çocuklarından kaldır
        parent_node.children.remove(node)

        # TreeWidget'tan kaldır
        parent_item.removeChild(selected_item)

    def load_data(self):
        root_item = QTreeWidgetItem(self.tree_widget)
        self.node_on_tree(self.root, root_item)

        if self.root.children:
            self.process_children(root_item, self.root.children)

    def process_children(self, parent_item, children):
        self.menu_count += len(children)
        for child in children:
            child_item = QTreeWidgetItem(parent_item)
            self.node_on_tree(child, child_item)

            if child.children:
                self.process_children(child_item, child.children)

    def node_on_tree(self, node, item=None):
        new_item = item if item else QTreeWidgetItem()
        new_item.setText(0, node.title)
        new_item.setText(1, str(node.id))
        new_item.setText(2, node.description)
        new_item.setText(3, str(node.data))
        new_item.setData(0, Qt.ItemDataRole.UserRole, node)

        return new_item

    def save_json(self):
        # Kök düğümü al
        json_data = [self.root.to_dict()]
        print(json_data)
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
