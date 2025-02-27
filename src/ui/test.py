from PyQt6.QtWidgets import QWidget, QToolTip
from PyQt6.QtGui import QPainter, QPolygon, QColor, QKeyEvent
from PyQt6.QtCore import QPoint, Qt, QEvent


class QuickShortcutPanel(QWidget):
    def __init__(self, win_pos_x: int, win_pos_y: int):
        super().__init__()
        print("location:" + str(win_pos_x) + "  " + str(win_pos_y))
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(int(win_pos_x), int(win_pos_y), 300, 200)

        # Activate mouse tracking for hover
        self.setMouseTracking(True)

        # Tooltip font boyutunu ayarla
        QToolTip.setFont(self.font())

        # Poligonları sınıf değişkenleri olarak tanımla
        self.triangle = QPolygon(
            [
                QPoint(100, 20),
                QPoint(50, 120),
                QPoint(150, 120),
            ]
        )

        self.hexagon = QPolygon(
            [
                QPoint(220, 50),
                QPoint(270, 80),
                QPoint(270, 130),
                QPoint(220, 160),
                QPoint(170, 130),
                QPoint(170, 80),
            ]
        )

        # İlk tooltip pozisyonunu ayarla
        self.current_tooltip = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Üçgen
        painter.setBrush(QColor("red"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPolygon(self.triangle)

        # Altıgen
        painter.setBrush(QColor("green"))
        painter.drawPolygon(self.hexagon)

    def mouseMoveEvent(self, event):
        """Fare hareketlerini takip et ve tooltip göster"""
        pos = event.pos()

        # Önceki tooltip'i gizle
        if self.current_tooltip:
            QToolTip.hideText()
            self.current_tooltip = None

        if self.triangle.containsPoint(pos, Qt.FillRule.OddEvenFill):
            QToolTip.showText(self.mapToGlobal(pos), "Üçgen", self)
            self.current_tooltip = "triangle"
        elif self.hexagon.containsPoint(pos, Qt.FillRule.OddEvenFill):
            QToolTip.showText(self.mapToGlobal(pos), "Altıgen", self)
            self.current_tooltip = "hexagon"

    def leaveEvent(self, event):
        """Fare pencereden çıkınca tooltip'i gizle"""
        if self.current_tooltip:
            QToolTip.hideText()
            self.current_tooltip = None

    def mousePressEvent(self, event):
        """Tıklama olaylarını yakala"""
        pos = event.pos()

        if self.triangle.containsPoint(pos, Qt.FillRule.OddEvenFill):
            print("Üçgene tıklandı!")
        elif self.hexagon.containsPoint(pos, Qt.FillRule.OddEvenFill):
            print("Altıgene tıklandı!")

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.close()

    def event(self, event: QEvent):
        if event.type() == QEvent.Type.WindowDeactivate:
            self.close()
        return super().event(event)
