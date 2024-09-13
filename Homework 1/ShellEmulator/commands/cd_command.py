from .command_abc import Command
import __main__ as main
from .utils import resolve_path

class Cd(Command):
    name: str = "change_direction"
    aliases: list[str] = ["cd"]
    description: str = "Changes the current directory."

    def execute(self, arguments: list[str]) -> bool:
        """
        :param arguments: List of command-line arguments.
        :return: True if executed successfully, False otherwise.
        """
        try:
            if not arguments:
                print(f"{self.name} requires at least one argument.")
                return False

            virtual_directory, real_directory = resolve_path(arguments[0])

            if real_directory is None:
                print(f"Error: Directory '{virtual_directory}' does not exist.")
                return False

            main.set_current_path(virtual_directory)
            return True

        except Exception as e:
            print(f"General error: {e}")
            return False
