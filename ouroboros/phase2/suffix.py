"""Compara distribuições diferenciais do prefixo completo e do sufixo correspondente."""
import json
from array import array

from .baseline.feistel16 import expand_key
from .differential import KEYS, histogram
from .lab import BITS, SIZE
from .rounds import advance


def campaign():
    results = {}
    for key in KEYS:
        full, suffix = array("H", range(SIZE)), array("H", range(SIZE))
        by_input = {f"{delta << 8:04x}": [] for delta in BITS[:8]}
        for index, subkey in enumerate(expand_key(key), start=1):
            advance(full, subkey)
            if index > 1:
                advance(suffix, subkey)
            for delta in BITS[:8]:
                high = delta << 8
                full_counts = histogram(full, high)
                suffix_counts = histogram(suffix, delta)
                if full_counts != suffix_counts:
                    raise AssertionError(f"{key:08x}, rodada {index}, diferença {high:04x}")
                output, pairs = max(full_counts.items(), key=lambda item: (item[1], -item[0]))
                by_input[f"{high:04x}"].append({
                    "rounds": index, "max_ordered_count": 2 * pairs,
                    "output_difference": f"{output:04x}", "distinct_outputs": len(full_counts),
                })
        results[f"{key:08x}"] = by_input
    return {"domain_size": SIZE, "full_histograms_matched": len(KEYS) * 8 * len(BITS[:8]),
            "feistel": results}


if __name__ == "__main__":
    print(json.dumps(campaign(), indent=2))
