import json
from pathlib import Path
import subprocess
import sys
import unittest

from endpoints import read_endpoints

HERE = Path(__file__).resolve().parent


class EndpointTest(unittest.TestCase):
    def test_cli(self):
        result = subprocess.run(
            [sys.executable, str(HERE / "endpoints.py"),
             str(HERE / "openapi.exemplo.json"), "--format", "json"],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["operations"], [
            {"method": "GET", "path": "/rascunhos"},
            {"method": "POST", "path": "/rascunhos"},
            {"method": "GET", "path": "/rascunhos/{id}"},
        ])

    def test_references_and_metadata(self):
        inventory = read_endpoints({
            "openapi": "3.0.3",
            "servers": [{"url": "https://example.com"}],
            "paths": {
                "x-notes": "metadado",
                "/ext": {"$ref": "https://example.com/routes.json"},
                "/local": {"parameters": [], "head": {}},
            },
        })
        self.assertEqual(inventory["operations"], [{"method": "HEAD", "path": "/local"}])
        self.assertEqual(inventory["paths_with_unresolved_refs"], ["/ext"])

    def test_invalid_document(self):
        for document in (
            {"swagger": "2.0"},
            {"openapi": "3.1.0", "paths": []},
            {"openapi": "3.1.0", "paths": {"/ok\nGET /fake": {}}},
            {"openapi": "3.1.0", "paths": {"/rota": {"get": None}}},
        ):
            with self.subTest(document=document), self.assertRaises(ValueError):
                read_endpoints(document)


if __name__ == "__main__":
    unittest.main()
