from typing import List, Tuple
from PyQt6.QtCore import QPoint

from static.config import Configs as cfg
import math


class Piece:
    def __init__(self, layer_index, piece_index, center: Tuple[int, int] = (0, 0)):
        self.coordiante_list: List[QPoint] = []
        self.layer_index: int = layer_index
        self.piece_index: int = piece_index
        self.k: int = 2
        self.angle_spacing = 1

    def _get_cooirdante(self, step: int, is_innener) -> Tuple[int, int]:
        """
        step -> yay çizilirken her bir adım \n
        is_inner -> parçanın iç mi yoksa dış yayı mı çizilecek\n
        merkez = (ş, e)\n
        başlangıç noktası = (ş + (cos((p-1)\*a) / k\*r), e + (sin((p-1)\*a) / k\*r))
        """
        x, y = cfg.center
        inner = 1 if is_innener else 0
        radian = math.radians((self.piece_index - inner) * cfg.piece_angle + step)
        radius = self.k * ((self.piece_index - inner) * cfg.piece_radius)
        return (x + (math.cos(radian) / radius), y + (math.sin(radian) / radius))

    def _set_coordinate(self):
        for s in range(cfg.piece_angle):
            self.coordiante_list.append(QPoint(self.get_cooirdante(s, True)))
        
        for s in range(cfg.piece_angle):
            self.coordiante_list.append(QPoint(self.get_cooirdante(s, False)))


