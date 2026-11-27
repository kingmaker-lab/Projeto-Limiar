import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent


class EntregaTest(unittest.TestCase):
    def run_command(self, *parts):
        return subprocess.run(
            [sys.executable, str(HERE / "entrega.py"), *map(str, parts)],
            capture_output=True, text=True,
        )

    def test_creation_and_verification(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            report = root / "relatório.md"
            report.write_bytes(b"relato de teste\n")
            summary = root / "resumo.json"
            summary.write_bytes(b"{}\n")
            destination = root / "pasta de entrega"
            result = self.run_command("criar", destination, report, summary)
            self.assertEqual(result.returncode, 0, result.stderr)
            result = self.run_command("verificar", destination)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout), {
                "ausentes": [], "extras": [], "divergentes": [],
            })

            (destination / report.name).write_bytes(b"texto alterado")
            (destination / summary.name).unlink()
            (destination / "extra.txt").touch()
            result = self.run_command("verificar", destination)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertEqual(json.loads(result.stdout), {
                "ausentes": [summary.name], "extras": ["extra.txt"],
                "divergentes": [report.name],
            })
            self.assertEqual(self.run_command("criar", destination, report).returncode, 2)
            self.assertEqual((destination / report.name).read_bytes(), b"texto alterado")

    def test_rejects_symlinks_and_unsafe_manifest_names(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "original.txt"
            source.touch()
            link = root / "atalho.txt"
            link.symlink_to(source)
            destination = root / "entrega"
            self.assertEqual(self.run_command("criar", destination, link).returncode, 2)
            self.assertFalse(destination.exists())
            self.assertEqual(self.run_command("criar", destination, source).returncode, 0)
            manifest = destination / "manifesto.json"
            data = json.loads(manifest.read_text())
            data["arquivos"][0]["nome"] = "../original.txt"
            manifest.write_text(json.dumps(data))
            self.assertEqual(self.run_command("verificar", destination).returncode, 2)
