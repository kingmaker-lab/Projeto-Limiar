#!/usr/bin/env bash
set -euo pipefail

work=$(mktemp -d)
trap 'rm -rf -- "$work"' EXIT
mkdir "$work/a" "$work/b"
name=$'linha\nquebrada'
printf 'conteúdo\n' > "$work/a/$name"
printf 'outro\n' > "$work/a/-teste"
cp -a "$work/a/." "$work/b/"
ln -s ./-teste "$work/a/link"
bash inventory.sh "$work/a" > "$work/first"
bash inventory.sh "$work/b" > "$work/second"
cmp "$work/first" "$work/second"
mapfile -d '' -t records < "$work/first"
[[ ${#records[@]} == 2 ]]
digest=$(sha256sum < "$work/a/$name")
[[ ${records[1]} == "${digest%% *}  ./$name" ]]
printf x >> "$work/b/$name"
bash inventory.sh "$work/b" > "$work/second"
if cmp -s "$work/first" "$work/second"; then exit 1; fi
if bash inventory.sh "$work/missing" 2>/dev/null; then exit 1; fi
