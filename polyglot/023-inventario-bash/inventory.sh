#!/usr/bin/env bash
set -euo pipefail

if [[ $# != 1 || ! -d "$1" ]]; then
    printf 'Uso: bash inventory.sh DIRETORIO\n' >&2
    exit 2
fi

export LC_ALL=C
unset CDPATH
(
    cd -- "$1/"
    find . -type f -print0 |
        sort -z |
        xargs -0 -r sha256sum --zero --
)
