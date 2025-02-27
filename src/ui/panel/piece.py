from typing import List, Tuple
from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QPolygon

from src.static.config import Configs as cfg
import math


class Piece:
    def __init__(self, layer_index, piece_index):
        self.coordinate_list: List[QPoint] = []
        self.layer_index: int = layer_index
        self.piece_index: int = piece_index
        self.k: int = 2
        self.angle_spacing = 1

        self._set_coordinate()

    def _get_coordinate(self, step: int, is_inner) -> Tuple[int, int]:

        x, y = cfg.center
        inner = 1 if is_inner else 0
        radian = math.radians((self.piece_index - inner) * cfg.piece_angle + step)
        radius = self.k * ((self.piece_index - inner) * cfg.piece_radius)
        return (
            int(x + (math.cos(radian) * radius)),
            int(y + (math.sin(radian) * radius)),
        )

    def _set_coordinate(self):
        for s in range(cfg.piece_angle):
            coord = self._get_coordinate(s, True)
            self.coordinate_list.append(QPoint(coord[0], coord[1]))

        for s in range(cfg.piece_angle):
            coord = self._get_coordinate(s, False)
            self.coordinate_list.append(QPoint(coord[0], coord[1]))

    def get_poligon(self) -> QPolygon:
        return QPolygon(self.coordinate_list)
