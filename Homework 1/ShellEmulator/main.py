"""
I'll start with a preface that I really wanted to do the Homework in C# or something more interesting.
But then I read 2-4 assignments and realized that Python is my choice.
"""
import shlex

from zip_handler import extract_zip
import commands
from commands import get_command
from commands import GlobalManager
from configs import сonfig_utils

# Global variables and setters accessible from all files
config: dict = сonfig_utils.get_config()


# Main loop
def main() -> None:

    GlobalManager.set_global_path(extract_zip(config['path_to_zip']))

    while not GlobalManager.exiting:
        line: str = input(f"{config['username']}:{GlobalManager.current_path}# ")
        if len(line) == 0:
            continue

        command_name: str = line.split()[0]

        args = shlex.split(line)[1:]
        if command := get_command(command_name):
            success, output = command.execute(args)
            if output:
                print(output)
        else:
            print(f"Unknown command: {command_name}")


if __name__ == '__main__':
    main()
