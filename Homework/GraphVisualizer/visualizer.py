import argparse
from os import PathLike


def print_tree(node, graph, prefix='', is_last=True, depth=0, max_depth=None):
    if max_depth is not None and depth > max_depth:
        return
    connector = '└── ' if is_last else '├── '
    print(prefix + connector + node)
    children = graph.get(node, [])
    for i, child in enumerate(children):
        is_last_child = (i == len(children) - 1)
        if is_last:
            new_prefix = prefix + '    '
        else:
            new_prefix = prefix + '│   '
        print_tree(child, graph, new_prefix, is_last_child, depth=depth + 1, max_depth=max_depth)


def main(dependencies_path: PathLike, max_depth: int):
    try:
        with open(dependencies_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        edges = []
        nodes = set()

        for line in lines:
            line = line.strip()
            if '-->' in line:
                parts = line.split('-->')
                src = parts[0].strip('[] ')
                dst = parts[1].strip('[] ')
                edges.append((src, dst))
                nodes.update([src, dst])
            elif line.startswith('[') and line.endswith(']'):
                node = line.strip('[] ')
                nodes.add(node)

        graph = {node: [] for node in nodes}
        for src, dst in edges:
            graph[src].append(dst)

        all_nodes = set(graph.keys())
        dest_nodes = set(dst for src, dst in edges)
        root_nodes = all_nodes - dest_nodes

        for root in root_nodes:
            print_tree(root, graph, depth=0, max_depth=max_depth)

    except FileNotFoundError:
        print(f"Файл по пути {dependencies_path} не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Программа для визуализации графов")
    parser.add_argument(
        "dependencies_path",
        help="Путь к файлу, в котором хранится граф в формате PlantUML")
    parser.add_argument(
        "max_depth",
        help="Максимальная глубина анализа зависимостей",
        type=int)
    args = parser.parse_args()

    main(args.dependencies_path, args.max_depth)
