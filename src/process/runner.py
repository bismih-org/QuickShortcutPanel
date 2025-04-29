import subprocess
import os
import pyautogui
import sys


def run_command(data):
    command: str = data[0]["command"]
    is_on_terminal: bool = data[0]["is_terminal"]
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
        # Add more mappings if needed
    }
    for d in data:
        ctrl, alt, shift, meta, key = (
            d["ctrl"],
            d["alt"],
            d["shift"],
            d["meta"],
            d["key"],
        )

        if key in key_mapping:
            key = key_mapping[key]
        try:
            # Prepare shortcut list for pyautogui
            shortcut_keys = []
            if ctrl:
                shortcut_keys.append("ctrl")
            if alt:
                shortcut_keys.append("alt")
            if shift:
                shortcut_keys.append("shift")
            if meta:
                shortcut_keys.append("win")  # or 'command' on macOS
            shortcut_keys.append(key)

            # Show what's being executed
            shortcut_str = "+".join(shortcut_keys).upper()
            print(f"Executing: {shortcut_str}")

            # Execute the shortcut
            pyautogui.hotkey(*shortcut_keys)
        except Exception as e:
            print(f"Error: {str(e)}")
            return f"Error: {str(e)}"
