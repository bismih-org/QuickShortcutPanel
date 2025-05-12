import json
import os

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