from .command_abc import Command
import __main__ as main
from .utils import resolve_path

class Cd(Command):
    name: str = "change_direction"
    aliases: list[str] = ["cd"]
    description: str = "Changes the current direction"

    def execute(self, arguments: list[str]) -> bool:
        if len(arguments) == 0:
            print(f"{self.name} requires at least one argument")
            return False

        virtual_directory, real_directory = resolve_path(arguments[0])

        if real_directory is None:
            print(f"Error: Directory '{virtual_directory}' does not exist.")
            return False

        main.set_current_path(virtual_directory)
        return True