"""Aggregation of daily station temperature and precipitation observations."""

import csv
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from math import isfinite


@dataclass
class Summary:
    days: int = 0
    temperature_sum: float = 0.0
    precipitation_mm: float = 0.0

    def add(self, temperature: float, precipitation: float) -> None:
        self.days += 1
        self.temperature_sum += temperature
        self.precipitation_mm += precipitation

    def report(self) -> dict:
        return {
            "days": self.days,
            "mean_temperature_c": round(self.temperature_sum / self.days, 3),
            "precipitation_mm": round(self.precipitation_mm, 3),
        }


def analyze(stream, baseline: int) -> dict:
    reader = csv.DictReader(stream)
    if reader.fieldnames != ["date", "temperature_c", "precipitation_mm"]:
        raise ValueError("expected date,temperature_c,precipitation_mm header")
    months = defaultdict(Summary)
    observed = set()
    for row in reader:
        try:
            if None in row:
                raise ValueError("extra column")
            day = date.fromisoformat(row["date"])
            if row["date"] != day.isoformat() or day in observed:
                raise ValueError("invalid or duplicate date")
            temperature = float(row["temperature_c"])
            rain = float(row["precipitation_mm"])
            if not (isfinite(temperature) and -100 <= temperature <= 80 and isfinite(rain) and 0 <= rain <= 3000):
                raise ValueError("out-of-range observation")
        except (ValueError, TypeError) as error:
            raise ValueError(f"line {reader.line_num}: {error}") from error
        observed.add(day)
        months[(day.year, day.month)].add(temperature, rain)
    if not any(year == baseline for year, _ in months):
        raise ValueError("baseline year missing")
    result = {}
    for (year, month), summary in sorted(months.items()):
        base = months.get((baseline, month))
        anomaly = None
        if base:
            anomaly = round(summary.temperature_sum / summary.days - base.temperature_sum / base.days, 3)
        result[f"{year:04d}-{month:02d}"] = {**summary.report(), "temperature_anomaly_c": anomaly}
    return result
