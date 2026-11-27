from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory
import unittest

from migrations import apply


class MigrationTest(unittest.TestCase):
    def setUp(self):
        work = TemporaryDirectory()
        self.addCleanup(work.cleanup)
        self.directory = Path(work.name)
        self.connection = sqlite3.connect(":memory:", isolation_level=None)
        self.addCleanup(self.connection.close)
        self.first = self.directory / "0001_create.sql"
        self.first.write_text("CREATE TABLE item (name TEXT NOT NULL);\n", encoding="utf-8")

    def test_replay_and_drift(self):
        self.assertEqual(apply(self.connection, self.directory), [self.first.name])
        self.assertEqual(apply(self.connection, self.directory), [])
        self.first.write_text("CREATE TABLE item (name TEXT);\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "history differs"):
            apply(self.connection, self.directory)

    def test_failure_rolls_back_entire_batch(self):
        for invalid in ("COMMIT;\n", "INSERT INTO missing VALUES (1);\n",
                        "DROP TABLE _schema_migrations;\n"):
            (self.directory / "0002_bad.sql").write_text(invalid, encoding="utf-8")
            with self.assertRaises(sqlite3.Error):
                apply(self.connection, self.directory)
            self.assertEqual(self.connection.execute("SELECT name FROM sqlite_master").fetchall(), [])
