import sys
import yaml
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTreeWidget,
    QTreeWidgetItem,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
    QLineEdit,
    QMessageBox,
    QFileDialog,
    QInputDialog,
    QDialog,
    QFormLayout,
    QDialogButtonBox,
)
from PyQt6.QtCore import Qt

from src.ui.menu_config.piece_node import build_tree, PieceNode
from src.ui.menu_config.node_editing_dialog import NodeEditDialog



class ConfigPanel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menu Configurator")
        self.setGeometry(100, 100, 800, 500)

        self.init_variables()
        self.main_ui()


    def init_variables(self):
        self.yaml_path = "data/menu.yaml"
        with open(self.yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        self.root = build_tree(data[0])

        self.menu_count = 1

    def main_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout(self.central_widget)

        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(["Menü", "ID"])
        self.tree_widget.itemSelectionChanged.connect(self.on_item_selected)
        self.tree_widget.setColumnWidth(0, 200)
        self.tree_widget.setColumnWidth(1, 50)
        self.tree_widget.setMinimumWidth(300)
        self.tree_widget.setMinimumHeight(400)
        self.tree_widget.setAlternatingRowColors(True)

        self.load_yaml()
        self.tree_widget.expandAll()
        self.main_layout.addWidget(self.tree_widget)

        self.button_ui()


    def button_ui(self):
        self.button_layout = QVBoxLayout()

        self.btn_add = QPushButton("Menü Ekle")
        self.btn_edit = QPushButton("Menü Düzenle")
        self.btn_delete = QPushButton("Menü Sil")
        self.btn_save = QPushButton("Kaydet")

        self.btn_add.clicked.connect(self.add_child_node)
        self.btn_edit.clicked.connect(self.edit_child_node)
        self.btn_delete.clicked.connect(self.delete_child_node)
        self.btn_save.clicked.connect(self.save_yaml)

        self.button_layout.addWidget(self.btn_add)
        self.button_layout.addWidget(self.btn_edit)
        self.button_layout.addWidget(self.btn_delete)
        self.button_layout.addWidget(self.btn_save)

        self.main_layout.addLayout(self.button_layout)




    def on_item_selected(self):
        is_selected = len(self.tree_widget.selectedItems()) > 0
        print(is_selected)

    def add_child_node(self):
        selected_items = self.tree_widget.selectedItems()

        if not selected_items:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir menü seçin.")
            return

        selected_item = selected_items[0]
        parent_node = selected_item.data(0, Qt.ItemDataRole.UserRole)
        dialog = NodeEditDialog(parent=self)

        if dialog.exec():
            node_data = dialog.get_data()
            if not node_data["title"]:
                QMessageBox.warning(self, "Uyarı", "Başlık boş olamaz.")
                return

            new_node = PieceNode(node_data["title"], self.menu_count)
            self.menu_count += 1
            parent_node.children.append(new_node)  # Update data model

            # Create and add the new item to the tree widget
            new_item = QTreeWidgetItem()
            new_item.setText(0, new_node.title)
            new_item.setText(1, str(new_node.id))
            new_item.setData(0, Qt.ItemDataRole.UserRole, new_node)

            selected_item.addChild(new_item)  # Add item to the tree view
            selected_item.setExpanded(True)

    def edit_child_node(self):
        selected_items = self.tree_widget.selectedItems()
        if not selected_items:
            return

        selected_item = selected_items[0]
        node = selected_item.data(0, Qt.ItemDataRole.UserRole)

        dialog = NodeEditDialog(node.title, parent=self)
        if dialog.exec():
            node_data = dialog.get_data()

            # Düğümü güncelle
            node.title = node_data["title"]

            # Görünümü güncelle
            selected_item.setText(0, node_data["title"])

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
            "Bu öğeyi ve tüm alt öğelerini silmek istediğinizden emin misiniz?",
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

    def load_yaml(self):
        root_item = QTreeWidgetItem(self.tree_widget)
        root_item.setText(0, self.root.title)
        root_item.setText(1, str(self.root.id))
        root_item.setData(0, Qt.ItemDataRole.UserRole, self.root)

        if self.root.children:
            self.process_children(root_item, self.root.children)

    def process_children(self, parent_item, children):
        self.menu_count += len(children)
        for child in children:
            child_item = QTreeWidgetItem(parent_item)
            child_item.setText(0, child.title)
            child_item.setText(1, str(child.id))
            child_item.setData(0, Qt.ItemDataRole.UserRole, child)

            if child.children:
                self.process_children(child_item, child.children)

    def save_yaml(self):
        # Kök düğümü al
        yml_data = [self.root.to_dict()]
        print(yml_data)
        # YAML dosyasını kaydet
        with open(self.yaml_path, "w", encoding="utf-8") as f:
            yaml.dump(yml_data, f, allow_unicode=True)