import os
import subprocess
import pyautogui
import threading
from src.process.pro_types import Process_Type


def run_action(data):
    for action in data:
        if action["type"] == Process_Type.BASH_COMMAND.name:
            thread = threading.Thread(target=run_command, args=(action["data"],))
            thread.daemon = False
            thread.start()
        elif action["type"] == Process_Type.KEYBOARD_SHORTCUT.name:
            run_shortcut(action["data"])
        elif action["type"] == Process_Type.OPEN_LINK.name:
            open_links(action["data"])
        elif action["type"] == Process_Type.RUN_APP.name:
            thread = threading.Thread(target=open_app, args=(action["data"],))
            thread.daemon = False
            thread.start()
        elif action["type"] == Process_Type.SPACIAL_PLUGINS.name:
            thread = threading.Thread(target=run_spacial_plugin, args=(action["data"],))
            thread.daemon = False
            thread.start()
        else:
            print(f"Unknown action type: {action['type']}")


def open_app(data):
    app_name = data["exec"]
    run_command({"command": app_name, "is_terminal": False})


def open_links(data):
    links = data["links"]
    if not links:
        return
    open_links = ""
    for link in links:
        open_links += f"xdg-open {link} & "

    run_command({"command": open_links, "is_terminal": False})


def run_spacial_plugin(data):
    path = data["path"]
    print(path)
    plugin_abs_path = os.path.abspath(path)
    main_file = os.path.join(plugin_abs_path, "main.py")

    if not os.path.exists(main_file):
        raise FileNotFoundError(f"{main_file} dosyası bulunamadı.")
    print(main_file)
    # main.py'yi ayrı bir process olarak başlat
    subprocess.Popen(["python3", main_file, plugin_abs_path])


def run_command(data):
    command: str = data["command"]
    is_on_terminal: bool = data["is_terminal"]
    print(f"Command: {command} is_terminal: {is_on_terminal}")
    env = os.environ.copy()
    env.pop("QT_QPA_PLATFORM_PLUGIN_PATH", None)
    env.pop("QT_PLUGIN_PATH", None)
    env.pop("QT_API", None)
    if is_on_terminal:
        # Run in terminal
        subprocess.Popen(
            f"konsole -e bash -c \"{command} && read -p 'Press Enter to continue...'\"",
            shell=True,
            env=env,
        )
        return "Command launched in terminal"
    else:
        try:
            _ = subprocess.run(command, shell=True, env=env, check=True, text=True)
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr}"


def run_shortcut(data):
    key_mapping = {
        "esc": "escape",
        "pgup": "pageup",
        "pgdn": "pagedown",
    }
    ctrl, alt, shift, meta, key = (
        data["ctrl"],
        data["alt"],
        data["shift"],
        data["meta"],
        data["key"].lower(),  # Key'i lowercase yapıyoruz
    )

    if key in key_mapping:
        key = key_mapping[key]
    try:
        # Tuşları tek tek basma ve bırakma
        if ctrl:
            pyautogui.keyDown("ctrl")
        if alt:
            pyautogui.keyDown("alt")
        if shift:
            pyautogui.keyDown("shift")
        if meta:
            pyautogui.keyDown("win")  # or 'command' on macOS

        pyautogui.press(key)

        # Tuşları bırakma (ters sırada)
        if meta:
            pyautogui.keyUp("win")
        if shift:
            pyautogui.keyUp("shift")
        if alt:
            pyautogui.keyUp("alt")
        if ctrl:
            pyautogui.keyUp("ctrl")

        # Log için
        shortcut_keys = []
        if ctrl:
            shortcut_keys.append("ctrl")
        if alt:
            shortcut_keys.append("alt")
        if shift:
            shortcut_keys.append("shift")
        if meta:
            shortcut_keys.append("win")
        shortcut_keys.append(key)
        shortcut_str = "+".join(shortcut_keys).upper()
        print(f"Executed: {shortcut_str}")

        return f"Başarıyla çalıştırıldı: {shortcut_str}"
    except Exception as e:
        print(f"Error: {str(e)}")
        return f"Error: {str(e)}"
