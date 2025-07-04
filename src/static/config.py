from typing import Tuple
from src.common.Logging import Log
from src.static.file_paths import Paths as path
from PyQt6.QtGui import QColor


class Configs:
    window_size: int = 600
    window_size_half: int = window_size // 2
    center: Tuple[int, int] = (window_size_half, window_size_half)
    piece_radius: int = 30
    piece_k: int = 2

    logger = Log()
