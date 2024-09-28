"""
I'll start with a preface that I really wanted to do the Homework in C# or something more interesting.
But then I read 2-4 assignments and realized that Python is my choice.
"""
import shlex

from zip_handler import extract_zip
from commands import get_command
from commands import GlobalManager
from configs import сonfig_utils

config: dict


def set_up(cfg: dict = None, files: dict = None, current_path: str = '/'):
    global config

    if cfg is not None:
        config = cfg
    else:
        config = сonfig_utils.get_config()

    if files:
        for file in files:
            GlobalManager.add_file(file, files[file])
    else:
        extract_zip(config['path_to_zip'])

    GlobalManager.set_current_path(current_path)


def main() -> None:
    set_up()

    while not GlobalManager.exiting:
        try:
            line: str = input(f"{config['username']}:{GlobalManager.current_path}# ")
            if len(line.strip()) == 0:
                continue

            tokens = shlex.split(line)
            if not tokens:
                continue

            command_name: str = tokens[0]
            args = tokens[1:]

            command = get_command(command_name)
            if command:
                success, output = command.execute(args)
                if output:
                    print(output)
                GlobalManager.add_command_history(f"{line} | {'Success' if success else 'Failure'}")
            else:
                print(f"Unknown command: {command_name}")
        except KeyboardInterrupt:
            print("\nExiting shell.")
            GlobalManager.set_exiting(True)
        except EOFError:
            print("\nExiting shell.")
            GlobalManager.set_exiting(True)
        except Exception as e:
            print(f"General Error: {e}")


if __name__ == '__main__':
    main()
