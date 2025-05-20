from PyQt6.QtWidgets import QApplication
from src.static.config import Configs as cfg

class ThemeManager:
    def __init__(self):
        self.is_dark_mode = True
        self._define_themes()
        
    def _define_themes(self):
        # Koyu tema - Ana vurgu rengi (194, 50, 50)
        self.dark_theme = {
            "MAIN_BG": "#12121a",
            "SECONDARY_BG": "#1a1a24",
            "TEXT": "#f0f0f5",
            "BORDER": "#303038",
            "ACCENT": "#c23232",         # Ana vurgu rengi (194, 50, 50)
            "ACCENT_HOVER": "#d24141",
            "ACCENT_PRESSED": "#b42828", 
            "DISABLED_BG": "#2a2a34",
            "DISABLED_TEXT": "#707080",
            "START_BUTTON": "#2e9e6a",   # Yeşil
            "START_BUTTON_HOVER": "#35b378",
            "STOP_BUTTON": "#c23232",    # Kırmızı (ana renk)
            "STOP_BUTTON_HOVER": "#d24141",
            "EXIT_BUTTON": "#505058",
            "SAVE_BUTTON": "#3c82be",    # Mavi
            "ALTERNATE_ROW": "#1e1e28",
            "SELECTION_BG": "#403046",   # Hafif mor ton
        }
        
        # Aydınlık tema - Ana vurgu rengi daha yumuşak (194, 50, 50)
        self.light_theme = {
            "MAIN_BG": "#f8f8fa",
            "SECONDARY_BG": "#ffffff",
            "TEXT": "#2a2a32",
            "BORDER": "#dadae0",
            "ACCENT": "#c23232",         # Ana vurgu rengi (194, 50, 50)
            "ACCENT_HOVER": "#d24141",
            "ACCENT_PRESSED": "#b42828",
            "DISABLED_BG": "#e8e8ec",
            "DISABLED_TEXT": "#a0a0a8",
            "START_BUTTON": "#2eb87a",   # Yeşil
            "START_BUTTON_HOVER": "#35d090",
            "STOP_BUTTON": "#c23232",    # Kırmızı (ana renk)
            "STOP_BUTTON_HOVER": "#d24141",
            "EXIT_BUTTON": "#858590",
            "SAVE_BUTTON": "#3c92de",    # Mavi
            "ALTERNATE_ROW": "#f0f4fa",
            "SELECTION_BG": "#f0e6ff",   # Açık mor ton
        }
        
        self.current_theme = self.dark_theme if self.is_dark_mode else self.light_theme
        
    def _generate_stylesheet(self):
        """QSS şablonunu oluşturur ve tema renkleriyle doldurur."""
        qss_template = """
            /* Ana Widget */
            QWidget {
                background: ${MAIN_BG};
                color: ${TEXT};
                font-family: 'Segoe UI', 'Arial', sans-serif;
                font-size: 13px;
            }
            
            /* TreeWidget */
            QTreeWidget {
                background: ${SECONDARY_BG};
                border: 1px solid ${BORDER};
                border-radius: 6px;
                alternate-background-color: ${ALTERNATE_ROW};
                selection-background-color: ${SELECTION_BG};
                selection-color: ${TEXT};
                padding: 5px;
            }
            
            QTreeWidget::item {
                border-radius: 3px;
                padding: 5px 2px;
                margin: 2px 0;
            }
            
            QTreeWidget::item:selected {
                background-color: ${SELECTION_BG};
            }
            
            QTreeWidget::branch {
                background-color: transparent;
            }
            
            /* Başlıklar */
            QHeaderView::section {
                background: ${DISABLED_BG};
                border: none;
                border-right: 1px solid ${BORDER};
                border-bottom: 1px solid ${BORDER};
                font-weight: bold;
                padding: 8px 4px;
            }
            
            /* Düğmeler */
            QPushButton {
                background: ${ACCENT};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                margin: 4px 0;
                font-weight: 500;
                text-transform: uppercase;
                font-size: 12px;
                letter-spacing: 0.5px;
            }
            
            QPushButton:hover {
                background: ${ACCENT_HOVER};
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
            }
            
            QPushButton:pressed {
                background: ${ACCENT_PRESSED};
            }
            
            QPushButton:disabled {
                background: ${DISABLED_BG};
                color: ${DISABLED_TEXT};
            }
            
            /* Özel düğmeler */
            QPushButton#btn_save {
                background: ${SAVE_BUTTON};
            }
            
            QPushButton#btn_add {
                background: ${START_BUTTON};
            }
            
            QPushButton#btn_add:hover {
                background: ${START_BUTTON_HOVER};
            }
            
            QPushButton#btn_delete {
                background: ${STOP_BUTTON};
            }
            
            QPushButton#btn_delete:hover {
                background: ${STOP_BUTTON_HOVER};
            }
            
            /* İletişim kutuları */
            QMessageBox {
                background: ${MAIN_BG};
            }
            
            QDialog {
                background: ${MAIN_BG};
            }
            
            /* Metin girişi */
            QLineEdit, QTextEdit {
                background: ${SECONDARY_BG};
                border: 1px solid ${BORDER};
                border-radius: 4px;
                padding: 6px;
                color: ${TEXT};
            }
            
            QLineEdit:focus, QTextEdit:focus {
                border: 1px solid ${ACCENT};
            }
            
            /* Combobox */
            QComboBox {
                background: ${SECONDARY_BG};
                border: 1px solid ${BORDER};
                border-radius: 4px;
                padding: 6px;
                color: ${TEXT};
            }
            
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: center right;
                width: 24px;
                border-left: none;
            }
            
            QComboBox QAbstractItemView {
                background: ${SECONDARY_BG};
                border: 1px solid ${BORDER};
                selection-background-color: ${SELECTION_BG};
            }
            
            /* Kaydırma Çubukları */
            QScrollBar:vertical {
                background: ${MAIN_BG};
                width: 10px;
                margin: 0;
            }
            
            QScrollBar::handle:vertical {
                background: ${BORDER};
                min-height: 30px;
                border-radius: 5px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: ${ACCENT};
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;
                background: none;
            }
        """
        
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