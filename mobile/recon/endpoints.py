"""Lista operações declaradas em um documento OpenAPI JSON local."""

import argparse
import json
from pathlib import Path
import re
import sys

HTTP_METHODS = ("get", "head", "options", "trace", "post", "put", "patch", "delete")
VERSIONS = re.compile(r"3\.[01]\.\d+", re.ASCII)


def read_endpoints(document):
    if not isinstance(document, dict):
        raise ValueError("esperado um objeto OpenAPI")
    version = document.get("openapi")
    if not isinstance(version, str) or not VERSIONS.fullmatch(version):
        raise ValueError("esperado um documento OpenAPI 3.0 ou 3.1")
    paths = document.get("paths", {})
    if not isinstance(paths, dict):
        raise ValueError("paths deve ser um objeto")

    operations = []
    unresolved = []
    for route, path_item in sorted(paths.items()):
        if route.startswith("x-"):
            continue
        if not route.startswith("/") or any(c.isspace() or not c.isprintable() for c in route):
            raise ValueError("rota inválida em paths")
        if not isinstance(path_item, dict):
            raise ValueError("esperado um objeto por rota")
        if "$ref" in path_item:
            unresolved.append(route)
        for method in HTTP_METHODS:
            if method not in path_item:
                continue
            if not isinstance(path_item[method], dict):
                raise ValueError("esperado um objeto por operação HTTP")
            operations.append({"method": method.upper(), "path": route})
    return {
        "schema": 1,
        "openapi": version,
        "operations": operations,
        "paths_with_unresolved_refs": unresolved,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("document", type=Path, help="caminho do arquivo OpenAPI JSON")
    parser.add_argument("--format", choices=("text", "json"), default="text",
                        help="formato de saída (padrão: text)")
    args = parser.parse_args()

    try:
        with args.document.open(encoding="utf-8") as source:
            inventory = read_endpoints(json.load(source))
    except (OSError, ValueError, RecursionError) as exc:
        print(f"endpoints: {exc}", file=sys.stderr)
        return 2

    if args.format == "json":
        print(json.dumps(inventory, indent=2))
    else:
        for operation in inventory["operations"]:
            print(f'{operation["method"]:7} {operation["path"]}')
        for route in inventory["paths_with_unresolved_refs"]:
            print(f"Referência não expandida: {route}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
