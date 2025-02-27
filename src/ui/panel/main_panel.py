from PyQt6.QtWidgets import QWidget, QToolTip
from PyQt6.QtGui import QPainter, QPolygon, QColor, QKeyEvent
from PyQt6.QtCore import QPoint, Qt, QEvent

from src.ui.panel.piece import Piece


class MainPanel(QWidget):
    def  __init__(self, win_pos_x: int, win_pos_y: int):
        super().__init__()
        
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(int(win_pos_x), int(win_pos_y), 300, 200)

        # Activate mouse tracking for hover
        self.setMouseTracking(True)

        # set tooltip font
        QToolTip.setFont(self.font())

        # set first tooltip position
        self.current_tooltip = None

        self.test_piece = Piece(layer_index=1,piece_index=1)
        self.test_piece2 = Piece(layer_index=2,piece_index=2)



    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Üçgen
        painter.setBrush(QColor("red"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPolygon(self.test_piece.get_poligon())

        painter.setBrush(QColor("green"))
        painter.drawPolygon(self.test_piece2.get_poligon())



    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.close()

    def event(self, event: QEvent):
        if event.type() == QEvent.Type.WindowDeactivate:
            self.close()
        return super().event(event)