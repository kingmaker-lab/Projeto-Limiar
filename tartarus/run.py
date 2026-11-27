"""Run the offline TARTARUS controls against versioned scenarios."""

import argparse
import json
from pathlib import Path

from controls import CONTROLS
from hecate import inspect_evidence
from telemetry.replay import summarize

ROOT = Path(__file__).resolve().parent


def run_experiment(experiment):
    if experiment == "TAR-006":
        directory = ROOT / "digital-forensics"
        evidence = inspect_evidence(
            (directory / "events.jsonl").read_bytes(),
            (directory / "events.sha256").read_text(encoding="ascii").strip(),
        )
        return {"id": experiment, "passed": evidence["integrity_ok"], "evidence": evidence}

    if experiment == "TAR-008":
        with (ROOT / "telemetry/events.jsonl").open(encoding="utf-8") as sample:
            evidence = summarize(sample)
        passed = evidence == {"events": 2, "alerts": ["sample-002"]}
        return {"id": experiment, "passed": passed, "evidence": evidence}

    check = CONTROLS[experiment]
    with (ROOT / "research/scenarios.json").open(encoding="utf-8") as source:
        scenarios = json.load(source)[experiment]
    if not (
        any(case["allowed"] is True for case in scenarios)
        and any(case["allowed"] is False for case in scenarios)
    ):
        raise ValueError(f"{experiment}: são necessários casos de aceitação e rejeição")

    cases = []
    for scenario in scenarios:
        allowed = check(scenario["input"])
        cases.append({
            "name": scenario["name"],
            "expected_allowed": scenario["allowed"],
            "observed_allowed": allowed,
            "passed": allowed is scenario["allowed"],
        })
    return {"id": experiment, "passed": all(case["passed"] for case in cases), "cases": cases}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    experiments = sorted((*CONTROLS, "TAR-006", "TAR-008"))
    parser.add_argument("experiment", nargs="?", default="all", choices=("all", *experiments))
    parser.add_argument("--list", action="store_true", help="listar experimentos executáveis")
    args = parser.parse_args()
    if args.list:
        print("\n".join(experiments))
        return 0

    selected = experiments if args.experiment == "all" else (args.experiment,)
    try:
        results = [run_experiment(experiment) for experiment in selected]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(2, f"TARTARUS: configuração inválida: {exc}\n")
    passed = all(result["passed"] for result in results)
    print(json.dumps({"schema_version": 1, "passed": passed, "experiments": results}, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
