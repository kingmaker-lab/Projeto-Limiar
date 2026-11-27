import unittest
from array import array

from .baseline.feistel16 import encrypt_with_round_keys, expand_key
from .lab import trace
from .rounds import advance


class RoundTests(unittest.TestCase):
    def test_each_prefix_matches_fixed_trace(self):
        report = trace()
        block, *expected = (int(state, 16) for state in report["states"])
        table = array("H", [block])
        for subkey, state in zip(report["subkeys"], expected, strict=True):
            advance(table, subkey)
            self.assertEqual(table[0], state)

    def test_final_mapping_matches_frozen_implementation(self):
        blocks = range(0, 65536, 257)
        table = array("H", blocks)
        subkeys = expand_key(0x13579BDF)
        for subkey in subkeys:
            advance(table, subkey)
        self.assertEqual(list(table), [encrypt_with_round_keys(x, subkeys) for x in blocks])
