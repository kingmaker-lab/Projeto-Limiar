"""Utilitários offline para revisar documentação e organizar evidências."""

import argparse
import csv
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re
import sys

from endpoints import read_endpoints
from recon import read_origins

HEADER_NAME = re.compile(r"[!#$%&'*+.^_`|~0-9A-Za-z-]+")
STATUS_LINE = re.compile(r"HTTP/(?:1\.[01]|[23](?:\.0)?) ([1-5][0-9]{2})(?: +.*)?")
REVIEW_HEADERS = (
    "cache-control", "content-security-policy", "content-type",
    "referrer-policy", "strict-transport-security", "x-content-type-options",
)
REPORT_FIELDS = {
    "titulo": "Título",
    "escopo": "Ativo e escopo",
    "ambiente": "Ambiente",
    "procedimento": "Procedimento autorizado",
    "esperado": "Resultado esperado",
    "observado": "Resultado observado",
    "impacto": "Impacto e condições",
    "evidencia": "Evidência mínima",
}


def load_json(path):
    with path.open(encoding="utf-8") as source:
        return json.load(source)


def compare(before, after):
    return {"adicionados": sorted(after - before), "removidos": sorted(before - after)}


def scope_diff(args):
    return compare(read_origins(args.antes, scope=True),
                   read_origins(args.depois, scope=True))


def api_diff(args):
    before = read_endpoints(load_json(args.antes))
    after = read_endpoints(load_json(args.depois))

    def operations(inventory):
        return {f'{item["method"]} {item["path"]}' for item in inventory["operations"]}

    result = compare(operations(before), operations(after))
    result["referencias_pendentes"] = {
        "antes": before["paths_with_unresolved_refs"],
        "depois": after["paths_with_unresolved_refs"],
    }
    return result


def read_headers(path):
    with path.open("rb") as source:
        status = STATUS_LINE.fullmatch(source.readline().rstrip(b"\r\n").decode("latin-1"))
        if not status:
            raise ValueError("esperada uma linha de status HTTP")
        names = []
        for line in source:
            line = line.rstrip(b"\r\n")
            if not line:
                break
            raw_name, sep, _ = line.partition(b":")
            name = raw_name.decode("latin-1")
            if not sep or not HEADER_NAME.fullmatch(name):
                raise ValueError("linha de cabeçalho inválida")
            names.append(name.lower())
    return int(status[1]), names


def review_headers(args):
    status, names = read_headers(args.arquivo)
    return {
        "status": status,
        "presentes": [name for name in REVIEW_HEADERS if name in names],
        "ausentes_na_captura": [name for name in REVIEW_HEADERS if name not in names],
    }


def share_headers(args):
    status, names = read_headers(args.arquivo)
    # Compartilha apenas nomes de uma lista fixa. Valores e corpo ficam fora.
    return {
        "status": status,
        "cabecalhos": {name: names.count(name) for name in REVIEW_HEADERS if name in names},
    }


def evidence_hash(args):
    digest = sha256()
    size = 0
    with args.arquivo.open("rb") as source:
        for block in iter(lambda: source.read(65536), b""):
            digest.update(block)
            size += len(block)
    return {"bytes": size, "sha256": digest.hexdigest()}


def verify_evidence(args):
    if not re.fullmatch(r"[0-9a-fA-F]{64}", args.sha256):
        raise ValueError("esperado um SHA-256 hexadecimal de 64 caracteres")
    result = evidence_hash(args)
    if result["sha256"] != args.sha256.lower():
        print("kit: SHA-256 diferente do esperado", file=sys.stderr)
        return 1
    return result


def timeline(args):
    events = []
    with args.arquivo.open(encoding="utf-8", newline="") as source:
        reader = csv.reader(source, strict=True)
        if next(reader, None) != ["quando", "evento"]:
            raise ValueError("esperado o cabeçalho CSV quando,evento")
        for row in reader:
            if len(row) != 2 or not row[1].strip():
                raise ValueError(f"CSV inválido na linha {reader.line_num}")
            when = datetime.fromisoformat(row[0].replace("Z", "+00:00"))
            if when.utcoffset() is None or "T" not in row[0]:
                raise ValueError(f"hora sem fuso explícito na linha {reader.line_num}")
            events.append((when.astimezone(timezone.utc), row[1]))
    return [{"quando_utc": when.isoformat(), "evento": event}
            for when, event in sorted(events, key=lambda entry: entry[0])]


def draft_report(args):
    evidence = load_json(args.arquivo)
    if not isinstance(evidence, dict) or any(key not in REPORT_FIELDS for key in evidence):
        raise ValueError("esperado um objeto com os campos do exemplo de relatório")
    for key, value in evidence.items():
        if not isinstance(value, str):
            raise ValueError(f"o campo {key} deve ser texto")

    lines = ["# Relatório em revisão"]
    for key, label in REPORT_FIELDS.items():
        value = evidence.get(key, "").strip()
        lines.extend(["", f"## {label}", "", value or "[A preencher]"])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(required=True, dest="command")
    for name, run, description in (
        ("diff-escopo", scope_diff, "mostra origens adicionadas e removidas"),
        ("diff-api", api_diff, "compara operações de dois contratos OpenAPI"),
        ("revisar-cabecalhos", review_headers, "confere presença de cabeçalhos em uma captura"),
        ("resumo-cabecalhos", share_headers, "produz um resumo sem valores ou corpo"),
        ("hash-evidencia", evidence_hash, "calcula o SHA-256 de um arquivo local"),
        ("verificar-evidencia", verify_evidence, "confere o SHA-256 de um arquivo local"),
        ("linha-do-tempo", timeline, "ordena eventos de um CSV e normaliza o fuso"),
        ("rascunho", draft_report, "transforma uma ficha JSON em relatório Markdown"),
    ):
        command = commands.add_parser(name, help=description, description=description)
        command.set_defaults(run=run)
        if name.startswith("diff-"):
            command.add_argument("antes", type=Path)
            command.add_argument("depois", type=Path)
        else:
            command.add_argument("arquivo", type=Path)
        if run is verify_evidence:
            command.add_argument("sha256")

    args = parser.parse_args()
    try:
        result = args.run(args)
    except (OSError, ValueError, csv.Error, OverflowError, RecursionError) as exc:
        print(f"kit: {exc}", file=sys.stderr)
        return 2
    if isinstance(result, int):
        return result
    print(result if isinstance(result, str) else json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
