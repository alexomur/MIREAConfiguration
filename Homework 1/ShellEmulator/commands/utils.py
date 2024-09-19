import os
import __main__ as main


def resolve_path(path: str) -> tuple[str, str] or None:
    """
    Resolves the given virtual path and checks if it exists in the real file system.

    :param path: The virtual path to a file or directory, which can be either relative or absolute.
    :return: A tuple (virtual_path, real_path) if the path exists, otherwise (None, None).
    """
    if not os.path.isabs(path):
        virtual_path = os.path.normpath(os.path.join(main.current_path, path)).replace(os.sep, "/")
    else:
        virtual_path = os.path.normpath(path).replace(os.sep, "/")

    real_path = os.path.join(main.global_path, virtual_path.lstrip("/").replace("/", os.sep))

    if os.path.exists(real_path):  # Проверяем существование файла или директории
        return virtual_path, real_path

    return None, None
