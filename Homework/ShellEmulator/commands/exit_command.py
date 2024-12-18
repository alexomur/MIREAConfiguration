import os
import shutil

from .utils import GlobalManager
from .command_abc import Command
from typing import List, Tuple


class Exit(Command):
    name: str = "exit"
    aliases: List[str] = []
    description: str = "Stops the application."

    def execute(self, arguments: List[str]) -> Tuple[bool, str]:
        """
        :param arguments: List of command-line arguments.
        :return: True if executed successfully, False otherwise. Out str - something to print
        """
        try:
            if arguments:
                return False, "Error: 'exit' command does not accept any arguments.\nUsage:\n  exit"

            GlobalManager.set_exiting(True)
            return True, ""

        except Exception as e:
            return False, f"General error: {e}"
