from .command_abc import Command
import __main__ as main
import os
from .utils import resolve_path

class List(Command):
    name: str = "list"
    aliases: list[str] = ["ls", "dir"]
    description: str = "Lists files in the specified directory."

    def execute(self, arguments: list[str]) -> bool:
        """
        :param arguments: List of command-line arguments.
        :return: True if executed successfully, False otherwise.
        """
        try:
            if not arguments:
                virtual_directory, real_directory = resolve_path(main.current_path)
            else:
                virtual_directory, real_directory = resolve_path(arguments[0])

            if real_directory is None:
                print(f"Error: Directory '{virtual_directory}' does not exist.")
                return False

            try:
                files = os.listdir(real_directory)
            except PermissionError:
                print(f"Error: Permission denied for directory '{virtual_directory}'.")
                return False
            except Exception as e:
                print(f"Error accessing directory '{virtual_directory}': {e}")
                return False

            for file in files:
                print(file)

            return True

        except Exception as e:
            print(f"General error: {e}")
            return False
