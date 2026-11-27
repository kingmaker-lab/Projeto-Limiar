from fractions import Fraction
from itertools import permutations
import unittest

from .differential import overlap_upper_bound, row_maxima


class DifferentialTests(unittest.TestCase):
    def test_identity_pairs_counted_once(self):
        self.assertEqual(row_maxima(range(8), (1, 2, 4)), [
            {"input_difference": delta, "output_difference": delta, "pairs": 4}
            for delta in (1, 2, 4)
        ])

    def test_bound_covers_exact_small_domain(self):
        counts = [sum(table[i] ^ table[i + 1] == 1 for i in (0, 2, 4))
                  for table in permutations(range(6))]
        for threshold in range(1, 4):
            observed = Fraction(sum(count >= threshold for count in counts), len(counts))
            self.assertLessEqual(observed, overlap_upper_bound(6, threshold))
        self.assertEqual(overlap_upper_bound(6, 3), Fraction(1, 15))

    def test_two_bit_difference_counts_both_pair_classes(self):
        from collections import Counter
        from .differential import histogram

        table = (1, 2, 0, 4, 6, 3, 5, 7)
        for delta in (3, 5, 6):
            ordered = Counter(table[i] ^ table[i ^ delta] for i in range(len(table)))
            actual = histogram(table, delta)
            self.assertEqual({value: 2 * count for value, count in actual.items()}, ordered)
