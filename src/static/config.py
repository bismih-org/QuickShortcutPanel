from typing import Tuple
from src.common.Logging import Log
from src.static.file_paths import Paths as path


class Configs:
    center: Tuple[int, int] = (10, 10)
    piece_angle: int = 20
    piece_radius: int = 30

    logger = Log()
