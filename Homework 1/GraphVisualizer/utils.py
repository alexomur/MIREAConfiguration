import json, os

def read_json_file(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

def get_dependencies(package_json):
    return package_json.get("dependencies", {})

def get_transitive_dependencies(package_path, dependencies, max_depth, current_depth=1):
    graph = {}

    if current_depth > max_depth:
        return graph

    for dep in dependencies:
        dep_path = os.path.join(package_path, 'node_modules', dep, 'package.json')
        if os.path.exists(dep_path):
            dep_package_json = read_json_file(dep_path)
            dep_deps = get_dependencies(dep_package_json)
            graph[dep] = list(dep_deps.keys())
            graph.update(get_transitive_dependencies(package_path, dep_deps, max_depth, current_depth + 1))
    return graph

def generate_plantuml(graph):
    lines = ["@startuml"]
    for package, deps in graph.items():
        lines.append(f"[{package}]")
        for dep in deps:
            lines.append(f"[{package}] --> [{dep}]")
    lines.append("@enduml")
    return "\n".join(lines)

def save_plantuml(plantuml_diagram, output_file):
    with open(output_file, 'w') as file:
        file.write(plantuml_diagram)

__all__ = ["read_json_file", "get_dependencies", "get_transitive_dependencies", "generate_plantuml", "save_plantuml"]
