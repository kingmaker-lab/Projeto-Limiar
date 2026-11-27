"""Campanha diferencial offline para diferenças de entrada de dois bits."""
import json
import random
from array import array
from itertools import combinations, count

from .confirm import CONTROL_SEEDS, KEYS, ROUND_COUNTS
from .differential import ALPHA, overlap_upper_bound, row_maxima
from .lab import BITS, SIZE
from .rounds import advance
from .variant import extended_schedule

DIFFERENCES = {
    "low_byte": tuple(a | b for a, b in combinations(BITS[:8], 2)),
    "high_byte": tuple(a | b for a, b in combinations(BITS[8:], 2)),
    "cross_byte": tuple(a | b for a in BITS[:8] for b in BITS[8:]),
}
FAMILY_SIZE = len(KEYS) * len(ROUND_COUNTS) * sum(map(len, DIFFERENCES.values())) * (SIZE - 1)


def summarize(table, threshold):
    groups = {}
    for label, differences in DIFFERENCES.items():
        rows = row_maxima(table, differences)
        counts = [2 * row["pairs"] for row in rows]
        groups[label] = {
            "max_ordered_count": max(counts),
            "rows_at_or_above_cutoff": sum(n >= threshold for n in counts),
            "rows": rows,
        }
    return groups


def campaign():
    threshold = next(2 * k for k in count(1)
                     if FAMILY_SIZE * overlap_upper_bound(SIZE, k) < ALPHA)
    feistel, controls = {}, {}
    for key in KEYS:
        table = array("H", range(SIZE))
        prefixes = {}
        for index, subkey in enumerate(extended_schedule(key), start=1):
            advance(table, subkey)
            if index in ROUND_COUNTS:
                prefixes[str(index)] = summarize(table, threshold)
        feistel[f"{key:08x}"] = prefixes
    for seed in CONTROL_SEEDS:
        table = array("H", range(SIZE))
        random.Random(seed).shuffle(table)
        controls[str(seed)] = summarize(table, threshold)
    return {"domain_size": SIZE, "family_size": FAMILY_SIZE, "alpha": float(ALPHA),
            "ordered_count_cutoff": threshold, "feistel": feistel, "controls": controls}


def format_report(report):
    """Keep each differential row together in the versioned report."""
    import re

    return re.sub(r"\{\n +(\"input_difference\"[^}]+)\n +\}",
                  lambda match: "{" + re.sub(r"\n +", " ", match[1]) + "}",
                  json.dumps(report, indent=2))


if __name__ == "__main__":
    print(format_report(campaign()))
