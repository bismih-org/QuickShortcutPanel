import os


class Paths:
    # HOME -> /home/user
    HOME = os.path.expanduser("~")
    config_path = HOME + "/.config/quick_shortcut_panel/"
    log_path = config_path + "/log"
    menu_yaml_path = "data/menu.yaml"
    menu_json_path = "data/menu.json"

    home_menu_json_path = config_path + "data/menu.json"

    prepared_plugin_path = "data/prepared_plugins"
    spacial_plugin_path = "data/special_plugins"

    home_prepared_plugin_path = config_path + "data/prepared_plugins"
    home_spacial_plugin_path = config_path + "data/special_plugins"

    @classmethod
    def file_check(cls, path, reset=False):
        if not os.path.exists(path):
            os.makedirs(path)
        elif reset:
            os.system("rm -rf " + path)
            os.makedirs(path)
    
    @classmethod
    def file_path_check_home(cls, path_home, path_default):
        if not os.path.exists(path_home):
            os.system("rm -rf " + path_home)
            folder_path = os.path.dirname(path_home)
            os.makedirs(folder_path, exist_ok=True)
            if os.path.exists(path_home):
                if os.path.isdir(path_default):
                    os.system("cp -rf " + path_default + " " + path_home+ "../")
            else:
                os.system("cp -rf " + path_default + " " + path_home)
        return path_home
