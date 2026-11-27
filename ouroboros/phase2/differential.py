"""Campanha diferencial offline sobre permutações sintéticas de 16 bits."""
import json
import random
from array import array
from collections import Counter
from fractions import Fraction
from math import comb, prod

from .baseline.feistel16 import encrypt_with_round_keys, expand_key
from .lab import BITS, SIZE

KEYS = (0x13579BDF, 0x2468ACE0, 0x31415926, 0x27182818)
CONTROL_SEEDS = tuple(range(20261127, 20261131))
ALPHA = Fraction(1, 100)
FAMILY_SIZE = len(KEYS) * len(BITS) * (SIZE - 1)


def overlap_upper_bound(size, pairs):
    """Union bound for overlap with one fixed perfect matching."""
    numerator = comb(size // 2, pairs)
    denominator = prod(size - 1 - 2 * index for index in range(pairs))
    return min(Fraction(1), Fraction(numerator, denominator))


def histogram(table, delta):
    pivot = delta & -delta
    return Counter(value ^ table[index ^ delta]
                   for index, value in enumerate(table) if not index & pivot)


def row_maxima(table, differences):
    rows = []
    for delta in differences:
        counts = histogram(table, delta)
        output, pairs = max(counts.items(), key=lambda item: (item[1], -item[0]))
        rows.append({"input_difference": delta, "output_difference": output, "pairs": pairs})
    return rows


def summarize(table):
    rows = row_maxima(table, BITS)
    maximum = max(row["pairs"] for row in rows)
    bound = min(Fraction(1), FAMILY_SIZE * overlap_upper_bound(SIZE, maximum))
    return {"rows": rows, "max_unordered_pairs": maximum,
            "max_ordered_count": 2 * maximum,
            "familywise_tail_upper_bound": float(bound),
            "crosses_threshold": bound < ALPHA}


def campaign():
    cipher, controls = {}, {}
    for key in KEYS:
        subkeys = expand_key(key)
        table = array("H", (encrypt_with_round_keys(x, subkeys) for x in range(SIZE)))
        cipher[f"{key:08x}"] = summarize(table)
        del table
    for seed in CONTROL_SEEDS:
        table = array("H", range(SIZE))
        random.Random(seed).shuffle(table)
        controls[str(seed)] = summarize(table)
        del table
    return {"domain_size": SIZE, "family_size": FAMILY_SIZE, "alpha": float(ALPHA),
            "feistel": cipher, "controls": controls}


if __name__ == "__main__":
    print(json.dumps(campaign(), indent=2))
