"""Replay the versioned synthetic policy events."""

import json
from pathlib import Path


def summarize(lines):
    event_ids = set()
    alerts = []
    for line_number, line in enumerate(lines, start=1):
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"linha {line_number}: JSON inválido") from exc
        if (
            not isinstance(event, dict)
            or set(event) != {"id", "action", "outcome"}
            or not isinstance(event["id"], str)
            or not event["id"].strip()
            or event["action"] != "policy_change"
            or event["outcome"] not in ("accepted", "rejected")
        ):
            raise ValueError(f"linha {line_number}: evento fora do contrato")
        event_id = event["id"]
        if event_id in event_ids:
            raise ValueError(f"linha {line_number}: identificador duplicado")
        event_ids.add(event_id)
        if event["outcome"] == "rejected":
            alerts.append(event_id)
    if not event_ids:
        raise ValueError("amostra sem eventos")
    return {"events": len(event_ids), "alerts": alerts}


if __name__ == "__main__":
    try:
        with Path(__file__).with_name("events.jsonl").open(encoding="utf-8") as fixture:
            result = summarize(fixture)
    except (OSError, ValueError) as exc:
        raise SystemExit(f"TARTARUS: {exc}") from exc
    print(json.dumps(result))
