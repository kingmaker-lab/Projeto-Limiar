import json
from pathlib import Path
import sqlite3
import stat
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
BACKUP = Path(__file__).resolve().with_name("cerberus-backup")


class BackupIntegration(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        self.source = self.directory / "operational state.sqlite"
        self.destination = self.directory / "snapshot.sqlite"
        self.key = self.directory / "operator.key"
        self.cli(self.source, "keygen")
        self.cli(self.source, "init")

    def cli(self, db, *args):
        process = subprocess.run([sys.executable, "-m", "cerberus", "--key", self.key,
                                  "--db", db, *args], cwd=ROOT,
                                 capture_output=True, check=True, timeout=8)
        return json.loads(process.stdout)

    def backup(self, source=None):
        return subprocess.run([BACKUP, source or self.source, self.destination],
                              capture_output=True, timeout=8)

    def test_recovers_committed_wal_revision_after_loss(self):
        policy = self.directory / "policy.json"
        policy.write_text('{"maintenance":true,"max_connections":50}')
        envelope = self.directory / "envelope.json"
        with sqlite3.connect(self.source) as writer:
            self.assertEqual(writer.execute("PRAGMA journal_mode=WAL").fetchone(), ("wal",))
            writer.execute("BEGIN")
            writer.execute("SELECT generation FROM revisions").fetchall()
            envelope.write_text(json.dumps(self.cli(self.source, "seal", "--expected", "0", policy)))
            committed = self.cli(self.source, "apply", envelope)
            self.assertGreater(self.source.with_name(self.source.name + "-wal").stat().st_size, 0)
            writer.rollback()
            writer.execute("BEGIN IMMEDIATE")
            writer.execute("UPDATE revisions SET policy='{}' WHERE generation=1")
            run = self.backup()
            self.assertEqual(run.returncode, 0, run.stderr)
            writer.rollback()
        writer.close()

        self.source.unlink()
        self.assertEqual(stat.S_IMODE(self.destination.stat().st_mode), 0o600)
        self.assertEqual(self.cli(self.destination, "status"), committed)
        recovered = self.cli(self.destination, "restore", "--expected", "1", "0")
        self.assertEqual(recovered["generation"], 2)
        self.assertEqual(recovered["source"], 0)

    def test_keeps_existing_destination(self):
        self.destination.write_bytes(b"existing evidence")
        self.assertEqual(self.backup().returncode, 1)
        self.assertEqual(self.destination.read_bytes(), b"existing evidence")
        self.assertEqual(list(self.directory.glob("*.partial.*")), [])

    def test_rejects_unrelated_corrupted_and_missing_sources(self):
        unrelated = self.directory / "unrelated.sqlite"
        with sqlite3.connect(unrelated) as db:
            db.execute("CREATE TABLE other(value TEXT)")
        db.close()
        corrupted = self.directory / "corrupted.sqlite"
        corrupted.write_bytes(b"not a database")
        missing = self.directory / "missing.sqlite"
        for invalid in (unrelated, corrupted, missing):
            with self.subTest(source=invalid):
                self.assertEqual(self.backup(invalid).returncode, 1)
                self.assertFalse(self.destination.exists())
                self.assertEqual(list(self.directory.glob("*.partial.*")), [])
        self.assertFalse(missing.exists())


if __name__ == "__main__":
    unittest.main()
