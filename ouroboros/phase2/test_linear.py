import unittest
from fractions import Fraction
from itertools import combinations
from math import comb

from .linear import FAMILY_SIZE, ALPHA, bit_planes, cutoff, linear_tail_bound, walsh_matrix
from .lab import SIZE


class LinearTests(unittest.TestCase):
    def test_bit_planes_match_scalar_walsh(self):
        values = [0, 2, 4, 7, 3, 6, 5, 1]
        masks = (1, 2, 4)
        actual = walsh_matrix(bit_planes(range(8), masks), bit_planes(values, masks), 8)
        expected = [[sum(1 if bool(i & a) == bool(y & b) else -1
                         for i, y in enumerate(values)) for b in masks] for a in masks]
        self.assertEqual(actual, expected)

    def test_tail_covers_exact_small_distribution(self):
        for threshold in (3, 4):
            count = sum(abs(4 * sum(i < 4 for i in sample) - 8) >= 4 * threshold - 8
                        for sample in combinations(range(8), 4))
            self.assertLessEqual(Fraction(count, comb(8, 4)), linear_tail_bound(8, threshold))

    def test_cutoff_is_first_passing_multiple_of_four(self):
        overlap = (cutoff() + SIZE) // 4
        self.assertLess(FAMILY_SIZE * linear_tail_bound(SIZE, overlap), ALPHA)
        self.assertGreaterEqual(FAMILY_SIZE * linear_tail_bound(SIZE, overlap - 1), ALPHA)
