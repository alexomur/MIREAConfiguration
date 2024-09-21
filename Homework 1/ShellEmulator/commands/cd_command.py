from .command_abc import Command
from .utils import resolve_path, GlobalManager
from typing import Tuple


class Cd(Command):
    name: str = "change_direction"
    aliases: list[str] = ["cd"]
    description: str = "Changes the current directory."

    def execute(self, arguments: list[str]) -> Tuple[bool, str]:
        """
        :param arguments: List of command-line arguments.
        :return: True if executed successfully, False otherwise. Out str - something to print
        """
        try:
            if not arguments:
                return False, f"{self.name} requires at least one argument."

            virtual_directory, real_directory = resolve_path(arguments[0])

            if real_directory is None:
                return False, f"Error: Directory '{arguments[0]}' does not exist."

            GlobalManager.set_current_path(virtual_directory)
            return True, ""

        except Exception as e:
            return False, f"General error: {e}"
