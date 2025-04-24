from PyQt6.QtWidgets import QWidget, QToolTip
from PyQt6.QtGui import QPainter, QColor, QKeyEvent, QPen
from PyQt6.QtCore import Qt, QEvent

from src.ui.panel.piece import Piece
from src.static.config import Configs as cfg


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

        self.active_pieces: list[Piece] = []

        self.test_piece = Piece(layer_index=1, piece_index=1, text="test")
        self.test_piece2 = Piece(layer_index=1, piece_index=2, text="test2")
        self.test_piece3 = Piece(layer_index=2, piece_index=2, text="test3")
        self.test_piece4 = Piece(layer_index=3, piece_index=2, text="test4")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Siyah kenar kalemi
        pen = QPen(QColor("black"))
        pen.setWidth(3)  # Kenar kalınlığı
        painter.setPen(pen)

        # İlk poligon (kırmızı iç, siyah kenar)
        painter.setBrush(QColor("red"))
        painter.drawPolygon(self.test_piece.get_poligon())

        # İkinci poligon (yeşil iç, siyah kenar)
        painter.setBrush(QColor("green"))
        painter.drawPolygon(self.test_piece2.get_poligon())

        # Üçüncü poligon (mavi iç, siyah kenar)
        painter.setBrush(QColor("blue"))
        painter.drawPolygon(self.test_piece3.get_poligon())

        # Dördüncü poligon (sarı iç, siyah kenar)
        painter.setBrush(QColor("yellow"))
        painter.drawPolygon(self.test_piece4.get_poligon())

    def mouseMoveEvent(self, event):
        """Fare hareketlerini takip et ve tooltip göster"""
        pos = event.pos()

        # Önceki tooltip'i gizle
        if self.current_tooltip:
            QToolTip.hideText()
            self.current_tooltip = None

        if self.test_piece.get_poligon().containsPoint(pos, Qt.FillRule.OddEvenFill):
            QToolTip.showText(self.mapToGlobal(pos), "Üçgen", self)
            self.current_tooltip = "triangle"
        elif self.test_piece2.get_poligon().containsPoint(pos, Qt.FillRule.OddEvenFill):
            QToolTip.showText(self.mapToGlobal(pos), "Altıgen", self)
            self.current_tooltip = "hexagon"

    def mousePressEvent(self, event):
        """Tıklama olaylarını yakala"""
        pos = event.pos()

        if self.test_piece.get_poligon().containsPoint(pos, Qt.FillRule.OddEvenFill):
            print("1 tıklandı!")
        elif self.test_piece2.get_poligon().containsPoint(pos, Qt.FillRule.OddEvenFill):
            print("2 tıklandı!")

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.close()

    def event(self, event: QEvent):
        if event.type() == QEvent.Type.WindowDeactivate:
            self.close()
        return super().event(event)
