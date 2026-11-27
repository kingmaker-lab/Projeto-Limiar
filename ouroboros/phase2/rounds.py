"""Diagnóstico de prefixos da permutação sintética EXP-008."""
import json
import random
from array import array
from itertools import count

from .baseline.feistel16 import ROUNDS, expand_key, round_function
from .differential import ALPHA, CONTROL_SEEDS, FAMILY_SIZE, KEYS, overlap_upper_bound, row_maxima
from .lab import BITS, SIZE

PREFIX_FAMILY_SIZE = ROUNDS * FAMILY_SIZE


def advance(table, subkey):
    lookup = [round_function(right, subkey) for right in range(256)]
    for index, state in enumerate(table):
        right = state & 255
        table[index] = (right << 8) | ((state >> 8) ^ lookup[right])


def summarize(table, cutoff):
    rows = row_maxima(table, BITS)
    low = 2 * max(row["pairs"] for row in rows[:8])
    high = 2 * max(row["pairs"] for row in rows[8:])
    maximum = max(low, high)
    return {"rows": rows, "low_byte_input_max": low, "high_byte_input_max": high,
            "max_ordered_count": maximum, "crosses_threshold": maximum >= cutoff}


def campaign():
    cutoff = next(2 * k for k in count(1)
                  if PREFIX_FAMILY_SIZE * overlap_upper_bound(SIZE, k) < ALPHA)
    cipher, controls = {}, {}
    for key in KEYS:
        table = array("H", range(SIZE))
        prefixes = []
        for index, subkey in enumerate(expand_key(key), start=1):
            advance(table, subkey)
            prefixes.append({"rounds": index, **summarize(table, cutoff)})
        cipher[f"{key:08x}"] = prefixes
        del table
    for seed in CONTROL_SEEDS:
        table = array("H", range(SIZE))
        random.Random(seed).shuffle(table)
        controls[str(seed)] = summarize(table, cutoff)
        del table
    return {"domain_size": SIZE, "family_size": PREFIX_FAMILY_SIZE, "alpha": float(ALPHA),
            "ordered_count_cutoff": cutoff, "feistel": cipher, "controls": controls}


if __name__ == "__main__":
    print(json.dumps(campaign(), indent=2))
