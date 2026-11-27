#!/bin/sh
# Executa a prática do Caderno usando apenas os arquivos incluídos no kit.
set -eu

if [ "$#" -gt 1 ]; then
    printf '%s\n' 'Uso: sh pratica.sh [pasta-de-saida-existente]' >&2
    exit 2
fi

kit_dir=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
output_parent=$(CDPATH='' cd -- "${1:-.}" && pwd)
output=$(mktemp -d "$output_parent/caderno-pratica.XXXXXX")
umask 077

cd "$kit_dir"
python3 recon.py --scope escopo.exemplo.txt --urls urls.exemplo.txt --format markdown \
    > "$output/caderno.md"
python3 endpoints.py openapi.exemplo.json --format json > "$output/endpoints.json"
python3 kit.py diff-escopo escopo.exemplo.txt exemplos/escopo-revisado.txt \
    > "$output/mudancas-escopo.json"
python3 kit.py diff-api openapi.exemplo.json exemplos/openapi-revisada.json \
    > "$output/mudancas-api.json"
python3 kit.py revisar-cabecalhos exemplos/resposta-http.txt > "$output/revisao-http.json"
python3 kit.py resumo-cabecalhos exemplos/resposta-http.txt > "$output/resumo-http.json"
python3 kit.py hash-evidencia exemplos/resposta-http.txt > "$output/impressao.json"
digest=$(python3 -c 'import json, sys; print(json.load(sys.stdin)["sha256"])' < "$output/impressao.json")
cp exemplos/resposta-http.txt "$output/resposta-ficticia.txt"
python3 kit.py verificar-evidencia "$output/resposta-ficticia.txt" "$digest" \
    > "$output/verificacao.json"
python3 kit.py linha-do-tempo exemplos/eventos.csv > "$output/eventos.json"
python3 kit.py rascunho exemplos/ficha.json > "$output/relatorio.md"

printf '%s\n' "$output"
