import unittest
from pathlib import Path

from replay import summarize


class ReplayTests(unittest.TestCase):
    def test_versioned_fixture(self):
        with Path(__file__).with_name("events.jsonl").open(encoding="utf-8") as fixture:
            self.assertEqual(summarize(fixture), {"events": 2, "alerts": ["sample-002"]})

    def test_invalid_records(self):
        valid = '{"id":"sample","action":"policy_change","outcome":"accepted"}'
        cases = [[], ["{"], ["null"], ['{"id":""}'], [valid, valid]]
        for lines in cases:
            with self.subTest(lines=lines), self.assertRaises(ValueError):
                summarize(lines)
