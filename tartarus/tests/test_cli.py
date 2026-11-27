import json
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from run import main

ROOT = Path(__file__).resolve().parents[1]


class ExperimentCliTests(unittest.TestCase):
    def cli(self, *args):
        return subprocess.run(
            [sys.executable, "-B", str(ROOT / "run.py"), *args],
            capture_output=True,
            text=True,
        )

    def test_full_report(self):
        result = self.cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["schema_version"], 1)
        self.assertTrue(report["passed"])
        self.assertEqual(
            [item["id"] for item in report["experiments"]],
            ["TAR-001", "TAR-002", "TAR-003", "TAR-004", "TAR-007", "TAR-008"],
        )
        self.assertEqual(report["experiments"][-1]["evidence"]["alerts"], ["sample-002"])

    def test_single_experiment(self):
        result = self.cli("TAR-004")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual([item["id"] for item in report["experiments"]], ["TAR-004"])

    def test_unknown_experiment(self):
        self.assertEqual(self.cli("TAR-999").returncode, 2)

    def test_regression_status(self):
        with patch("sys.argv", ["run.py", "TAR-001"]), patch("builtins.print"), patch(
            "run.CONTROLS", {"TAR-001": lambda _: True}
        ):
            self.assertEqual(main(), 1)
