import argparse
import os
import subprocess
from os import PathLike
from utils import *

def main(lockfile_path: PathLike, plantuml_path: PathLike, max_depth: int):
    lockfile_json = read_json_file(lockfile_path)

    package_name = lockfile_json.get("name", "root")

    dependencies = get_dependencies_from_lockfile(lockfile_json)

    graph = get_transitive_dependencies_from_lockfile(dependencies, lockfile_json, max_depth)

    plantuml_diagram = generate_plantuml(graph, package_name, max_depth)

    plantuml_file = "dependencies.txt"
    save_plantuml(plantuml_diagram, plantuml_file)

    try:
        if not plantuml_path or not os.path.exists(plantuml_path):
            raise FileNotFoundError(f"Файл {plantuml_path} не найден или путь не указан.")
        subprocess.run(["python", plantuml_path, plantuml_file])
    except Exception as e:
        print(f"Невозможно запустить программу для визуализации графа. Подробнее:\n{e}\n\nЗависимости в формате PlantUML:\n{plantuml_diagram}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Инструмент для визуализации графа зависимостей JavaScript (npm).")

    parser.add_argument(
        "-l",
        "--lockfile_path",
        help="Путь к файлу package-lock.json",
        required=False,
        default="package-lock.json")
    parser.add_argument(
        "-u",
        "--plantuml_path",
        help="Путь к программе для визуализации",
        required=False,
        default="None") # replace with visualizer.py on release
    parser.add_argument(
        "-d",
        "--max_depth",
        help="Максимальная глубина анализа зависимостей",
        type=int,
        required=False,
        default=2)

    args = parser.parse_args()
    main(args.lockfile_path, args.plantuml_path, args.max_depth)
