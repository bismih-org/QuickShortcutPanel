import json
import math
import time
from typing import List
from PyQt6.QtWidgets import QWidget, QToolTip
from PyQt6.QtGui import QPainter, QKeyEvent, QPen, QBrush
from PyQt6.QtCore import Qt, QEvent

from src.static.config import Configs as cfg
from src.ui.menu_config.piece_node import PieceNode, build_tree
from src.process.runner import run_action


class MainPanel(QWidget):
    def __init__(self, win_pos_x: int, win_pos_y: int):
        super().__init__()

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(
            int(win_pos_x - cfg.window_size_half),
            int(win_pos_y - cfg.window_size_half),
            cfg.window_size,
            cfg.window_size,
        )

        # Activate mouse tracking for hover
        self.setMouseTracking(True)

        # set tooltip font
        QToolTip.setFont(self.font())

        # set first tooltip position
        self.current_tooltip = None
        self.hover_node = None  # Fare üzerinde olan parça

        self.init_variables()

        self.active_pieces_nodes: List[PieceNode] = [self.root_node]
        self.active_node = self.root_node

    def init_variables(self):
        with open(cfg.menu_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.root_node = build_tree(data[0])
        PieceNode.update_layer_piece_index(self.root_node)
        print(self.root_node)

        self.pending_node = None  # Bekleme süresindeki düğüm
        self.hover_start_time = 0  # Hover'a başlama zamanı
        self.hover_delay = 0.07  # Saniye cinsinden bekleme süresi

    def paintEvent(self, a0):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        pen = QPen(cfg.THEME_COLORS["border"])
        pen.setWidth(2)  # Kenar kalınlığı
        painter.setPen(pen)

        for pn in self.active_pieces_nodes:
            for p in pn.children:
                # Dolgu rengini belirle (hover, active veya normal)
                if self.hover_node == p:
                    painter.setBrush(QBrush(cfg.THEME_COLORS["hover"]))
                elif p == self.active_node and p.layer_index > 0:
                    painter.setBrush(QBrush(cfg.THEME_COLORS["active"]))
                else:
                    painter.setBrush(QBrush(cfg.THEME_COLORS["normal"]))

                painter.drawPolygon(p.piece_data.get_poligon())

                # --- Add text ---
                painter.save()

                # Set text properties
                painter.setPen(cfg.THEME_COLORS["text"])  # Text color

                # Get piece position and angle information
                center_pos = p.piece_data.get_center_pos()
                angle = p.piece_data.get_angle()

                # Calculate text position adjustment based on layer index
                radial_offset = 0
                if p.layer_index > 1:
                    # Adjust radial offset based on layer index
                    radial_offset = (p.layer_index - 1) * 20

                # Calculate position along radial line
                radian = math.radians(angle)
                offset_x = math.cos(radian) * radial_offset
                offset_y = math.sin(radian) * radial_offset

                # Translate to the center of the piece
                painter.translate(center_pos.x() + offset_x, center_pos.y() + offset_y)

                # Adjust angle for text readability
                adjusted_angle = angle
                if angle > 90 and angle < 270:
                    adjusted_angle += 180

                painter.rotate(adjusted_angle)

                # Draw text centered at the new origin (0,0)
                font_metrics = painter.fontMetrics()

                words = p.title.split()
                title = "\n".join(words)

                text_rect = font_metrics.boundingRect(
                    0, 0, 1000, 1000, Qt.TextFlag.TextWordWrap, title
                )
                text_x = -text_rect.width() / 2
                text_y = -text_rect.height() / 2  # Metni dikey olarak da ortala

                painter.drawText(
                    int(text_x),
                    int(text_y),
                    text_rect.width(),
                    text_rect.height(),
                    Qt.TextFlag.TextJustificationForced,
                    title,
                )

                # Restore painter state
                painter.restore()

                # Reset pen for the border
                painter.setPen(pen)

    def mouseMoveEvent(self, a0):
        """Fare hareketlerini takip et ve tooltip göster"""
        pos = a0.pos()
        old_hover = self.hover_node
        self.hover_node = None

        # Fare pozisyonundaki parçayı bul
        found_node = None
        for pn in self.active_pieces_nodes:
            for p in pn.children:
                if p.piece_data.get_poligon().containsPoint(
                    pos, Qt.FillRule.OddEvenFill
                ):
                    found_node = p
                    # QToolTip.showText(self.mapToGlobal(pos), p.title, self)
                    # self.current_tooltip = p.title
                    self.hover_node = p
                    break
            if found_node:
                break

        # Hover değişikliği varsa
        if old_hover != self.hover_node:
            # Hover'ı görsel olarak güncelleyin
            self.update()

            if self.hover_node:
                # Yeni bir hover başladıysa
                if self.hover_node != self.pending_node:
                    self.pending_node = self.hover_node
                    self.hover_start_time = time.time()
            else:
                # Hover sona erdiyse
                self.pending_node = None

        # Bekleyen bir düğüm varsa ve yeterli süre geçtiyse aktif yap
        current_time = time.time()
        if (
            self.pending_node
            and current_time - self.hover_start_time >= self.hover_delay
            and self.pending_node == self.hover_node
        ):  # Hala aynı düğüm üzerindeyiz

            self.active_node = self.pending_node
            self.active_node_list_control(self.pending_node)
            self.pending_node = None  # Bekleyen düğümü temizle

    def active_node_list_control(self, node: PieceNode):
        """Aktif node listesini kontrol et ve ekle"""
        print(f"Active node: {node.title}")

        # Mevcut katmandan daha yüksek veya eşit katmandaki tüm düğümleri kaldır
        self.active_pieces_nodes = [
            n for n in self.active_pieces_nodes if n.layer_index < node.layer_index
        ]

        # Yeni düğümü ekle
        if node not in self.active_pieces_nodes:
            self.active_pieces_nodes.append(node)

        self.update()

    def mousePressEvent(self, a0):
        """Tıklama olaylarını yakala"""
        pos = a0.pos()

        for pn in self.active_pieces_nodes:
            # İlk poligon (kırmızı iç, siyah kenar)
            for p in pn.children:
                if p.piece_data.get_poligon().containsPoint(
                    pos, Qt.FillRule.OddEvenFill
                ):
                    print(f"Clicked on {p.title}")
                    run_action(p.data)
        self.close()

    def keyPressEvent(self, a0: QKeyEvent):
        if a0.key() == Qt.Key.Key_Escape:
            self.close()

    def event(self, a0: QEvent):
        if a0.type() == QEvent.Type.WindowDeactivate:
            self.close()
        return super().event(a0)
