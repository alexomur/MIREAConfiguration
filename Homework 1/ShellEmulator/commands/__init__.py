import __main__ as main
from .command_abc import Command
from .exit_command import Exit
from .list_command import List
from .cd_command import Cd
from .date_command import Date
from .chown_command import Chown
from .history_command import History


def get_command(command_name: str) -> Command or None:
    commands = [Exit, List, Cd, Date, Chown, History]

    for command_class in commands:
        if command_class.name == command_name:
            main.add_command_history(command_name)
            return command_class()

        if command_name in command_class.aliases:
            main.add_command_history(command_name)
            return command_class()

    return None


__all__ = ["get_command", "Command", "Exit", "List", "Cd", "Date", "Chown", "History"]
