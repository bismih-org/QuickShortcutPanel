import subprocess
import os




def run_command(command: str, is_on_terminal: bool):
    if is_on_terminal:
        # Run in terminal
        subprocess.Popen(f'konsole -e bash -c "{command} && read -p \'Press Enter to continue...\'"', shell=True)
        return "Command launched in terminal"
    else:
        try:
            _ = subprocess.run(command, shell=True, check=True, text=True)
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr}"


def run_shortcut():
    pass