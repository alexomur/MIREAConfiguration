import os, re


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

    normalized_virtual_path = "/".join(processed_segments)
    if not os.path.isabs(normalized_virtual_path):
        combined_path = os.path.join(GlobalManager.current_path, normalized_virtual_path)
    else:
        combined_path = normalized_virtual_path

    virtual_path = os.path.normpath(combined_path).replace(os.sep, "/")

    if virtual_path == "/":
        return virtual_path

    # Remove leading '/' to match GlobalManager.files keys
    virtual_path = virtual_path.lstrip('/')

    # If path is directory, ensure it ends with '/'
    if not virtual_path.endswith('/'):
        potential_dir = virtual_path + '/'
        # Check if 'virtual_path/' exists or any file starts with 'virtual_path/'
        if GlobalManager.get_file(potential_dir) or any(p.startswith(potential_dir) for p in GlobalManager.files):
            virtual_path = potential_dir

    # Now check if virtual_path exists as directory
    if GlobalManager.get_file(virtual_path):
        return virtual_path

    # Additionally, consider directory existing if any file starts with virtual_path + '/'
    if any(p.startswith(virtual_path + '/') for p in GlobalManager.files):
        return virtual_path + '/'

    return None


class File:
    def __init__(self, is_dir: bool, name: str, path: str, files: list) -> None:
        self.is_dir = is_dir
        self.name = name
        self.path = path
        self.files = files

    def __str__(self):
        return self.name


# static class
class GlobalManager:
    files = {}
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
