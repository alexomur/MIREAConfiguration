from .Command import Command
from .Exit import Exit
from .List import List
from .Cd import Cd


def get_command(command_name: str) -> Command or None:
    commands = [Exit, List, Cd]

    for command_class in commands:
        if command_class.name == command_name:
            return command_class()

        if command_name in command_class.aliases:
            return command_class()

    return None


__all__ = ["get_command", "Command", "Exit", "List", "Cd"]