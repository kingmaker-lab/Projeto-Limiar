#!/bin/sh
# A saída é JSONL. Cada configuração tem cinco amostras por padrão.
set -eu
pulse=${1:-./PULSE/build/pulse}
repeat=${2:-5}
workers=${3:-4}

"$pulse" bench --repeat "$repeat" --tasks 96 --words 262144 --workers 1
"$pulse" bench --repeat "$repeat" --tasks 96 --words 262144 --workers "$workers"
"$pulse" bench --repeat "$repeat" --tasks 96 --words 262144 --workers "$workers" --target-ms 2
