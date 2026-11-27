#!/usr/bin/env bash
set -euo pipefail

experiment=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
polyglot=$(cd -- "$experiment/../.." && pwd)
work=$(mktemp -d)
hermes_pid=

stop_hermes() {
    if [[ -n "$hermes_pid" ]]; then
        kill "$hermes_pid" 2>/dev/null || true
        wait "$hermes_pid" 2>/dev/null || true
        hermes_pid=
    fi
}

cleanup() {
    stop_hermes
    rm -rf -- "$work"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

start_hermes() {
    "$work/hermes" -port 0 -file "$work/messages.json" > "$work/endpoint" 2> "$work/hermes.log" &
    hermes_pid=$!
    for ((attempt = 0; attempt < 100; attempt++)); do
        if [[ -s "$work/endpoint" ]] && IFS= read -r endpoint < "$work/endpoint" &&
            [[ "$endpoint" =~ ^http://127\.0\.0\.1:[0-9]+$ ]]; then
            return
        fi
        if ! kill -0 "$hermes_pid" 2>/dev/null; then
            break
        fi
        sleep 0.05
    done
    cat "$work/hermes.log" >&2
    echo "Hermes não anunciou um endereço de loopback." >&2
    return 1
}

http() {
    curl --noproxy '*' --fail --silent --show-error --max-time 5 "$@"
}

measure() {
    local label=$1
    shift
    env time -q -f "$label elapsed_s=%e peak_rss_kib=%M" -o "$work/metrics" -a "$@"
}

(cd "$polyglot/004-hermes-go" && go build -buildvcs=false -o "$work/hermes" .)
cargo build --manifest-path "$polyglot/003-aegis-rust/Cargo.toml" --locked --offline --target-dir "$work/rust"
aegis="$work/rust/debug/aegis"
report="$work/report.json"

measure gaia python3 -B "$polyglot/015-gaia-python/main.py" "$experiment/sample.csv" --baseline 2024 > "$report"
python3 -B "$polyglot/015-gaia-python/main.py" "$experiment/sample.csv" --baseline 2024 > "$work/repeated.json"
cmp "$report" "$work/repeated.json"
jq -e --slurpfile expected "$experiment/expected-report.json" '. == $expected[0]' "$report" > /dev/null

digest=$(measure aegis_hash "$aegis" hash "$report")
[[ "$digest" =~ ^[a-f0-9]{64}$ ]]
event=$(jq -ce --arg sha256 "$digest" '
    keys | {
        version: 1, type: "climate.report.published", report_id: "gaia-monthly-sample",
        period: {from: first, through: last}, sha256: $sha256
    }
' "$report")

start_hermes
receipt=$(http -H 'Content-Type: application/json' --data-binary "$(jq -cn --arg text "$event" '{text: $text}')" "$endpoint/messages")
jq -e --arg text "$event" '. == {id: 1, text: $text}' <<< "$receipt" > /dev/null
stop_hermes

start_hermes
restored=$(http "$endpoint/messages?after=0")
jq -e --argjson receipt "$receipt" '. == [$receipt]' <<< "$restored" > /dev/null
restored_digest=$(jq -er '.[0].text | fromjson | select(.version == 1 and .type == "climate.report.published") | .sha256' <<< "$restored")
measure aegis_clean "$aegis" check "$report" "$restored_digest" > "$work/clean.log"
grep -q ' status=ok$' "$work/clean.log"

# Troca a quebra de linha depois de "{" por um espaço. O JSON conserva o mesmo valor.
printf ' ' | dd of="$report" bs=1 seek=1 conv=notrunc status=none
jq -e --slurpfile expected "$experiment/expected-report.json" '. == $expected[0]' "$report" > /dev/null
status=0
measure aegis_changed "$aegis" check "$report" "$restored_digest" > "$work/changed.log" || status=$?
[[ "$status" == 1 ]]
grep -q ' status=changed$' "$work/changed.log"

printf 'Evento recuperado após reinício: %s\n' "$event"
printf 'Detecção confirmada após alterar um byte do relatório.\n'
printf 'report_bytes=%s snapshot_bytes=%s\n' "$(stat -c %s "$report")" "$(stat -c %s "$work/messages.json")"
awk '/^VmHWM:/ {print "hermes peak_rss_kib=" $2}' "/proc/$hermes_pid/status"
cat "$work/metrics"
