from commands import Command

import os, re


def resolve_path(path: str) -> tuple[str, str] or None:
    """
    Resolves the given virtual path and checks if it exists in the real file system.

    :param path: The virtual path to a file or directory, which can be either relative or absolute.
    :return: A tuple (virtual_path, real_path) if the path exists, otherwise (None, None).
    """
    # Разделяем путь на сегменты
    segments = path.split('/')
    processed_segments = []

    for segment in segments:
        # Проверяем, состоит ли сегмент только из точек
        if re.fullmatch(r'\.+', segment):
            dot_count = len(segment)
            # Каждые две точки интерпретируем как '..'
            up_levels = dot_count // 2
            processed_segments.extend(['..'] * up_levels)
            # Если количество точек нечетное, добавляем один '.' в конце
            if dot_count % 2 != 0:
                processed_segments.append('.')
        else:
            # Оставляем сегмент без изменений
            processed_segments.append(segment)

    # Собираем обработанные сегменты обратно в путь
    normalized_virtual_path = "/".join(processed_segments)
    virtual_path = os.path.normpath(
        os.path.join(GlobalManager.current_path, normalized_virtual_path) if not os.path.isabs(
            normalized_virtual_path) else normalized_virtual_path).replace(os.sep, "/")

    real_path = os.path.join(GlobalManager.global_path, virtual_path.lstrip("/").replace("/", os.sep))

    if os.path.exists(real_path):  # Проверяем существование файла или директории
        return virtual_path, real_path

    return None, None


# static class
class GlobalManager:
    global_path: str
    current_path: str = "/"
    exiting: bool = False
    command_history: list[str] = []

    def __init__(self):
        raise Exception(f"{type(GlobalManager).__name__} is an static class and cannot be instantiated")

    @staticmethod
    def set_current_path(path: str) -> None:
        GlobalManager.current_path = path

    @staticmethod
    def set_global_path(path: str) -> None:
        GlobalManager.global_path = path

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
