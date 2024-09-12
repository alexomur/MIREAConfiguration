from .Command import Command
import __main__
import os

class Cd(Command):
    name: str = "change_direction"
    aliases: list[str] = ["cd"]
    description: str = "Changes the current direction"

    def execute(self, arguments: list[str]) -> bool:
        if len(arguments) == 0:
            print(f"{self.name} requires at least one argument")
            return False
        __main__.current_direction = os.path.join(__main__.current_path, arguments[0])
        print(os.path.join(__main__.current_path, arguments[0]))

        return True