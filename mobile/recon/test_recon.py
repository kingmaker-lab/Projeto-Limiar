import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from recon import origin

HERE = Path(__file__).resolve().parent


class ReconTest(unittest.TestCase):
    def run_cli(self, scope):
        return subprocess.run(
            [sys.executable, str(HERE / "recon.py"), "--scope", str(scope),
             "--urls", str(HERE / "urls.exemplo.txt")],
            capture_output=True, text=True,
        )

    def test_inventory(self):
        result = self.run_cli(HERE / "escopo.exemplo.txt")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {
            "schema": 1,
            "matched": ["https://api.example.com:8443", "https://app.example.com"],
            "unmatched": ["http://app.example.com", "https://cdn.app.example.com"],
            "total_origins": 4,
        })
        self.assertNotIn("token", result.stdout)

    def test_invalid_scope(self):
        with tempfile.TemporaryDirectory() as temp:
            scope = Path(temp) / "scope.txt"
            for value in ("", "https://*.example.com", "https://example.com/private"):
                with self.subTest(value=value):
                    scope.write_text(value, encoding="utf-8")
                    result = self.run_cli(scope)
                    self.assertEqual(result.returncode, 2)
                    self.assertEqual(result.stdout, "")

    def test_origins(self):
        self.assertEqual(origin("https://[2001:0db8::1]:443/"), "https://[2001:db8::1]")
        for value in ("ftp://example.com", "https://user:pass@example.com/",
                      "https://example.com:65536", "https://[::1]extra"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                origin(value)


if __name__ == "__main__":
    unittest.main()
