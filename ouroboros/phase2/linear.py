"""Campanha offline de Walsh para máscaras de peso um."""
import json
import random
from array import array
from fractions import Fraction
from math import comb

from .confirm import CONTROL_SEEDS, KEYS, ROUND_COUNTS
from .differential import ALPHA
from .lab import BITS, SIZE
from .rounds import advance
from .variant import extended_schedule

FAMILY_SIZE = len(KEYS) * len(ROUND_COUNTS) * len(BITS) ** 2


def linear_tail_bound(size, overlap):
    half = size // 2
    if overlap <= size // 4:
        return Fraction(1)
    first = Fraction(comb(half, overlap) ** 2, comb(size, half))
    ratio = Fraction(half - overlap, overlap + 1) ** 2
    return min(Fraction(1), 2 * first / (1 - ratio))


def cutoff(family_size=FAMILY_SIZE):
    low, high = SIZE // 4 + 1, SIZE // 2
    while low < high:
        middle = (low + high) // 2
        if family_size * linear_tail_bound(SIZE, middle) < ALPHA:
            high = middle
        else:
            low = middle + 1
    return 4 * low - SIZE


def bit_planes(values, masks):
    planes = []
    for mask in masks:
        packed = bytearray((len(values) + 7) // 8)
        for index, value in enumerate(values):
            if value & mask:
                packed[index >> 3] |= 1 << (index & 7)
        planes.append(int.from_bytes(packed, "little"))
    return planes


def walsh_matrix(inputs, outputs, size):
    return [[size - 2 * (left ^ right).bit_count() for right in outputs] for left in inputs]


def summarize(table, inputs, threshold):
    matrix = walsh_matrix(inputs, bit_planes(table, BITS), len(table))
    peak = max(abs(value) for row in matrix for value in row)
    return {"walsh": matrix, "max_abs_walsh": peak, "crosses_threshold": peak >= threshold}


def campaign():
    threshold = cutoff()
    inputs = bit_planes(range(SIZE), BITS)
    exposures, controls = {}, {}
    for key in KEYS:
        table = array("H", range(SIZE))
        prefixes = {}
        for index, subkey in enumerate(extended_schedule(key), start=1):
            advance(table, subkey)
            if index in ROUND_COUNTS:
                prefixes[str(index)] = summarize(table, inputs, threshold)
        exposures[f"{key:08x}"] = prefixes
    for seed in CONTROL_SEEDS:
        table = array("H", range(SIZE))
        random.Random(seed).shuffle(table)
        controls[str(seed)] = summarize(table, inputs, threshold)
    return {"domain_size": SIZE, "masks": BITS, "family_size": FAMILY_SIZE,
            "alpha": float(ALPHA), "absolute_walsh_cutoff": threshold,
            "feistel": exposures, "controls": controls}


if __name__ == "__main__":
    print(json.dumps(campaign(), indent=2))
