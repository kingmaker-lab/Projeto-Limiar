import json
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class WitnessIntegration(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        directory = Path(temporary.name)
        self.db = directory / "state.sqlite"
        self.key = directory / "operator.key"
        self.anchor = directory / "anchor.json"
        self.old = directory / "old.sqlite"
        self.policy = directory / "policy.json"
        self.envelope = directory / "envelope.json"
        self.cli(self.db, "keygen")
        self.cli(self.db, "init")
        shutil.copyfile(self.db, self.old)

    def cli(self, db, *args):
        run = subprocess.run([sys.executable, "-m", "cerberus", "--key", self.key,
                              "--db", db, *args], cwd=ROOT, capture_output=True,
                             check=True, timeout=6)
        return json.loads(run.stdout)

    def apply(self, db, expected, limit):
        self.policy.write_text(json.dumps({"maintenance": False, "max_connections": limit}))
        candidate = self.cli(db, "seal", "--expected", str(expected), self.policy)
        self.envelope.write_text(json.dumps(candidate))
        return self.cli(db, "apply", self.envelope)

    def witness(self, operation, db=None, rejection=None):
        run = subprocess.run(["ruby", ROOT / "ruby-witness/witness.rb", operation,
                              self.anchor, db or self.db, self.key], capture_output=True,
                             text=True, timeout=8)
        if rejection:
            self.assertEqual(run.returncode, 1, run.stderr)
            self.assertIn(rejection, run.stderr)
            self.assertEqual(run.stdout, "")
            return
        self.assertEqual(run.returncode, 0, run.stderr)
        return json.loads(run.stdout)

    def test_advances_and_rejects_older_database(self):
        first = self.witness("init")
        self.assertEqual(first["generation"], 0)
        self.apply(self.db, 0, 200)
        self.assertEqual(self.witness("verify")["generation"], 1)
        self.assertEqual(json.loads(self.anchor.read_text()), first)
        latest = self.witness("advance")
        self.assertEqual(json.loads(self.anchor.read_text()), latest)
        self.witness("advance", self.old, rejection="histórico truncado")
        self.assertEqual(json.loads(self.anchor.read_text()), latest)

    def test_rejects_authenticated_fork_at_same_generation(self):
        self.apply(self.db, 0, 200)
        self.apply(self.old, 0, 300)
        initial = self.witness("init")
        self.witness("verify", self.old, rejection="prefixo histórico divergente")
        self.assertEqual(json.loads(self.anchor.read_text()), initial)

    def test_refuses_lacuna_in_authenticated_history(self):
        self.apply(self.db, 0, 200)
        self.apply(self.db, 1, 300)
        with sqlite3.connect(self.db) as db:
            db.execute("DELETE FROM revisions WHERE generation = 1")
        db.close()
        self.witness("init", rejection="lacuna na geração 1")
        self.assertFalse(self.anchor.exists())

    def test_never_advances_after_failed_authentication(self):
        old = self.witness("init")
        self.apply(self.db, 0, 200)
        with sqlite3.connect(self.db) as db:
            db.execute("UPDATE revisions SET mac='broken' WHERE generation=1")
        db.close()
        self.witness("advance", rejection="exportação autenticada falhou")
        self.assertEqual(json.loads(self.anchor.read_text()), old)
