"""Apply ordered SQL migrations with checksum and transaction checks."""

from hashlib import sha256
from pathlib import Path
import re
import sqlite3

LEDGER = "_schema_migrations"
NAME = re.compile(r"([0-9]{4})_[a-z0-9_]+\.sql")


def catalog(directory):
    paths = sorted(Path(directory).glob("*.sql"))
    if not paths:
        raise ValueError("migration catalog is empty")
    for position, path in enumerate(paths, 1):
        match = NAME.fullmatch(path.name)
        if not match or int(match[1]) != position:
            raise ValueError(f"expected migration {position:04d}, found {path.name}")
        with path.open("rb") as source:
            data = source.read(1024 * 1024 + 1)
        if len(data) > 1024 * 1024:
            raise ValueError(f"{path.name}: exceeds 1 MiB")
        yield path.name, sha256(data).hexdigest(), data.decode("utf-8")


def statements(sql):
    lines = []
    for line in sql.splitlines(keepends=True):
        lines.append(line)
        if ";" in line and sqlite3.complete_statement("".join(lines)):
            yield "".join(lines)
            lines.clear()
    tail = "".join(lines)
    if any(line.strip() and not line.lstrip().startswith("--") for line in tail.splitlines()):
        raise ValueError("unterminated statement (expected semicolon at end of line)")


def authorize(action, first, second, _database, _context):
    forbidden = (sqlite3.SQLITE_TRANSACTION, sqlite3.SQLITE_SAVEPOINT, sqlite3.SQLITE_ATTACH,
                 sqlite3.SQLITE_DETACH, sqlite3.SQLITE_PRAGMA, sqlite3.SQLITE_CREATE_TRIGGER,
                 sqlite3.SQLITE_CREATE_TEMP_TRIGGER, sqlite3.SQLITE_CREATE_VTABLE)
    if action in forbidden or LEDGER in ((first or "").lower(), (second or "").lower()):
        return sqlite3.SQLITE_DENY
    return sqlite3.SQLITE_OK


def apply(connection, directory):
    entries = iter(catalog(directory))
    entry = next(entries)
    connection.execute("BEGIN IMMEDIATE")
    try:
        connection.execute(f"""CREATE TABLE IF NOT EXISTS {LEDGER}
            (position INTEGER PRIMARY KEY, name TEXT NOT NULL, sha256 TEXT NOT NULL)""")
        previous = connection.execute(f"SELECT position, name, sha256 FROM {LEDGER} ORDER BY position")
        for expected, (position, name, digest) in enumerate(previous, 1):
            if position != expected or entry is None or entry[:2] != (name, digest):
                raise ValueError(f"migration history differs at position {expected}")
            entry = next(entries, None)

        applied = []
        while entry is not None:
            name, digest, sql = entry
            connection.set_authorizer(authorize)
            try:
                for statement in statements(sql):
                    connection.execute(statement)
            finally:
                connection.set_authorizer(None)
            position = int(name[:4])
            connection.execute(f"INSERT INTO {LEDGER} VALUES (?, ?, ?)", (position, name, digest))
            applied.append(name)
            entry = next(entries, None)
        connection.commit()
        return applied
    except BaseException:
        connection.rollback()
        raise
