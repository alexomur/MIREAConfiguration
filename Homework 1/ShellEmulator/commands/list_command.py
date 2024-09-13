from .command_abc import Command
import __main__ as main
import os
from .utils import resolve_path

class List(Command):
    name: str = "list"
    aliases = ["ls", "dir"]
    description: str = "List of files in directory"

    def execute(self, arguments: list[str]) -> bool:
        # Используем resolve_directory для поиска директории
        if len(arguments) == 0:
            virtual_directory, real_directory = resolve_path(main.current_path)
        else:
            virtual_directory, real_directory = resolve_path(arguments[0])

        if real_directory is None:
            print(f"Error: Directory '{virtual_directory}' does not exist.")
            return False

        files = os.listdir(real_directory)

        for file in files:
            print(file)

        return True