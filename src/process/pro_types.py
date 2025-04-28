from enum import Enum


class Process_Type(Enum):
    MENU_ITEM_GROUP = "Menü öğesi grubu"
    SPACIAL_PLUGINS = "Özel eklentiler"
    KEYBOARD_SHORTCUT = "Klavye kısayolu"
    BASH_COMMAND = "Bash Komutu"
    RUN_APP = "Uygulama çalıştır"

    @classmethod
    def get_name(cls, value):
        for p in cls:
            if p.name == value:
                return p.value
