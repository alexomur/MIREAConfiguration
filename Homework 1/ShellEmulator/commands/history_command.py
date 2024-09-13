from .command_abc import Command
import __main__ as main
from typing import List


class History(Command):
    name: str = "history"
    aliases: List[str] = []
    description: str = "Displays the command history."

    def execute(self, arguments: List[str]) -> bool:
        """
        :param arguments: List of command-line arguments.
        :return: True if executed successfully, False otherwise.
        """
        try:
            if arguments:
                if arguments[0].isdigit():
                    num = int(arguments[0])
                    self.print_history(num)
                else:
                    print(f"Error: Invalid argument '{arguments[0]}' for 'history'.")
                    print("Usage: history [N]")
                    return False
            else:
                self.print_history()

            return True

        except Exception as e:
            print(f"General error: {e}")
            return False

    @staticmethod
    def print_history(num: int = None) -> None:
        history = main.get_command_history()

        if num is not None:
            history = history[-num:]

        # Печатаем команды с их номерами
        for idx, command in enumerate(history, start=1):
            print(f"{idx}  {command}")
