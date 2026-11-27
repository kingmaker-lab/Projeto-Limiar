#!/bin/sh
set -eu
umask 077
binary=${1:?uso: sh demo.sh /caminho/atlas}
work=$(mktemp -d)
trap 'rm -rf -- "$work"' EXIT
ledger="$work/ledger"
alice=$("$binary" wallet "$work/alice.pem")
bob=$("$binary" wallet "$work/bob.pem")
"$binary" -dir "$ledger" init
"$binary" -dir "$ledger" mine "$alice" >/dev/null
"$binary" -dir "$ledger" sign "$work/alice.pem" "$bob" 17 > "$work/transfer.json"
"$binary" -dir "$ledger" mine "$alice" "$work/transfer.json" >/dev/null
if "$binary" -dir "$ledger" mine "$alice" "$work/transfer.json" 2>"$work/replay.err"; then
  echo 'Replay aceito' >&2
  exit 1
fi
grep -qx 'nonce incorreto' "$work/replay.err"
status=$("$binary" -dir "$ledger" status)
printf '%s\n' "$status" | grep -Fq '"height":2'
printf '%s\n' "$status" | grep -Fq '"supply":100'
printf '%s\n' "$status" | grep -Fq "\"$alice\":{\"balance\":83,\"nonce\":1}"
printf '%s\n' "$status" | grep -Fq "\"$bob\":{\"balance\":17,\"nonce\":0}"
printf '%s\n' "$status"
