import zipfile
import os
from commands import utils


def extract_zip(path):
    with zipfile.ZipFile(path, "r") as zip_f:
        for file_info in zip_f.infolist():
            name = file_info.filename
            if file_info.is_dir():
                # Добавляем директорию
                utils.GlobalManager.add_file(name, "")
            else:
                # Добавляем файл
                utils.GlobalManager.add_file(name, zip_f.read(name))

                # Добавляем все родительские директории
                parent = os.path.dirname(name) + '/'
                while parent != '/':
                    if parent not in utils.GlobalManager.files:
                        utils.GlobalManager.add_file(parent, "")
                    parent = os.path.dirname(parent[:-1]) + '/'  # Удаляем последний '/' перед dirname
