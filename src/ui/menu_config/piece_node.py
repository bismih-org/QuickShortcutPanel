from typing import List
import yaml


class PieceNode:
    def __init__(self, title: str, id_: int):
        self.title = title
        self.id = id_
        self.children: List["PieceNode"] = []

    def add_child(self, child: "PieceNode"):
        self.children.append(child)

    def __str__(self):
        return self._str_helper()

    def _str_helper(self, level=0):
        indent = "  " * level
        result = f"{indent}- {level} -{self.title} (ID: {self.id})\n"
        for child in self.children:
            result += child._str_helper(level + 1)
        return result

    def to_dict(self):
        result = {
            "title": self.title,
            "id": self.id,
        }
        if self.children:
            result["children"] = [child.to_dict() for child in self.children]

        return result


def build_tree(data):
    # Kök düğümü oluştur
    root = PieceNode(data["title"], data["id"])

    # Çocukları varsa işle
    if "children" in data:
        for child_data in data["children"]:
            child_node = build_tree(child_data)
            root.add_child(child_node)

    return root


if __name__ == "__main__":
    yaml_str = """
    - title: root
    id: 0
    children:
        - title: menu 1
        id: 1
        - title: menu 2
        id: 2
        children:
            - title: menu 3
            id: 3
        - title: menu 5
        id: 5
        children:
            - title: menu 6
            id: 6
        - title: menu 4
        id: 4
    """
    data = yaml.safe_load(yaml_str)
    root = build_tree(data[0])

    for r in root.children:
        print(r)
        print("-" * 20)

    print(root.children)
