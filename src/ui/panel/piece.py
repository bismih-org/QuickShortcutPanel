from typing import List, Tuple
from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QPolygon

from src.static.config import Configs as cfg
import math


class Piece:
    def __init__(
        self, layer_index, piece_index, text: str = "", piece_angle: int = 90
    ):
        self.coordinate_list: List[QPoint] = []
        self.layer_index: int = layer_index
        self.piece_index: int = piece_index
        self.angle_spacing = 1
        self.text = text
        self.text_angle = 0
        self.piece_angle = piece_angle

        self._set_coordinate()
        poly = self.get_poligon()
        self.center_pos = poly.boundingRect().center()

    def _get_coordinate(self, angle_offset: int, is_inner) -> Tuple[int, int]:
        x, y = cfg.center
        radius_factor = self.layer_index if is_inner else self.layer_index + 1
        radius = cfg.piece_k * (radius_factor * cfg.piece_radius)

        # Parça açısı ve yay üzerindeki konumu hesapla
        base_angle = self.piece_index * self.piece_angle
        angle = base_angle + angle_offset

        radian = math.radians(angle)
        return (
            int(x + (math.cos(radian) * radius)),
            int(y + (math.sin(radian) * radius)),
        )

    def _set_coordinate(self):
        # İç yay (başlangıç açısından bitiş açısına)
        start_angle = self.piece_index * self.piece_angle
        end_angle = (self.piece_index + 1) * self.piece_angle

        self.text_angle = int((start_angle + end_angle) / 2)

        # İç yay noktaları
        for angle in range(start_angle, end_angle + 1):
            coord = self._get_coordinate(angle - start_angle, True)
            self.coordinate_list.append(QPoint(coord[0], coord[1]))

        # Dış yay noktaları (ters sırada)
        for angle in range(end_angle, start_angle - 1, -1):
            coord = self._get_coordinate(angle - start_angle, False)
            self.coordinate_list.append(QPoint(coord[0], coord[1]))

    def get_poligon(self) -> QPolygon:
        return QPolygon(self.coordinate_list)

    def get_angle(self) -> int:
        return self.text_angle

    def get_center_pos(self) -> QPoint:
        return self.center_pos

    def get_radius(self) -> int:
        return int(self.get_poligon().boundingRect().width() / 2)
