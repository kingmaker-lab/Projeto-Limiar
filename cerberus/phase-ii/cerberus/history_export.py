"""Exporta revisões autenticadas para uma testemunha de continuidade."""
import argparse
from pathlib import Path
import sqlite3
import sys

from . import core
from .__main__ import read_key


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("db", type=Path)
    parser.add_argument("key", type=Path)
    args = parser.parse_args()
    try:
        key = read_key(args.key)
        # Uma única transação fornece uma visão consistente ao exportador.
        with core.database(args.db) as db:
            for (generation,) in db.execute("SELECT generation FROM revisions ORDER BY generation"):
                sys.stdout.buffer.write(core.canonical(core.load(db, key, generation)) + b"\n")
            sys.stdout.buffer.flush()
    except (ValueError, OSError, sqlite3.Error, RecursionError) as error:
        print(f"Exportação recusada ({error})", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
