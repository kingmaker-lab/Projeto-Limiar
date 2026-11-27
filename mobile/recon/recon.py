"""Inventário offline de origens web para revisar o escopo de um programa."""

import argparse
import ipaddress
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

LABEL = re.compile(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", re.ASCII)


def origin(value, *, scope=False):
    if any(ch.isspace() or ord(ch) < 32 or ord(ch) == 127 for ch in value):
        raise ValueError("espaço ou caractere de controle")
    if "\\" in value:
        raise ValueError("barra invertida")
    url = urlsplit(value)
    if url.scheme not in {"http", "https"} or not url.hostname or "@" in url.netloc:
        raise ValueError("use HTTP(S) com host e sem credenciais")
    if scope and (url.path not in {"", "/"} or "?" in value or "#" in value):
        raise ValueError("o escopo aceita somente origens exatas")
    host = url.hostname.removesuffix(".")
    try:
        port = url.port
    except ValueError:
        raise ValueError("porta inválida") from None
    if port == 0 or url.netloc.endswith(":"):
        raise ValueError("porta inválida")
    if url.netloc.startswith("["):
        if not re.fullmatch(r"\[[0-9a-fA-F:.]+\](?::[0-9]+)?", url.netloc):
            raise ValueError("use um IPv6 entre colchetes")
        host = f"[{ipaddress.IPv6Address(host).compressed}]"
    else:
        host = host.encode("idna").decode("ascii").lower()
        if len(host) > 253 or not all(LABEL.fullmatch(label) for label in host.split(".")):
            raise ValueError("host inválido ou curinga")
    default_port = 443 if url.scheme == "https" else 80
    suffix = f":{port}" if port is not None and port != default_port else ""
    return f"{url.scheme}://{host}{suffix}"


def read_origins(path, *, scope=False):
    origins = set()
    with path.open(encoding="utf-8") as source:
        for line_number, line in enumerate(source, 1):
            value = line.strip()
            if not value or value.startswith("#"):
                continue
            try:
                origins.add(origin(value, scope=scope))
            except ValueError as exc:
                raise ValueError(f"{path}, linha {line_number}: {exc}") from None
    return origins


def markdown_inventory(matched, unmatched):
    lines = [
        "# Caderno de escopo",
        "",
        "- Programa e link da política:",
        "- Data da consulta:",
        "- Métodos permitidos e restrições:",
        "- Canal privado de envio:",
        "",
        "## Correspondem à lista",
        "",
    ]
    lines.extend([f"- [ ] `{item}`" for item in matched] or ["Nenhuma origem."])
    lines.extend(["", "## Sem correspondência na lista", ""])
    lines.extend([f"- [ ] `{item}`" for item in unmatched] or ["Nenhuma origem."])
    lines.extend([
        "",
        "## Registro de observação",
        "",
        "- Ativo e regra aplicável:",
        "- Comportamento esperado:",
        "- Comportamento observado:",
        "- Evidência mínima:",
        "- Impacto e condições:",
        "- Próxima ação:",
    ])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scope", required=True, type=Path, help="origens autorizadas")
    parser.add_argument("--urls", required=True, type=Path, help="URLs coletadas manualmente")
    parser.add_argument("--format", choices=("json", "markdown"), default="json",
                        help="formato do inventário (padrão: json)")
    args = parser.parse_args()

    try:
        scope = read_origins(args.scope, scope=True)
        if not scope:
            raise ValueError("o arquivo de escopo está vazio")
        origins = read_origins(args.urls)
    except (OSError, ValueError) as exc:
        print(f"recon: {exc}", file=sys.stderr)
        return 2

    matched = sorted(origins & scope)
    unmatched = sorted(origins - scope)
    if args.format == "markdown":
        print(markdown_inventory(matched, unmatched))
    else:
        print(json.dumps({
            "schema": 1,
            "matched": matched,
            "unmatched": unmatched,
            "total_origins": len(origins),
        }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
