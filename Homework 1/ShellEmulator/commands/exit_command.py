from .command_abc import Command
import __main__ as main
from typing import List


class Exit(Command):
    name: str = "exit"
    aliases: List[str] = []
    description: str = "Stops the application."

    def execute(self, arguments: List[str]) -> bool:
        """
        :param arguments: List of command-line arguments.
        :return: True if executed successfully, False otherwise.
        """
        try:
            if arguments:
                print("Error: 'exit' command does not accept any arguments.")
                print("Usage:")
                print("  exit")
                return False

            main.set_exiting(True)
            return True

        except Exception as e:
            print(f"General error: {e}")
            return False
