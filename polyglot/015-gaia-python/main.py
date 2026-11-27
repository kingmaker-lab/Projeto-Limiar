import argparse
import csv
import json

from climate import analyze


def main():
    parser = argparse.ArgumentParser(description="Summarize daily station measurements by month")
    parser.add_argument("file")
    parser.add_argument("--baseline", type=int, required=True)
    args = parser.parse_args()
    try:
        with open(args.file, encoding="utf-8", newline="") as stream:
            print(json.dumps(analyze(stream, args.baseline), indent=2))
    except (OSError, ValueError, csv.Error) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
