"""Verify a synthetic evidence file and reconstruct its timeline."""

import hashlib
import json
import re
from datetime import datetime


TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def inspect_evidence(sample, expected_sha256):
    if re.fullmatch(r"[0-9a-f]{64}", expected_sha256) is None:
        raise ValueError("referência SHA-256 inválida")

    observed_sha256 = hashlib.sha256(sample).hexdigest()
    integrity_ok = observed_sha256 == expected_sha256
    evidence = {
        "expected_sha256": expected_sha256,
        "observed_sha256": observed_sha256,
        "integrity_ok": integrity_ok,
    }
    if not integrity_ok:
        return evidence

    events = []
    seen = set()
    for number, line in enumerate(sample.decode("utf-8").splitlines(), start=1):
        try:
            event = json.loads(line)
            if (
                not isinstance(event, dict)
                or set(event) != {"id", "timestamp", "action"}
                or any(not isinstance(value, str) or not value.strip() for value in event.values())
            ):
                raise ValueError("evento fora do contrato")
            timestamp = event["timestamp"]
            if datetime.strptime(timestamp, TIMESTAMP_FORMAT).strftime(TIMESTAMP_FORMAT) != timestamp:
                raise ValueError("data fora do formato UTC esperado")
            if event["id"] in seen:
                raise ValueError("identificador duplicado")
        except ValueError as exc:
            raise ValueError(f"linha {number}: {exc}") from exc
        seen.add(event["id"])
        events.append(event)

    if not events:
        raise ValueError("amostra sem eventos")

    evidence["timeline"] = sorted(events, key=lambda event: (event["timestamp"], event["id"]))
    return evidence
