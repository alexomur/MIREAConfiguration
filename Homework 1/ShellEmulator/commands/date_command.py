from .command_abc import Command

from datetime import datetime
from typing import List, Tuple

"""
Just for the sake of testing... I gave ChatGPT-5-Preview the task of mimicking my code
And it wrote this class

At what point I stopped writing the code myself, is left for the observer to ponder
"""
class Date(Command):
    name: str = "date"
    aliases: List[str] = []
    description: str = "Displays the current date and time or formats it according to the provided argument."

    def execute(self, arguments: List[str]) -> Tuple[bool, str]:
        """
        :param arguments: List of command-line arguments.
        :return: True if executed successfully, False otherwise.
        """
        try:
            if not arguments:
                current_datetime = datetime.now()
                return True, current_datetime.strftime("%a %b %d %H:%M:%S %Y")
            elif len(arguments) == 1:
                format_arg = arguments[0]
                if format_arg.startswith('+'):
                    format_string = format_arg[1:]
                    try:
                        formatted_date = datetime.now().strftime(format_string)
                        return True, formatted_date
                    except Exception as e:
                        return False, f"Error formatting date: {e}"
                else:
                    return False, "Error: Format must start with '+'. For example, '+%Y-%m-%d %H:%M:%S'."
            else:
                return False, "Error: Incorrect number of arguments.\nUsage:\n  date\n  date \"+<format>\""
        except Exception as e:
            return False, f"General error: {e}"