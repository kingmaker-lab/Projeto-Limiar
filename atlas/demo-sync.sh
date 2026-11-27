#!/bin/sh
set -eu
umask 077
binary=${1:?uso: sh demo-sync.sh /caminho/atlas}
work=$(mktemp -d)
pid=
stop_peer() {
  if [ -n "$pid" ]; then
    kill "$pid" 2>/dev/null || true
    wait "$pid" 2>/dev/null || true
    pid=
  fi
}
trap 'stop_peer; rm -rf -- "$work"' EXIT

source_dir="$work/source"
replica_dir="$work/replica"
start_peer() {
  : > "$work/address"
  "$binary" -dir "$source_dir" serve 0 >> "$work/address" &
  pid=$!
  attempt=0
  while [ ! -s "$work/address" ]; do
    if ! kill -0 "$pid" 2>/dev/null || [ "$attempt" -ge 100 ]; then
      echo 'Servidor local indisponível' >&2
      exit 1
    fi
    attempt=$((attempt + 1))
    sleep 0.05
  done
  read -r address < "$work/address"
  port=${address#127.0.0.1:}
}

alice=$("$binary" wallet "$work/alice.pem")
bob=$("$binary" wallet "$work/bob.pem")
"$binary" -dir "$source_dir" init
"$binary" -dir "$source_dir" mine "$alice" >/dev/null
source_status=$("$binary" -dir "$source_dir" status)
network=$(printf '%s\n' "$source_status" | sed -n 's/^{"network":"\([a-f0-9]*\)".*/\1/p')
start_peer
first=$("$binary" -dir "$replica_dir" sync "$port" "$network")
[ "$first" = "$source_status" ]
stop_peer

"$binary" -dir "$source_dir" sign "$work/alice.pem" "$bob" 17 > "$work/transfer.json"
"$binary" -dir "$source_dir" mine "$alice" "$work/transfer.json" >/dev/null
start_peer
"$binary" -dir "$replica_dir" sync "$port" "$network" >/dev/null
source_status=$("$binary" -dir "$source_dir" status)
replica_status=$("$binary" -dir "$replica_dir" status)
[ "$source_status" = "$replica_status" ]
cmp "$source_dir/ledger.json" "$replica_dir/ledger.json"
printf '%s\n' "$replica_status" | grep -Fq '"height":2'
printf '%s\n' "$replica_status" | grep -Fq '"supply":100'
printf '%s\n' "$replica_status" | grep -Fq "\"$bob\":{\"balance\":17,\"nonce\":0}"
printf '%s\n' "$replica_status"
