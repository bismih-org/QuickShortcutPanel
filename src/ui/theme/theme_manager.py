from PyQt6.QtWidgets import QApplication
from src.static.config import Configs as cfg
import os
from PyQt6.QtCore import QDir


class ThemeManager:
    def __init__(self):
        self.is_dark_mode = True
        try:
            self.icons_dir = self.ensure_icons_exists()  # İkon dosyalarını oluştur
            QDir.addSearchPath(
                "icons", self.icons_dir
            )  # İkon dizinini QT arama yoluna ekle
        except Exception as e:
            print(f"İkon dizini oluşturulurken hata oluştu: {e}")
        self._define_themes()

    def _define_themes(self):
        # Koyu tema - Ana vurgu rengi (194, 50, 50)
        self.dark_theme = {
            "MAIN_BG": "#12121a",
            "SECONDARY_BG": "#1a1a24",
            "TEXT": "#f0f0f5",
            "BORDER": "#303038",
            "ACCENT": "#d35400",  # Ana vurgu rengi (211, 84, 0)
            "ACCENT_HOVER": "#e67e22",  # Daha yumuşak turuncu
            "ACCENT_PRESSED": "#c0392b",  # Daha koyu turuncu-kırmızı
            "DISABLED_BG": "#2a2a34",
            "DISABLED_TEXT": "#707080",
            "START_BUTTON": "#2e9e6a",  # Yeşil
            "START_BUTTON_HOVER": "#35b378",
            "STOP_BUTTON": "#d35400",  # Turuncu (ana renk)
            "STOP_BUTTON_HOVER": "#e67e22",
            "EXIT_BUTTON": "#505058",
            "SAVE_BUTTON": "#3c82be",  # Mavi
            "ALTERNATE_ROW": "#1e1e28",
            "SELECTION_BG": "#403046",  # Hafif mor ton
        }

        # Aydınlık tema - Ana vurgu rengi daha yumuşak (211, 84, 0)
        self.light_theme = {
            "MAIN_BG": "#f8f8fa",
            "SECONDARY_BG": "#ffffff",
            "TEXT": "#2a2a32",
            "BORDER": "#dadae0",
            "ACCENT": "#d35400",  # Ana vurgu rengi (211, 84, 0)
            "ACCENT_HOVER": "#e67e22",  # Daha yumuşak turuncu
            "ACCENT_PRESSED": "#c0392b",  # Daha koyu turuncu-kırmızı
            "DISABLED_BG": "#e8e8ec",
            "DISABLED_TEXT": "#a0a0a8",
            "START_BUTTON": "#2eb87a",  # Yeşil
            "START_BUTTON_HOVER": "#35d090",
            "STOP_BUTTON": "#d35400",  # Turuncu (ana renk)
            "STOP_BUTTON_HOVER": "#e67e22",
            "EXIT_BUTTON": "#858590",
            "SAVE_BUTTON": "#3c92de",  # Mavi
            "ALTERNATE_ROW": "#f0f4fa",
            "SELECTION_BG": "#f0e6ff",  # Açık mor ton
        }

        self.current_theme = self.dark_theme if self.is_dark_mode else self.light_theme

    def ensure_icons_exists(self):
        """İkon dosyalarının varlığını kontrol eder, yoksa oluşturur"""
        icons_dir = os.path.join(os.path.dirname(__file__), "icons")
        if not os.path.exists(icons_dir):
            os.makedirs(icons_dir)

        # Checkbox tik işareti
        check_white_path = os.path.join(icons_dir, "check-white.png")
        if not os.path.exists(check_white_path):
            from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor

            pixmap = QPixmap(18, 18)
            pixmap.fill(QColor(0, 0, 0, 0))  # Şeffaf arkaplan

            painter = QPainter(pixmap)
            painter.setPen(QPen(QColor(255, 255, 255), 2))  # Beyaz renk, 2px kalınlık
            painter.drawLine(4, 9, 8, 13)  # Tik işaretinin ilk çizgisi
            painter.drawLine(8, 13, 14, 7)  # Tik işaretinin ikinci çizgisi
            painter.end()

            pixmap.save(check_white_path)

        # Açık dal ikonu
        branch_open_path = os.path.join(icons_dir, "branch-open.png")
        if not os.path.exists(branch_open_path):
            from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor

            pixmap = QPixmap(16, 16)
            pixmap.fill(QColor(0, 0, 0, 0))  # Şeffaf arkaplan

            painter = QPainter(pixmap)
            painter.setPen(QPen(QColor(180, 180, 180), 2))  # Gri renk, 2px kalınlık
            painter.drawLine(4, 8, 12, 8)  # Yatay çizgi
            painter.drawLine(8, 4, 8, 12)  # Dikey çizgi
            painter.end()

            pixmap.save(branch_open_path)

        # Kapalı dal ikonu
        branch_closed_path = os.path.join(icons_dir, "branch-closed.png")
        if not os.path.exists(branch_closed_path):
            from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor

            pixmap = QPixmap(16, 16)
            pixmap.fill(QColor(0, 0, 0, 0))  # Şeffaf arkaplan

            painter = QPainter(pixmap)
            painter.setPen(QPen(QColor(180, 180, 180), 2))  # Gri renk, 2px kalınlık
            painter.drawLine(4, 8, 12, 8)  # Yatay çizgi
            painter.end()

            pixmap.save(branch_closed_path)

        # İkon dizini yolunu QT kaynağı olarak ekleyebilmek için geri döndür
        return icons_dir

    def _generate_stylesheet(self):
        """QSS şablonunu oluşturur ve tema renkleriyle doldurur."""
        with open(
            os.path.join(os.path.dirname(__file__), "../../../data/theme.qss"), "r"
        ) as f:
            qss_template = f.read()

        # Tema değişkenlerini değiştir
        for key, value in self.current_theme.items():
            qss_template = qss_template.replace(f"${{{key}}}", value)

        return qss_template

    def apply_theme(self, dark_mode=True):
        """Temayı uygular."""
        self.is_dark_mode = dark_mode
        self.current_theme = self.dark_theme if dark_mode else self.light_theme

        # Uygulama örneğine stil sayfasını uygula
        app = QApplication.instance()
        if app:
            app.setStyleSheet(self._generate_stylesheet())

            # Düğmelerin ID'lerini ayarlama
            # Bu kısmı ConfigPanel'deki init içinde yapmak gerekecek

        return self.is_dark_mode

    def toggle_theme(self):
        """Tema modunu değiştirir ve yeni tema modunu döndürür."""
        return self.apply_theme(not self.is_dark_mode)
