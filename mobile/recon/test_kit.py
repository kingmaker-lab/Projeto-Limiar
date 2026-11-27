import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
CAPTURE = "exemplos/resposta-http.txt"


class KitTest(unittest.TestCase):
    def run_tool(self, *args):
        return subprocess.run(
            [sys.executable, "kit.py", *args], cwd=HERE,
            capture_output=True, text=True,
        )

    def get_output(self, *args):
        result = self.run_tool(*args)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def test_scope_diff(self):
        output = self.get_output("diff-escopo", "escopo.exemplo.txt",
                                 "exemplos/escopo-revisado.txt")
        self.assertEqual(json.loads(output), {
            "adicionados": ["https://docs.example.com"],
            "removidos": ["https://api.example.com:8443"],
        })

    def test_api_diff(self):
        output = self.get_output("diff-api", "openapi.exemplo.json",
                                 "exemplos/openapi-revisada.json")
        self.assertEqual(json.loads(output), {
            "adicionados": ["GET /status"],
            "removidos": ["POST /rascunhos"],
            "referencias_pendentes": {"antes": [], "depois": []},
        })

    def test_header_review(self):
        output = json.loads(self.get_output("revisar-cabecalhos", CAPTURE))
        self.assertEqual(output["status"], 200)
        self.assertEqual(output["presentes"], ["cache-control", "content-type"])
        self.assertIn("content-security-policy", output["ausentes_na_captura"])

    def test_header_summary_discards_values_and_body(self):
        raw = self.get_output("resumo-cabecalhos", CAPTURE)
        self.assertEqual(json.loads(raw), {
            "status": 200, "cabecalhos": {"cache-control": 1, "content-type": 1},
        })
        for value in ("VALOR_FICTICIO", "CORPO_FICTICIO", "application/json", "set-cookie"):
            self.assertNotIn(value, raw)
        with tempfile.TemporaryDirectory() as temp:
            capture = Path(temp) / "response.http"
            capture.write_bytes(b"HTTP/2 200\r\nContent-Type: image/png\r\n\r\n\xff")
            output = self.get_output("resumo-cabecalhos", str(capture))
            self.assertEqual(json.loads(output)["cabecalhos"], {"content-type": 1})

    def test_hash_and_verification(self):
        with tempfile.TemporaryDirectory() as temp:
            evidence = Path(temp) / "evidence.txt"
            evidence.write_bytes(b"abc")
            digest = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
            self.assertEqual(json.loads(self.get_output("hash-evidencia", str(evidence))),
                             {"bytes": 3, "sha256": digest})
            self.get_output("verificar-evidencia", str(evidence), digest)
            evidence.write_bytes(b"xyz")
            mismatch = self.run_tool("verificar-evidencia", str(evidence), digest)
            self.assertEqual(mismatch.returncode, 1, mismatch.stderr)
            self.assertEqual(mismatch.stdout, "")
            self.assertEqual(self.run_tool("verificar-evidencia", str(evidence), "abc").returncode, 2)

    def test_timeline_orders_in_utc(self):
        output = self.get_output("linha-do-tempo", "exemplos/eventos.csv")
        self.assertEqual(json.loads(output), [
            {"quando_utc": "2026-11-27T12:03:00+00:00", "evento": "Política fictícia conferida"},
            {"quando_utc": "2026-11-27T12:18:00+00:00", "evento": "Rascunho revisado"},
        ])

    def test_report(self):
        output = self.get_output("rascunho", "exemplos/ficha.json")
        self.assertIn("## Resultado esperado", output)
        self.assertIn("## Resultado observado", output)
        self.assertIn("O arquivo da política registra permitir para C2.", output)

    def test_invalid_capture_timeline_and_report(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "input.txt"
            for command, content in (
                ("resumo-cabecalhos", "HTTP/1.1 200 OK\ninvalid\n"),
                ("linha-do-tempo", "quando,evento\n2026-11-27T12:03:00,Evento\n"),
                ("rascunho", '{"evidencia": 42}'),
            ):
                with self.subTest(command=command):
                    path.write_text(content, encoding="utf-8")
                    result = self.run_tool(command, str(path))
                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
