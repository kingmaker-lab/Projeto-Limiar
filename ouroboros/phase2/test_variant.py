import unittest
from array import array

from .baseline.feistel16 import encrypt_with_round_keys, expand_key, round_function
from .rounds import advance
from .variant import EXTENDED_ROUNDS, KEYS, extended_schedule


class VariantTests(unittest.TestCase):
    def test_historical_prefix(self):
        for key in KEYS:
            schedule = extended_schedule(key)
            reference = expand_key(key)
            self.assertEqual(schedule[:8], reference)
            self.assertEqual(len(schedule), EXTENDED_ROUNDS)
            table = array("H", [0, 0x1234, 0xFFFF])
            for subkey in schedule[:8]:
                advance(table, subkey)
            self.assertEqual(list(table), [encrypt_with_round_keys(x, reference)
                                          for x in (0, 0x1234, 0xFFFF)])

    def test_variant_inverse_on_synthetic_blocks(self):
        schedule = extended_schedule(KEYS[0])
        plain = range(0, 65536, 257)
        table = array("H", plain)
        for subkey in schedule:
            advance(table, subkey)
        for cipher, expected in zip(table, plain, strict=True):
            left, right = cipher >> 8, cipher & 255
            for subkey in reversed(schedule):
                left, right = right ^ round_function(left, subkey), left
            self.assertEqual((left << 8) | right, expected)
