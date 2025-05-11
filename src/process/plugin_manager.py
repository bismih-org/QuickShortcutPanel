import json
import os
import sys
import importlib.util

from src.static.file_paths import Paths


def get_plugins():
    plugins_with_data = []
    for _, _, files in os.walk(Paths.prepared_plugin_path):
        for file in files:
            if file.endswith(".json"):
                plug_name = file.strip(".json")
                plug_data = get_plugin_data(plug_name)
                plugins_with_data.append([plug_name, plug_data])

    return plugins_with_data


def get_plugin_data(plugin_name):
    with open(Paths.prepared_plugin_path + "/" + plugin_name + ".json", "r") as f:
        data = json.load(f)
    return data


def save_plugin_data(plugin_name, data):
    with open(Paths.prepared_plugin_path + "/" + plugin_name + ".json", "w") as f:
        json.dump(data, f, indent=4)


def get_special_plugins():
    special_plugins = []
    for root, _, files in os.walk(Paths.spacial_plugin_path):
        for file in files:
            if file.endswith(".json"):
                data = get_special_plugins_data(os.path.join(root, file))
                special_plugins.append(
                    {
                        "data": data,
                        "path": root,
                    }
                )

    return special_plugins


def get_special_plugins_data(file):
    with open(file, "r") as f:
        data = json.load(f)
    return data


def run_plugin(path):
    print(path)
    plugin_abs_path = os.path.abspath(path)
    main_file = os.path.join(plugin_abs_path, "main.py")

    if not os.path.exists(main_file):
        raise FileNotFoundError(f"{main_file} dosyası bulunamadı.")

    if plugin_abs_path not in sys.path:
        sys.path.insert(0, plugin_abs_path)

    module_name = "main"
    spec = importlib.util.spec_from_file_location(module_name, main_file)
    main_module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = main_module

    spec.loader.exec_module(main_module)

    if hasattr(main_module, "run_plugin"):
        main_module.run_plugin(plugin_abs_path)
    else:
        raise ImportError(f"{main_file} dosyasında run_plugin fonksiyonu bulunamadı.")
