from .utils import GlobalManager
from .command_abc import Command
from typing import List, Tuple


class History(Command):
    name: str = "history"
    aliases: List[str] = []
    description: str = "Displays the command history."

    def execute(self, arguments: List[str]) -> Tuple[bool, str]:
        """
        :param arguments: List of command-line arguments.
        :return: True if executed successfully, False otherwise. Out str - something to print
        """
        try:
            history: str
            if arguments:
                if arguments[0].isdigit():
                    num = int(arguments[0])
                    history = self.get_history(num)
                else:
                    return False, f"Error: Invalid argument '{arguments[0]}' for 'history'.\nUsage:\n  history [N]"
            else:
                history = self.get_history()

            return True, history

        except Exception as e:
            return False, f"General error: {e}"

    @staticmethod
    def get_history(num: int = None) -> str:
        history = GlobalManager.get_command_history()

        if num is not None:
            history = history[-num:]

        output: str = ""

        for idx, command in enumerate(history, start=1):
            output += f"{idx}  {command}\n"
        return output
