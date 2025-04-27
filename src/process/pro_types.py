from enum import Enum

class Process_Type(Enum):
    KEYBOARD_SHORTCUT = "Klavye kısayolu"
    BASH_COMMAND = "Bash Komutu"
    RUN_APP = "Uygulama çalıştır"

    @classmethod
    def get_type(cls, value):
        for p in cls:
            if p.name == value:
                return p.value

