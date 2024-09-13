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

        new_path = arguments[0]
        if not os.path.isabs(new_path):
            new_virtual_path = os.path.normpath(os.path.join(main.current_path, new_path)).replace(os.sep, "/")
            new_real_path = os.path.join(main.global_path, new_virtual_path.lstrip("/").replace("/", os.sep))
        else:
            new_virtual_path = os.path.normpath(new_path).replace(os.sep, "/")
            new_real_path = os.path.join(main.global_path, new_virtual_path.lstrip("/").replace("/", os.sep))

        if not os.path.isdir(new_real_path):
            print(f"Error: Directory '{new_virtual_path}' does not exist.")
            return False

        main.set_current_path(new_virtual_path)
        return True