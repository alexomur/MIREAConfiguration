from .command_abc import Command

from datetime import datetime
from typing import List

"""
Just for the sake of testing... I gave ChatGPT-5-Preview the task of mimicking my code
And it wrote this class

At what point I stopped writing the code myself, is left for the observer to ponder
"""
class Date(Command):
    name: str = "date"
    aliases: List[str] = []
    description: str = "Displays the current date and time or formats it according to the provided argument."

    def execute(self, arguments: List[str]) -> bool:
        """
        :param arguments: List of command-line arguments.
        :return: True if executed successfully, False otherwise.
        """
        try:
            if not arguments:
                current_datetime = datetime.now()
                print(current_datetime.strftime("%a %b %d %H:%M:%S %Y"))
                return True
            elif len(arguments) == 1:
                format_arg = arguments[0]
                if format_arg.startswith('+'):
                    format_string = format_arg[1:]
                    try:
                        formatted_date = datetime.now().strftime(format_string)
                        print(formatted_date)
                        return True
                    except Exception as e:
                        print(f"Error formatting date: {e}")
                        return False
                else:
                    print("Error: Format must start with '+'. For example, '+%Y-%m-%d %H:%M:%S'.")
                    return False
            else:
                print("Error: Incorrect number of arguments.")
                print("Usage:")
                print("  date")
                print('  date "+<format>"')
                return False
        except Exception as e:
            print(f"General error: {e}")
            return False