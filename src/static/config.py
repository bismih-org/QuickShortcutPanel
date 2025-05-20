from typing import Tuple
from src.common.Logging import Log
from src.static.file_paths import Paths as path
from PyQt6.QtGui import QColor


class Configs:
    window_size: int = 600
    window_size_half: int = window_size // 2
    center: Tuple[int, int] = (window_size_half, window_size_half)
    piece_radius: int = 30
    piece_k: int = 2

    menu_yaml_path: str = path.menu_yaml_path
    menu_json_path: str = path.menu_json_path

    logger = Log()


    THEME_COLORS = {
        # Ana renk paleti
        "background": QColor(18, 18, 24),       # Koyu siyahımsı arka plan
        "border": QColor(48, 48, 56),           # Yumuşak kenar çizgisi
        "text": QColor(240, 240, 245),          # Hafif gri metin
        "normal": QColor(30, 30, 38),           # Koyu gri normal parçalar
        
        # Vurgu renkleri - Ana kırmızı renk etrafında
        "accent": QColor(194, 50, 50),          # Ana vurgu/aksan rengi (Kırmızı)
        "hover": QColor(210, 65, 65),           # Hover durumu için daha açık kırmızı
        "active": QColor(180, 40, 40),          # Active durumu için daha koyu kırmızı
        
        # Tamamlayıcı renkler
        "success": QColor(46, 160, 110),        # Yeşil (başarı durumu) 
        "warning": QColor(240, 140, 40),        # Turuncu (uyarı durumu)
        "info": QColor(60, 130, 190),           # Mavi (bilgi durumu)
        
        # Eski renkler için geriye dönük uyumluluk
        "unactive": QColor(70, 70, 80),         # Pasif durum
        "same_layer": QColor(110, 80, 190),     # Aynı katman için mor tonları
    }
