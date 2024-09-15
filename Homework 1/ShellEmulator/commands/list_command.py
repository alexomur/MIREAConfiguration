from typing import Tuple

from .command_abc import Command
import __main__ as main
import os
from .utils import resolve_path

class List(Command):
    name: str = "list"
    aliases: list[str] = ["ls", "dir"]
    description: str = "Lists files in the specified directory."

    def execute(self, arguments: list[str]) -> Tuple[bool, str]:
        """
        :param arguments: List of command-line arguments.
        :return: True if executed successfully, False otherwise. Out str - something to print
        """
        try:
            if not arguments:
                virtual_directory, real_directory = resolve_path(main.current_path)
            else:
                virtual_directory, real_directory = resolve_path(arguments[0])

            if real_directory is None:
                return False, f"Error: Directory '{virtual_directory}' does not exist."

            try:
                files = os.listdir(real_directory)
            except PermissionError:
                return False, f"Error: Permission denied for directory '{virtual_directory}'."
            except Exception as e:
                return False, f"Error accessing directory '{virtual_directory}': {e}"

            output = ""
            for file in files:
                output += f"{file}\n"

            return True, output[:-1]

        except Exception as e:
            return False, f"General error: {e}"
