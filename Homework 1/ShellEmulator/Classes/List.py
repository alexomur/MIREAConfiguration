from .Command import Command
import __main__
import os

class List(Command):
    name: str = "list"
    aliases = ["ls"]
    description: str = "List of files in directory"

    def execute(self, arguments: list[str]) -> bool:
        if len(arguments) == 0:
            directory = str(os.path.join(__main__.global_path, __main__.current_path))
        else:
            directory = arguments[0]

        files = os.listdir(directory)
        files = [f for f in files if os.path.join(directory, f)]

        for file in files:
            print(file)

        return True