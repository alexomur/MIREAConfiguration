from .command_abc import Command

# Используем модуль dateparser или вручную обрабатываем выражения
# Для простоты используем встроенные возможности datetime
# Пример: "next Monday", "+5 days", "-2 weeks"
# Заметим, что datetime.strptime не поддерживает такие выражения
# Поэтому используем метод fromisoformat или другое ограниченное парсинг
# Для полноты можно использовать библиотеку dateutil.parser

from dateutil import parser as date_parser
from dateutil.relativedelta import relativedelta

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import argparse
from typing import List

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