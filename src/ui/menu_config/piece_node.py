from typing import List
import yaml

from src.ui.panel.piece import Piece


class PieceNode:
    def __init__(self, title: str, id_: int, type_:str, description: str):
        self.title = title
        self.id = id_
        self.type = type_
        self.description = description
        self.children: list[PieceNode] = []
        self.layer_index = 0
        self.piece_index = 0
        self.piece_data: Piece

    def add_child(self, child: "PieceNode"):
        self.children.append(child)

    def __str__(self):
        return self._str_helper()

    def _str_helper(self, level=0):
        indent = "  " * level
        result = f"{indent}- {self.layer_index} {self.piece_index} -{self.title} (ID: {self.id})\n"
        for child in self.children:
            result += child._str_helper(level + 1)
        return result

    def to_dict(self):
        result = {
            "title": self.title,
            "id": self.id,
            "type": self.type,
            "description": self.description,
        }
        if self.children:
            result["children"] = [child.to_dict() for child in self.children]

        return result

    @classmethod
    def update_layer_piece_index(cls, root_node: "PieceNode"):
        def update(node: "PieceNode", layer_index: int, piece_index: int):
            node.layer_index = layer_index
            node.piece_index = piece_index
            node.piece_data = Piece(layer_index, piece_index)

            for i, child in enumerate(node.children):
                update(child, layer_index + 1, i)

        update(root_node, 0, 0)


def build_tree(data):
    # Kök düğümü oluştur
    root = PieceNode(data["title"], data["id"], data["type"], data["description"])

    # Çocukları varsa işle
    if "children" in data:
        for child_data in data["children"]:
            child_node = build_tree(child_data)
            root.add_child(child_node)

    return root
