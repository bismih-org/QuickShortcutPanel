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

    menu_yaml_path: str = path.menu_yaml_path
    menu_json_path: str = path.menu_json_path

    logger = Log()


    THEME_COLORS = {
        "background": QColor(10, 10, 10, 230),  # Yarı saydam siyahımsı arka plan
        "border": QColor(60, 60, 60),  # Daha yumuşak kenar çizgisi
        "text": QColor(240, 240, 240),  # Hafif gri text, gözü yormaması için
        "normal": QColor(45, 45, 45),  # Koyu gri normal parçalar
        "hover": QColor(240, 160, 30),  # Canlı turuncu/amber hover efekti
        "active": QColor(190, 120, 30),  # Daha koyu turuncu ton aktif parçalar için
    }
