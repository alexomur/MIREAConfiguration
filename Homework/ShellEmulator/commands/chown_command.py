from .command_abc import Command
from typing import List
from .utils import resolve_path
from typing import Tuple


# this command has no more sense because of du demand of unzipping archive into the memory instead of temp dir
class Chown(Command):
    name: str = "chown"
    aliases: List[str] = []
    description: str = "Changes the owner and/or group of a file or directory. (ONLY FOR WINDOWS)"

    def execute(self, arguments: List[str]) -> Tuple[bool, str]:
        """
        :param arguments: List of command-line arguments.
        :return: True if executed successfully, False otherwise. Out str - something to print
        """
        try:
            if len(arguments) < 2:
                return False, "Error: 'chown' requires at least two arguments.\nUsage:\n  chown <owner>[:<group>] <file>..."

            files = arguments[1:]

            for file in files:
                resolved = resolve_path(file)
                if not resolved or resolved == (None, None):
                    return False, f"Error: File or directory '{file}' does not exist."

                # Hard process of changing owner...

                return True, f"Successfully changed ownership of '/{resolved}'"

        except Exception as e:
            return False, f"General error: {e}"
