from .command_abc import Command
from .exit_command import Exit
from .list_command import List
from .cd_command import Cd


def get_command(command_name: str) -> Command or None:
    commands = [Exit, List, Cd]

    for command_class in commands:
        if command_class.name == command_name:
            return command_class()

        if command_name in command_class.aliases:
            return command_class()

    return None


__all__ = ["get_command", "Command", "Exit", "List", "Cd"]