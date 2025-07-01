#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os
import subprocess


changelog = "debian/changelog"
if os.path.exists(changelog):
    head = open(changelog).readline()
    try:
        version = head.split("(")[1].split(")")[0]
    except:
        print("debian/changelog format is wrong for get version")
        version = "0.0.0"
    f = open("data/version", "w")
    f.write(version)
    f.close()


data_files = [
    # Main executable and desktop file
    ("/usr/bin", ["quick-shortcut-panel"]),
    ("/usr/bin", ["quick-shortcut-panel-config"]),
    ("/usr/share/applications", ["tr.org.bismih.quick-shortcut-panel.desktop"]),
    # Icons
    (
        "/usr/share/icons/hicolor/scalable/apps/",
        ["data/icons/quick-shortcut-panel.png"],
    ),
    ("/usr/share/icons/", ["data/icons/quick-shortcut-panel.png"]),
    # Main application files
    ("/usr/share/quickshortcutpanel/", ["main.py", "main_config.py"]),
    # Source code
    ("/usr/share/quickshortcutpanel/src/common", ["src/common/Logging.py"]),
    (
        "/usr/share/quickshortcutpanel/src/process",
        [
            "src/process/plugin_manager.py",
            "src/process/pro_types.py",
            "src/process/runner.py",
        ],
    ),
    (
        "/usr/share/quickshortcutpanel/src/static",
        ["src/static/config.py", "src/static/file_paths.py"],
    ),
    (
        "/usr/share/quickshortcutpanel/src/ui/menu_config",
        ["src/ui/menu_config/config_ui.py", "src/ui/menu_config/piece_node.py"],
    ),
    (
        "/usr/share/quickshortcutpanel/src/ui/menu_config/process_ui",
        [
            "src/ui/menu_config/process_ui/app_selecetor.py",
            "src/ui/menu_config/process_ui/command_runner_ui.py",
            "src/ui/menu_config/process_ui/config_dialog.py",
            "src/ui/menu_config/process_ui/link_opener.py",
            "src/ui/menu_config/process_ui/short_cut_selector.py",
            "src/ui/menu_config/process_ui/spacial_plugin.py",
        ],
    ),
    (
        "/usr/share/quickshortcutpanel/src/ui/panel",
        ["src/ui/panel/main_panel.py", "src/ui/panel/piece.py"],
    ),
    ("/usr/share/quickshortcutpanel/src/ui/theme", ["src/ui/theme/theme_manager.py"]),
    (
        "/usr/share/quickshortcutpanel/src/ui/theme/icons",
        [
            "src/ui/theme/icons/branch-closed.png",
            "src/ui/theme/icons/branch-open.png",
            "src/ui/theme/icons/check-white.png",
        ],
    ),
    # Data files
    (
        "/usr/share/quickshortcutpanel/data",
        ["data/menu.json", "data/menu.yaml", "data/theme.qss", "data/version"],
    ),
    (
        "/usr/share/quickshortcutpanel/data/icons",
        ["data/icons/quick-shortcut-panel.png"],
    ),
    # Prepared plugins
    (
        "/usr/share/quickshortcutpanel/data/prepared_plugins",
        [
            "data/prepared_plugins/Hoparlör_Eko.json",
            "data/prepared_plugins/Hoparlör_gürültü.json",
            "data/prepared_plugins/Hoparlör_Normal.json",
            "data/prepared_plugins/Mirofon_Gürültü.json",
            "data/prepared_plugins/yazilim_modu.json",
        ],
    ),
]


setup(
    name="quick-shortcut-panel",
    version=version,
    packages=find_packages(),
    scripts=["quick-shortcut-panel"],
    install_requires=["PyQt6", "pyautogui", "coloredlogs", "pyyaml", "pyxdg"],
    data_files=data_files,
    author="Muhammet Halak",
    author_email="halakmuhammet145@gmail.com",
    description="A quick shortcut panel for Linux",
    license="GPLv3",
    keywords="quick-shortcut-panel, quick, panel, hızlı, kısayol",
    url="https://github.com/bismih-org/QuickShortcutPanel",
)
