import argparse
from os import PathLike
from collections import defaultdict


def main(dependencies_path: PathLike):
    levels = []

    try:
        pass

    except FileNotFoundError:
        print(f"Файл по пути {dependencies_path} не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Программа для визуализации графов")
    parser.add_argument("dependencies_path", help="Путь к файлу, в котором хранится граф в формате PlantUML")
    args = parser.parse_args()

    main(args.dependencies_path)
