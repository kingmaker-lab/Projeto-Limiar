"""Amplia o ensaio de Walsh offline para máscaras de até dois bits."""
import json
import random
from array import array
from itertools import combinations

from .confirm import CONTROL_SEEDS, KEYS, ROUND_COUNTS
from .differential import ALPHA
from .lab import BITS, SIZE
from .linear import bit_planes, cutoff, walsh_matrix
from .rounds import advance
from .variant import extended_schedule

PAIRS = tuple(combinations(range(len(BITS)), 2))
MASKS = (BITS, tuple(BITS[i] | BITS[j] for i, j in PAIRS))
FAMILY_SIZE = len(KEYS) * len(ROUND_COUNTS) * sum(map(len, MASKS)) ** 2


def parity_planes(values):
    singles = bit_planes(values, BITS)
    return singles, [singles[i] ^ singles[j] for i, j in PAIRS]


def summarize(table, inputs, threshold):
    outputs = parity_planes(table)
    groups = {}
    for input_weight, left in enumerate(inputs, start=1):
        for output_weight, right in enumerate(outputs, start=1):
            matrix = walsh_matrix(left, right, len(table))
            cells = [(i, j, value) for i, row in enumerate(matrix) for j, value in enumerate(row)]
            i, j, peak = max(cells, key=lambda cell: abs(cell[2]))
            groups[f"{input_weight}x{output_weight}"] = {
                "max_abs_walsh": abs(peak),
                "signed_walsh": peak,
                "input_mask": f"{MASKS[input_weight - 1][i]:04x}",
                "output_mask": f"{MASKS[output_weight - 1][j]:04x}",
                "cells_at_or_above_cutoff": sum(abs(value) >= threshold for _, _, value in cells),
            }
    return groups


def campaign():
    threshold = cutoff(FAMILY_SIZE)
    inputs = parity_planes(range(SIZE))
    feistel, controls = {}, {}
    for key in KEYS:
        table = array("H", range(SIZE))
        summaries = {}
        for index, subkey in enumerate(extended_schedule(key), start=1):
            advance(table, subkey)
            if index in ROUND_COUNTS:
                summaries[str(index)] = summarize(table, inputs, threshold)
        feistel[f"{key:08x}"] = summaries
    for seed in CONTROL_SEEDS:
        table = array("H", range(SIZE))
        random.Random(seed).shuffle(table)
        controls[str(seed)] = summarize(table, inputs, threshold)
    return {"domain_size": SIZE, "family_size": FAMILY_SIZE, "alpha": float(ALPHA),
            "absolute_walsh_cutoff": threshold, "feistel": feistel, "controls": controls}


if __name__ == "__main__":
    print(json.dumps(campaign(), indent=2))
