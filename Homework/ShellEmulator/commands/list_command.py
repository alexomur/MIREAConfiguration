from typing import Tuple

from .utils import GlobalManager
from .command_abc import Command
from .utils import resolve_path


class List(Command):
    name: str = "list"
    aliases: list[str] = ["ls", "dir"]
    description: str = "Lists files in the specified directory."

    def execute(self, arguments: list[str]) -> Tuple[bool, str]:
        """
        :param arguments: List of command-line arguments.
        :return: Tuple[bool, str] - (success status, message to print)
        """
        try:
            # Определяем виртуальную директорию
            if not arguments:
                virtual_directory = resolve_path(GlobalManager.current_path)
            else:
                virtual_directory = resolve_path(arguments[0])

            if virtual_directory is None:
                dir_name = arguments[0] if arguments else GlobalManager.current_path
                return False, f"Error: Directory '{dir_name}' does not exist."

            # Убедимся, что виртуальная директория заканчивается '/'
            if not virtual_directory.endswith('/'):
                virtual_directory += '/'

            if virtual_directory == "/":
                prefix = ""
            else:
                prefix = virtual_directory

            items = set()
            for path in GlobalManager.files.keys():
                if not path.startswith(prefix):
                    continue

                # Удаляем префикс виртуальной директории из пути
                remainder = path[len(prefix):]

                # Пропускаем, если это сама директория
                if not remainder:
                    continue

                # Разделяем оставшуюся часть пути по первому '/'
                parts = remainder.split('/', 1)

                if len(parts) == 2:
                    # Это поддиректория
                    items.add(parts[0] + '/')
                else:
                    # Это файл
                    items.add(parts[0])

            # Формируем отсортированный вывод
            output = '\n'.join(sorted(items))
            return True, output

        except Exception as e:
            return False, f"General error: {e}"
