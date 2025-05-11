from PyQt6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QMessageBox,
    QGridLayout,
)
from PyQt6.QtCore import Qt


class BasicApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Ana pencere ayarları
        self.setWindowTitle("Basit PyQt6 Uygulaması")
        self.setGeometry(100, 100, 400, 300)  # x, y, genişlik, yükseklik

        # Ana widget ve layout oluşturma
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Başlık etiketi
        title_label = QLabel("Hoş Geldiniz")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(
            "font-size: 18px; font-weight: bold; margin-bottom: 10px;"
        )
        main_layout.addWidget(title_label)

        # Form düzeni için grid layout
        form_layout = QGridLayout()

        # İsim alanı
        name_label = QLabel("İsim:")
        self.name_input = QLineEdit()
        form_layout.addWidget(name_label, 0, 0)
        form_layout.addWidget(self.name_input, 0, 1)

        # Soyisim alanı
        surname_label = QLabel("Soyisim:")
        self.surname_input = QLineEdit()
        form_layout.addWidget(surname_label, 1, 0)
        form_layout.addWidget(self.surname_input, 1, 1)

        # Yaş alanı
        age_label = QLabel("Yaş:")
        self.age_input = QLineEdit()
        form_layout.addWidget(age_label, 2, 0)
        form_layout.addWidget(self.age_input, 2, 1)

        # Form layout'u ana layout'a ekle
        main_layout.addLayout(form_layout)

        # Butonlar için yatay layout
        button_layout = QHBoxLayout()

        # Kaydet butonu
        save_button = QPushButton("Kaydet")
        save_button.clicked.connect(self.save_data)
        button_layout.addWidget(save_button)

        # Temizle butonu
        clear_button = QPushButton("Temizle")
        clear_button.clicked.connect(self.clear_form)
        button_layout.addWidget(clear_button)

        # Çıkış butonu
        exit_button = QPushButton("Çıkış")
        exit_button.clicked.connect(self.close)
        button_layout.addWidget(exit_button)

        # Buton layout'unu ana layout'a ekle
        main_layout.addLayout(button_layout)

        # Durum mesajı için label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.status_label)

    def save_data(self):
        """Kaydet butonuna tıklandığında çalışacak fonksiyon"""
        name = self.name_input.text()
        surname = self.surname_input.text()
        age = self.age_input.text()

        if not name or not surname or not age:
            QMessageBox.warning(self, "Uyarı", "Lütfen tüm alanları doldurun!")
            return

        try:
            age_int = int(age)
            if age_int <= 0:
                QMessageBox.warning(self, "Uyarı", "Yaş pozitif bir sayı olmalıdır!")
                return

            # Burada verileri kaydedebilirsiniz (örneğin database'e)
            message = f"{name} {surname} ({age}) bilgileri başarıyla kaydedildi."
            self.status_label.setText(message)
            self.status_label.setStyleSheet("color: green;")

        except ValueError:
            QMessageBox.warning(self, "Uyarı", "Yaş alanına sadece sayı giriniz!")

    def clear_form(self):
        """Temizle butonuna tıklandığında çalışacak fonksiyon"""
        self.name_input.clear()
        self.surname_input.clear()
        self.age_input.clear()
        self.status_label.clear()
