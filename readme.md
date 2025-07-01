# Kısayol

# Geliştirme için
```console
sudo apt install xdotool python3-pyqt6 python3-coloredlogs python3-yaml python3-xdg
```

![alt text](doc/app.png)
![alt text](doc/setting.png)
## Bağımlılıklar

`sudo apt install python3-serial python3-requests python3-coloredlogs python3-websockets usbutils`

veya

`pip install -r requirements.txt`

# Çalıştırmak için

`python3 Main.py`

# Derlemek için

```console
sudo apt install devscripts git-buildpackage
sudo mk-build-deps -ir
gbp buildpackage --git-export-dir=/tmp/build/bismih-welcome -us -uc --git-ignore-branch --git-ignore-new
```