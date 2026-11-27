import json
from pathlib import Path
import subprocess
import tempfile
import unittest

HERE = Path(__file__).resolve().parent


class PraticaTest(unittest.TestCase):
    def test_runs_from_another_directory_and_preserves_existing_results(self):
        with tempfile.TemporaryDirectory(prefix="limiar prática ") as temp:
            parent = Path(temp)
            generated = []
            for _ in range(2):
                result = subprocess.run(
                    ["sh", str(HERE / "pratica.sh")], cwd=parent,
                    capture_output=True, text=True,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                output = Path(result.stdout.strip())
                self.assertEqual(output.parent, parent)
                generated.append(output)

            first, second = generated
            self.assertNotEqual(first, second)
            self.assertEqual({path.name for path in first.iterdir()}, {
                "caderno.md", "endpoints.json", "mudancas-escopo.json",
                "mudancas-api.json", "revisao-http.json", "resumo-http.json",
                "impressao.json", "resposta-ficticia.txt", "verificacao.json",
                "eventos.json", "relatorio.md",
            })
            self.assertEqual(
                json.loads((first / "impressao.json").read_text()),
                json.loads((first / "verificacao.json").read_text()),
            )
            self.assertIn("Caso C2", (first / "relatorio.md").read_text())
