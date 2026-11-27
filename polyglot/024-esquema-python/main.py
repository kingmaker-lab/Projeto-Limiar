import argparse
import json
import sqlite3
from contextlib import closing

from migrations import apply


def main():
    parser = argparse.ArgumentParser(description="Apply an ordered SQLite migration catalog")
    parser.add_argument("database")
    parser.add_argument("directory")
    args = parser.parse_args()
    try:
        with closing(sqlite3.connect(args.database, isolation_level=None)) as connection:
            connection.execute("PRAGMA foreign_keys = ON")
            print(json.dumps({"applied": apply(connection, args.directory)}))
    except (ValueError, sqlite3.Error, OSError) as error:
        parser.exit(2, f"{error}\n")


if __name__ == "__main__":
    main()
