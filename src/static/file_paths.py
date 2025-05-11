import os


class Paths:
    # HOME -> /home/user
    HOME = os.path.expanduser("~")
    config_path = HOME + "/.config/quick_shortcut_panel"
    log_path = config_path + "/log"
    menu_yaml_path = "data/menu.yaml"
    menu_json_path = "data/menu.json"

    prepared_plugin_path = "data/prepared_plugins"
    spacial_plugin_path = "data/special_plugins"

    @classmethod
    def file_check(cls, path, reset=False):
        if not os.path.exists(path):
            os.makedirs(path)
        elif reset:
            os.system("rm -rf " + path)
            os.makedirs(path)
