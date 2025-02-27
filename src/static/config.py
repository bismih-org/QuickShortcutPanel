from typing import Tuple
from common.Logging import Log
from static.file_paths import Paths as path


class Configs:
    center: Tuple[int, int] = (10, 10)
    piece_angle: int = 20
    piece_radius: int = 30

    logger = Log()
