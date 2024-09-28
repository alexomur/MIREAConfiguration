from typing import Tuple

from .command_abc import Command
from .utils import resolve_path, GlobalManager


class Cd(Command):
    name: str = "cd"
    aliases: list[str] = []
    description: str = "Changes the current directory."

    def execute(self, arguments: list[str]) -> Tuple[bool, str]:
        """
        :param arguments: List of command-line arguments.
        :return: Tuple[bool, str] - (success status, message to print)
        """
        try:
            if not arguments:
                return False, f"{self.name} requires at least one argument."

            target_path = arguments[0]

            virtual_directory = resolve_path(target_path)

            if virtual_directory is None:
                return False, f"Error: Directory '{target_path}' does not exist."

            if not virtual_directory.endswith('/'):
                virtual_directory += '/'

            GlobalManager.set_current_path(virtual_directory)
            return True, f"Changed directory to '{virtual_directory}'."

        except Exception as e:
            return False, f"General error: {e}"
