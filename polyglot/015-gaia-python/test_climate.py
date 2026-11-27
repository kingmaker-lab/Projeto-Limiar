import io
import unittest

from climate import analyze

HEADER = "date,temperature_c,precipitation_mm\n"


class ClimateTest(unittest.TestCase):
    def test_anomaly_and_missing_baseline_month(self):
        report = analyze(io.StringIO(HEADER + "2020-01-01,10,1\n2021-01-04,12,3\n2021-02-01,9,0\n"), 2020)
        self.assertEqual(report["2021-01"]["temperature_anomaly_c"], 2)
        self.assertEqual(report["2021-01"]["precipitation_mm"], 3)
        self.assertIsNone(report["2021-02"]["temperature_anomaly_c"])

    def test_rejects_corrupt_measurements(self):
        for data in ("2020-01-01,NaN,2\n", "2020-01-01,1,-1\n",
                     "2020-01-01,1,2\n2020-01-01,3,4\n"):
            with self.subTest(data=data), self.assertRaises(ValueError):
                analyze(io.StringIO(HEADER + data), 2020)
