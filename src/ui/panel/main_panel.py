from typing import List
from PyQt6.QtWidgets import QWidget, QToolTip
from PyQt6.QtGui import QPainter, QColor, QKeyEvent, QPen
from PyQt6.QtCore import Qt, QEvent
import yaml

from src.ui.panel.piece import Piece
from src.static.config import Configs as cfg
from src.ui.menu_config.piece_node import PieceNode, build_tree


class MainPanel(QWidget):
    def __init__(self, win_pos_x: int, win_pos_y: int):
        super().__init__()

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(int(win_pos_x), int(win_pos_y), 600, 600)

        # Activate mouse tracking for hover
        self.setMouseTracking(True)

        # set tooltip font
        QToolTip.setFont(self.font())

        # set first tooltip position
        self.current_tooltip = None

        self.init_variables()

        self.active_pieces_nodes: List[PieceNode] = [self.root_node]
        self.active_node = self.root_node

    def init_variables(self):
        with open(cfg.menu_yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        self.root_node = build_tree(data[0])
        PieceNode.update_layer_piece_index(self.root_node)
        print(self.root_node)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Siyah kenar kalemi
        pen = QPen(QColor("black"))
        pen.setWidth(3)  # Kenar kalınlığı
        painter.setPen(pen)

        for pn in self.active_pieces_nodes:
            # İlk poligon (kırmızı iç, siyah kenar)
            for p in pn.children:
                painter.setBrush(QColor("red"))
                painter.drawPolygon(p.piece_data.get_poligon())
                # --- Add text ---
                # Save painter state
                painter.save()

                # Set text properties
                painter.setPen(QColor("white"))  # Text color
                # painter.setFont(QFont("Arial", 10)) # Optional: Set font

                # Translate and rotate painter context
                painter.translate(p.piece_data.get_center_pos())
                painter.rotate(p.piece_data.get_angle())

                # Draw text centered at the new origin (0,0)
                font_metrics = painter.fontMetrics()
                text_rect = font_metrics.boundingRect(p.title)
                # Adjust x, y to center the text
                text_x = -text_rect.width() / 2
                # Adjust y for vertical centering (approximation)
                text_y = font_metrics.ascent() / 2 - font_metrics.descent() / 2

                painter.drawText(int(text_x), int(text_y), p.title)

                # Restore painter state
                painter.restore()

                # Reset pen for the border (important if text color was different)
                # painter.setPen(pen)
                print("çalışıyor")

    def mouseMoveEvent(self, event):
        """Fare hareketlerini takip et ve tooltip göster"""
        pos = event.pos()

        # Önceki tooltip'i gizle
        if self.current_tooltip:
            QToolTip.hideText()
            self.current_tooltip = None

        for pn in self.active_pieces_nodes:
            # İlk poligon (kırmızı iç, siyah kenar)
            for p in pn.children:
                if p.piece_data.get_poligon().containsPoint(
                    pos, Qt.FillRule.OddEvenFill
                ):
                    QToolTip.showText(self.mapToGlobal(pos), p.title, self)
                    self.current_tooltip = p.title
                    self.active_node = p
                    self.active_node_list_control(p)
                    break

    def active_node_list_control(self, node: PieceNode):
        """Aktif node listesini kontrol et ve ekle"""
        print(f"Active node: {node.title}")
        for n in self.active_pieces_nodes:
            if n.layer_index >= self.active_node.layer_index:
                self.active_pieces_nodes.remove(n)
                break
        if node not in self.active_pieces_nodes:
            self.active_pieces_nodes.append(node)
        self.update()

    def mousePressEvent(self, event):
        """Tıklama olaylarını yakala"""
        pos = event.pos()

        for pn in self.active_pieces_nodes:
            # İlk poligon (kırmızı iç, siyah kenar)
            for p in pn.children:
                if p.piece_data.get_poligon().containsPoint(
                    pos, Qt.FillRule.OddEvenFill
                ):
                    print(f"Clicked on {p.title}")

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.close()

    def event(self, event: QEvent):
        if event.type() == QEvent.Type.WindowDeactivate:
            self.close()
        return super().event(event)
