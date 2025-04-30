import subprocess
import pyautogui
import threading
from src.process.pro_types import Process_Type


def run_action(data):
    for a in data:
        if a["type"] == Process_Type.BASH_COMMAND.name:
            thread = threading.Thread(target=run_command, args=(a["data"],))
            thread.daemon = False
            thread.start()
        elif a["type"] == Process_Type.KEYBOARD_SHORTCUT.name:
            run_shortcut(a["data"])
        else:
            print(f"Unknown action type: {a['type']}")


def run_command(data):
    command: str = data["command"]
    is_on_terminal: bool = data["is_terminal"]
    print(f"Command: {command} is_terminal: {is_on_terminal}")
    if is_on_terminal:
        # Run in terminal
        subprocess.Popen(
            f"konsole -e bash -c \"{command} && read -p 'Press Enter to continue...'\"",
            shell=True,
        )
        return "Command launched in terminal"
    else:
        try:
            _ = subprocess.run(command, shell=True, check=True, text=True)
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
            pyautogui.keyDown('ctrl')
        if alt:
            pyautogui.keyDown('alt')
        if shift:
            pyautogui.keyDown('shift')
        if meta:
            pyautogui.keyDown('win')  # or 'command' on macOS
        
        pyautogui.press(key)
        
        # Tuşları bırakma (ters sırada)
        if meta:
            pyautogui.keyUp('win')
        if shift:
            pyautogui.keyUp('shift')
        if alt:
            pyautogui.keyUp('alt')
        if ctrl:
            pyautogui.keyUp('ctrl')
            
        # Log için
        shortcut_keys = []
        if ctrl: shortcut_keys.append("ctrl")
        if alt: shortcut_keys.append("alt")
        if shift: shortcut_keys.append("shift")
        if meta: shortcut_keys.append("win")
        shortcut_keys.append(key)
        shortcut_str = "+".join(shortcut_keys).upper()
        print(f"Executed: {shortcut_str}")
        
        return f"Başarıyla çalıştırıldı: {shortcut_str}"
    except Exception as e:
        print(f"Error: {str(e)}")
        return f"Error: {str(e)}"
