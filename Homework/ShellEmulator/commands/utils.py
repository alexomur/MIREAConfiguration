import re


def resolve_path(path: str) -> str | None:
    """
    Checks if it exists in the archive file system

    :param path: Path to file in the archive file system
    :return: Resolved path if it exists, None otherwise
    """
    segments = path.split('/')
    processed_segments = []

    # checking path for '..' and other dots constructs
    for segment in segments:
        if re.fullmatch(r'\.+', segment):
            dot_count = len(segment)
            up_levels = dot_count // 2
            processed_segments.extend(['..'] * up_levels)
            if dot_count % 2 != 0:
                processed_segments.append('.')
        else:
            processed_segments.append(segment)

    # coming back to /.../.../ form
    processed_segments = list(filter(None, processed_segments))
    if not processed_segments:
        processed_path = '/'
    else:
        processed_path = '/'.join(processed_segments)

    # checking path on existing
    if processed_path + '/' in GlobalManager.files:
        return processed_path + '/'
    elif '/' + processed_path in GlobalManager.files:
        return processed_path
    elif processed_path in GlobalManager.files:
        return processed_path
    elif GlobalManager.current_path + processed_path in GlobalManager.files:
        return GlobalManager.current_path + processed_path
    return None

# static class
class GlobalManager:
    files = {'/':''}
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
