import unittest
from array import array

from .differential import histogram
from .rounds import advance


class SuffixTests(unittest.TestCase):
    def test_identity_after_omitting_first_round(self):
        prefix = array("H", range(65536))
        suffix = array("H", prefix)
        advance(prefix, 0x17)
        for subkey in (0xAC, 0xF0):
            advance(prefix, subkey)
            advance(suffix, subkey)
            self.assertEqual(histogram(prefix, 0x0400), histogram(suffix, 0x0004))
