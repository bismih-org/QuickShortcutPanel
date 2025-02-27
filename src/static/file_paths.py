import os

class Path:
    # HOME -> /home/user
    HOME = os.path.expanduser("~")
    config_path = HOME + "/.config/quick_shortcut_panel"
    log_path = config_path + "/log"

    @classmethod
    def file_check(self, path, reset=False):
        if not os.path.exists(path):
            os.makedirs(path)
        elif reset:
            os.system("rm -rf "+path)
            os.makedirs(path)