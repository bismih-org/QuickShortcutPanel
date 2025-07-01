import json
import os

from src.static.file_paths import Paths


def get_plugins():
    plugins_with_data = []
    Paths.file_check(
        Paths.file_path_check_home(
            Paths.home_prepared_plugin_path, Paths.prepared_plugin_path
        )
    )
    for _, _, files in os.walk(
        Paths.file_path_check_home(
            Paths.home_prepared_plugin_path, Paths.prepared_plugin_path
        )
    ):
        print("Plugins: ", files)
        for file in files:
            if file.endswith(".json"):
                plug_name = file[:-5]

                try:
                    plug_data = get_plugin_data(plug_name)
                    plugins_with_data.append([plug_name, plug_data])
                except FileNotFoundError as e:
                    print(f"Hata: {plug_name} dosyası açılamadı: {e}")
                except json.JSONDecodeError as e:
                    print(f"JSON hata: {plug_name} dosyası geçerli bir JSON değil: {e}")
                except Exception as e:
                    print(f"Beklenmeyen hata: {plug_name} dosyası için: {e}")

    return plugins_with_data


def get_plugin_data(plugin_name):
    # Dosya yolunu oluştururken os.path.join kullanmak daha güvenlidir
    file_path = os.path.join(
        Paths.file_path_check_home(
            Paths.home_prepared_plugin_path, Paths.prepared_plugin_path
        ),
        f"{plugin_name}.json",
    )

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def save_plugin_data(plugin_name, data):
    plugin_name = plugin_name.split(" ")
    plugin_name = "_".join(plugin_name)

    # Dosya yolunu oluştururken os.path.join kullanmak daha güvenlidir
    file_path = os.path.join(
        Paths.file_path_check_home(
            Paths.home_prepared_plugin_path, Paths.prepared_plugin_path
        ),
        f"{plugin_name}.json",
    )

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def get_special_plugins():
    special_plugins = []
    Paths.file_check(
        Paths.file_path_check_home(
            Paths.home_spacial_plugin_path, Paths.spacial_plugin_path
        )
    )
    for root, _, files in os.walk(
        Paths.file_path_check_home(
            Paths.home_spacial_plugin_path, Paths.spacial_plugin_path
        )
    ):
        for file in files:
            if file.endswith(".json"):
                try:
                    data = get_special_plugins_data(os.path.join(root, file))
                    special_plugins.append(
                        {
                            "data": data,
                            "path": root,
                        }
                    )
                except Exception as e:
                    print(f"Hata: {file} dosyası işlenemedi: {e}")

    return special_plugins


def get_special_plugins_data(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data
