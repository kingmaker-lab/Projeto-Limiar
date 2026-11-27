"""Comparação offline da referência de oito rodadas com uma extensão de quatro."""
import json
import platform
import random
from array import array
from itertools import count
from statistics import median
from time import perf_counter

from .baseline.feistel16 import ROUNDS, expand_key, rotl8, round_function
from .differential import ALPHA, overlap_upper_bound
from .lab import BITS, SIZE
from .rounds import advance, summarize

VARIANT = "W16-K32-Feistel12-S4-P8-KS1E"
EXTENDED_ROUNDS = 12
KEYS = (0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A)
CONTROL_SEEDS = (20261131, 20261132, 20261133, 20261134)
FAMILY_SIZE = len(KEYS) * (EXTENDED_ROUNDS - ROUNDS + 1) * len(BITS) * (SIZE - 1)


def extended_schedule(key):
    reference = expand_key(key)
    state = key.to_bytes(4, "big")
    subkeys = []
    for index in range(EXTENDED_ROUNDS):
        a, b, c, d = state
        mixed = (rotl8(a, 3) + b + rotl8(c, 1) + d + 0x9D + 0x3D * index) & 255
        next_byte = round_function(mixed, 0)
        subkeys.append(next_byte ^ d)
        state = state[1:] + bytes([next_byte])
    if tuple(subkeys[:ROUNDS]) != reference:
        raise AssertionError("O prefixo da agenda difere do EXP-008")
    return tuple(subkeys)


def benchmark(subkeys):
    lookups = [[round_function(right, subkey) for right in range(256)] for subkey in subkeys]
    timings = {8: [], 12: []}
    blocks = 4096
    for repeat in range(5):
        for rounds in ((8, 12) if repeat % 2 == 0 else (12, 8)):
            selected = lookups[:rounds]
            start = perf_counter()
            for block in range(blocks):
                left, right = block >> 8, block & 255
                for lookup in selected:
                    left, right = right, left ^ lookup[right]
            timings[rounds].append((perf_counter() - start) * 1e9 / blocks)
    return {"python": platform.python_version(), "platform": platform.platform(),
            "blocks_per_repeat": blocks, "ns_per_block": timings,
            "median_ns_per_block": {n: median(samples) for n, samples in timings.items()}}


def campaign():
    cutoff = next(2 * k for k in count(1)
                  if FAMILY_SIZE * overlap_upper_bound(SIZE, k) < ALPHA)
    cipher, controls = {}, {}
    for key in KEYS:
        table = array("H", range(SIZE))
        prefixes = {}
        for index, subkey in enumerate(extended_schedule(key), start=1):
            advance(table, subkey)
            if index >= ROUNDS:
                prefixes[str(index)] = summarize(table, cutoff)
        if len(set(table)) != SIZE:
            raise AssertionError("A variante deixou de ser uma permutação")
        cipher[f"{key:08x}"] = prefixes
        del table
    for seed in CONTROL_SEEDS:
        table = array("H", range(SIZE))
        random.Random(seed).shuffle(table)
        controls[str(seed)] = summarize(table, cutoff)
        del table

    return {"variant": VARIANT, "domain_size": SIZE, "family_size": FAMILY_SIZE,
            "alpha": float(ALPHA), "ordered_count_cutoff": cutoff,
            "meets_criterion": any(p["8"]["crosses_threshold"] for p in cipher.values())
            and all(not p["12"]["crosses_threshold"] for p in cipher.values()),
            "feistel": cipher, "controls": controls, "benchmark": benchmark(extended_schedule(KEYS[0]))}


if __name__ == "__main__":
    print(json.dumps(campaign(), indent=2))
