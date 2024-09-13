from .Command import Command
import __main__ as main
import os

class Cd(Command):
    name: str = "change_direction"
    aliases: list[str] = ["cd"]
    description: str = "Changes the current direction"

    def execute(self, arguments: list[str]) -> bool:
        if len(arguments) == 0:
            print(f"{self.name} requires at least one argument")
            return False
        main.set_current_path(os.path.join(main.current_path, arguments[0]))
        return True