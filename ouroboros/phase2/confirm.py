"""Confirmação diferencial offline em chaves sintéticas reservadas."""
import hashlib
import json
import random
from array import array
from itertools import count

from .differential import ALPHA, overlap_upper_bound
from .lab import BITS, SIZE
from .rounds import summarize
from .variant import measure_prefixes

ROUND_COUNTS = (8, 9, 12)
KEY_LABELS = tuple(f"limiar-ouroboros-confirmacao-v1:{index}" for index in range(8))
KEYS = tuple(int.from_bytes(hashlib.sha256(label.encode("ascii")).digest()[:4], "big")
             for label in KEY_LABELS)
CONTROL_SEEDS = tuple(range(20261201, 20261209))
FAMILY_SIZE = len(KEYS) * len(ROUND_COUNTS) * len(BITS) * (SIZE - 1)


def campaign():
    cutoff = next(2 * k for k in count(1)
                  if FAMILY_SIZE * overlap_upper_bound(SIZE, k) < ALPHA)
    feistel = {f"{key:08x}": measure_prefixes(key, ROUND_COUNTS, cutoff) for key in KEYS}
    controls = {}
    for seed in CONTROL_SEEDS:
        table = array("H", range(SIZE))
        random.Random(seed).shuffle(table)
        controls[str(seed)] = summarize(table, cutoff)

    crossing = {str(rounds): sum(row[str(rounds)]["crosses_threshold"] for row in feistel.values())
                for rounds in ROUND_COUNTS}
    return {"key_labels": dict(zip(KEY_LABELS, map("{:08x}".format, KEYS), strict=True)),
            "domain_size": SIZE, "family_size": FAMILY_SIZE, "alpha": float(ALPHA),
            "ordered_count_cutoff": cutoff, "crossing_keys_by_round_count": crossing,
            "meets_criterion": crossing["8"] >= 4 and crossing["9"] == 0,
            "feistel": feistel, "controls": controls}


if __name__ == "__main__":
    print(json.dumps(campaign(), indent=2))
