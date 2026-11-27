"""Prepara e verifica uma pasta local de entrega de evidências."""

import argparse
import json
from pathlib import Path
import re
import shutil
import sys

from kit import file_digest

MANIFEST = "manifesto.json"
DIGEST = re.compile("[0-9a-f]{64}")


def valid_name(name):
    return (isinstance(name, str) and name not in {"", ".", "..", MANIFEST}
            and "/" not in name and "\\" not in name
            and all(character.isprintable() for character in name))


def regular_file(path):
    return not path.is_symlink() and path.is_file()


def create(destination, sources):
    names = [source.name for source in sources]
    if len(set(names)) != len(names):
        raise ValueError("arquivos de origem com nomes repetidos")
    if any(not valid_name(source.name) or not regular_file(source) for source in sources):
        raise ValueError("cada origem deve ser um arquivo regular com nome válido")

    destination.mkdir(mode=0o700)
    try:
        entries = []
        for source in sorted(sources, key=lambda path: path.name):
            target = destination / source.name
            with target.open("xb") as output, source.open("rb") as input_file:
                shutil.copyfileobj(input_file, output, length=65536)
            entries.append({"nome": source.name, **file_digest(target)})
        data = {"schema": 1, "arquivos": entries}
        (destination / MANIFEST).write_text(
            json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    except BaseException:
        shutil.rmtree(destination)
        raise
    return {"arquivos": len(entries), "pasta": str(destination)}


def manifest_entries(path):
    if not regular_file(path):
        raise ValueError("manifesto ausente ou inválido")
    data = json.loads(path.read_text(encoding="utf-8"))
    if (not isinstance(data, dict) or type(data.get("schema")) is not int
            or data["schema"] != 1 or not isinstance(data.get("arquivos"), list)
            or not data["arquivos"]):
        raise ValueError("formato de manifesto inválido")

    entries = {}
    for entry in data["arquivos"]:
        if not isinstance(entry, dict) or entry.keys() != {"nome", "bytes", "sha256"}:
            raise ValueError("entrada inválida no manifesto")
        name, size, digest = entry["nome"], entry["bytes"], entry["sha256"]
        if not valid_name(name) or name in entries or type(size) is not int or size < 0:
            raise ValueError("nome repetido, nome inválido ou tamanho inválido")
        if not isinstance(digest, str) or not DIGEST.fullmatch(digest):
            raise ValueError("SHA-256 inválido no manifesto")
        entries[name] = {"bytes": size, "sha256": digest}
    return entries


def verify(directory):
    if directory.is_symlink():
        raise ValueError("informe a pasta de entrega diretamente")
    expected = manifest_entries(directory / MANIFEST)
    present = {path.name: path for path in directory.iterdir() if path.name != MANIFEST}
    return {
        "ausentes": sorted(expected.keys() - present.keys()),
        "extras": sorted(present.keys() - expected.keys()),
        "divergentes": sorted(
            name for name in expected.keys() & present.keys()
            if not regular_file(present[name]) or file_digest(present[name]) != expected[name]
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    make = commands.add_parser("criar", help="copia arquivos escolhidos para uma pasta nova")
    make.add_argument("pasta", type=Path)
    make.add_argument("arquivos", nargs="+", type=Path)
    check = commands.add_parser("verificar", help="compara a pasta com o manifesto")
    check.add_argument("pasta", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "criar":
            result = create(args.pasta, args.arquivos)
            code = 0
        else:
            result = verify(args.pasta)
            code = int(any(result.values()))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return code
    except (OSError, ValueError, RecursionError) as exc:
        print(f"entrega: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
