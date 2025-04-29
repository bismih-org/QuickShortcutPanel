from typing import Tuple
from src.common.Logging import Log
from src.static.file_paths import Paths as path


class Configs:
    center: Tuple[int, int] = (300, 300)
    piece_angle: int = 50
    piece_radius: int = 30
    piece_k: int = 2

    menu_yaml_path: str = path.menu_yaml_path
    menu_json_path: str = path.menu_json_path

    logger = Log()
