from enum import Enum


class Process_Type(Enum):
    KEYBOARD_SHORTCUT = "Klavye kısayolu"
    BASH_COMMAND = "Bash Komutu"
    OPEN_LINK = "Link aç"
    RUN_APP = "Uygulama çalıştır"
    SPACIAL_PLUGINS = "Özel eklentiler"
    PREPARED_PLUGINS = "Hazır eklentiler"

    @classmethod
    def get_name(cls, value):
        for p in cls:
            if p.name == value:
                return p.value
