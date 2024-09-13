"""
I'll start with a preface that I really wanted to do the Homework in C# or something more interesting.
But then I read 2-4 assignments and realized that Python is my choice.
"""
import os.path, shlex, zipfile, tempfile

from Classes import *
from Configs import Config

exiting: bool = False
global_path: str
current_path: str = ""
config: dict = Config.get_config()

def extract_zip():
    with zipfile.ZipFile(config["path_to_zip"], "r") as zip_f:
        temp_dir = tempfile.mkdtemp()
        zip_f.extractall(temp_dir)
        return temp_dir

def main() -> None:
    global exiting, global_path, current_path

    global_path = extract_zip()

    known_commands = {
        "ls": List(),
        "exit": Exit(),
        "cd": Cd(),
    }

    while not exiting:
        line: str = input(f"{config['username']}{current_path}> ")
        if len(line) == 0:
            continue

        command_name: str = line.split()[0]

        args = shlex.split(''.join(line.split()[1:]))
        if command := known_commands.get(command_name):
            command.execute(args)
        else:
            print(f"Unknown command: {command_name}")

if __name__ == '__main__':
    main()
