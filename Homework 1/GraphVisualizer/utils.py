import json

def read_json_file(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

def get_dependencies_from_lockfile(lockfile):
    return lockfile.get("dependencies", {})

def get_transitive_dependencies_from_lockfile(dependencies, lockfile, max_depth, current_depth=1):
    graph = {}

    if current_depth > max_depth:
        return graph

    for dep_name, dep_info in dependencies.items():
        dep_deps = dep_info.get('requires', {})
        graph[dep_name] = list(dep_deps.keys()) if dep_deps else []
        if current_depth < max_depth and dep_deps:
            deeper_deps = {dep: lockfile['dependencies'].get(dep, {}) for dep in dep_deps}
            graph.update(get_transitive_dependencies_from_lockfile(deeper_deps, lockfile, max_depth, current_depth + 1))

    return graph

def generate_plantuml(graph, root_package, max_depth):
    lines = ["@startuml", f"[{root_package}]"]
    for package, deps in graph.items():
        if deps and max_depth > 0:
            lines.append(f"[{root_package}] --> [{package}]")
        for dep in deps:
            if max_depth > 1:
                lines.append(f"[{package}] --> [{dep}]")
    lines.append("@enduml")
    return "\n".join(lines)

def save_plantuml(plantuml_diagram, output_file):
    with open(output_file, 'w') as file:
        file.write(plantuml_diagram)

__all__ = ["read_json_file", "get_dependencies_from_lockfile", "get_transitive_dependencies_from_lockfile", "generate_plantuml", "save_plantuml"]
