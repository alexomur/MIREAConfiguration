"""
I'll start with a preface that I really wanted to do the Homework in C# or something more interesting.
But then I read 2-4 assignments and realized that Python is my choice.
"""
import shlex

from zip_handler import extract_zip
from commands import get_command
from configs import сonfig_utils

# Global variables and setters accessible from all files
exiting: bool = False
global_path: str
current_path: str = "/"
config: dict = Config.get_config()
command_history = []

def get_command_history():
    return command_history

def add_command_history(command: str):
    command_history.append(command)

def set_exiting(new_value: bool) -> None:
    global exiting
    exiting = new_value

def set_current_path(new_value: str) -> None:
    global current_path
    current_path = new_value

def set_global_path(new_value: str) -> None:
    global global_path
    global_path = new_value


# Main loop
def main() -> None:
    global exiting, global_path, current_path

    global_path = extract_zip(config['path_to_zip'])

    while not exiting:
        line: str = input(f"{config['username']}:{current_path}# ")
        if len(line) == 0:
            continue

        command_name: str = line.split()[0]

        args = shlex.split(line)[1:]
        if command := get_command(command_name):
            command.execute(args)
        else:
            print(f"Unknown command: {command_name}")

if __name__ == '__main__':
    main()
