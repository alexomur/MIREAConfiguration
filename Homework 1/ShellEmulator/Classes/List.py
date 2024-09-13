from .Command import Command
import __main__ as main
import os

class List(Command):
    name: str = "list"
    aliases = ["ls", "dir"]
    description: str = "List of files in directory"

    def execute(self, arguments: list[str]) -> bool:
        if len(arguments) == 0:
            virtual_directory = main.current_path
            real_directory = os.path.join(main.global_path, virtual_directory.lstrip("/").replace("/", os.sep))
        else:
            virtual_directory = arguments[0]
            if not os.path.isabs(virtual_directory):
                virtual_directory = os.path.normpath(os.path.join(main.current_path, virtual_directory)).replace(os.sep, "/")
            real_directory = os.path.join(main.global_path, virtual_directory.lstrip("/").replace("/", os.sep))

        if not os.path.isdir(real_directory):
            print(f"Error: Directory '{virtual_directory}' does not exist.")
            return False

        files = os.listdir(str(real_directory))

        for file in files:
            print(file)

        return True