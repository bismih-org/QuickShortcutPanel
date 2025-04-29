from typing import Tuple
from src.common.Logging import Log
from src.static.file_paths import Paths as path


class Configs:
    window_size: int = 600
    window_size_half: int = window_size // 2
    center: Tuple[int, int] = (window_size_half, window_size_half)
    piece_angle: int = 50
    piece_radius: int = 30
    piece_k: int = 2

    menu_yaml_path: str = path.menu_yaml_path
    menu_json_path: str = path.menu_json_path

    logger = Log()
