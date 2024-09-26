import os, re


def resolve_path(path: str) -> str | None:
    """
    Checks if it exists in the archive file system

    :param path: Absolute or relative path
    :return: Absolute resolved path if it exists, None otherwise
    """
    if path.startswith('/'):
        combined_path = path
    else:
        if GlobalManager.current_path == '/':
            combined_path = '/' + path
        else:
            combined_path = GlobalManager.current_path.rstrip('/') + '/' + path

    segments = combined_path.split('/')
    processed_segments = []

    # checking path for '..' and other dots constructs
    # Измени этот цикл, чтобы проверять различные нестандартные условия, например '..'
    for segment in segments:
        if segment == '..':
            if processed_segments:
                processed_segments.pop()
        elif segment == '.' or segment == '':
            continue
        else:
            processed_segments.append(segment)

    processed_segments = list(filter(None, processed_segments))
    if not processed_segments:
        processed_path = '/'
    else:
        processed_path = '/'.join(processed_segments)

    # Добавь сюда свой код, отвечающий за возврат пути
    # Проверка на существование директории с добавлением '/'
    if processed_path + '/' in GlobalManager.files:
        return processed_path + '/'
    elif processed_path in GlobalManager.files:
        return processed_path
    return None



# static class
class GlobalManager:
    files = {'/': ''}
    current_path: str = "/"
    exiting: bool = False
    command_history: list[str] = []

    def __init__(self):
        raise Exception(f"{type(GlobalManager).__name__} is an static class and cannot be instantiated")

    @staticmethod
    def set_current_path(path: str) -> None:
        GlobalManager.current_path = path

    @staticmethod
    def set_exiting(exiting: bool) -> None:
        GlobalManager.exiting = exiting

    @staticmethod
    def get_command_history() -> list:
        return GlobalManager.command_history.copy()

    @staticmethod
    def add_command_history(command: str) -> None:
        GlobalManager.command_history.append(command)

    @staticmethod
    def clear_command_history() -> None:
        GlobalManager.command_history = []

    @staticmethod
    def add_file(path: str, file) -> None:
        GlobalManager.files[path] = file

    @staticmethod
    def get_file(path: str) -> str | None:
        if path in GlobalManager.files.keys():
            return GlobalManager.files[path]
        return None


if __name__ == "__main__":
    resolve_path("/private/test/")