"""Analyse measured kick distances without requiring striker-speed data."""

import argparse
import csv
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import mean, stdev


@dataclass(frozen=True)
class HeightSummary:
    """Distance statistics for one mechanical kick height."""

    height_from_floor_mm: float
    trial_count: int
    mean_distance_m: float
    standard_deviation_m: float


def read_trials(path: Path) -> dict[float, list[float]]:
    """Read heights and stopped distances from the measurement CSV."""
    trials: dict[float, list[float]] = defaultdict(list)
    with path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        required_columns = {"height_from_floor_mm", "roll_distance_m"}
        if reader.fieldnames is None or not required_columns.issubset(reader.fieldnames):
            raise ValueError(
                "CSV must contain height_from_floor_mm and roll_distance_m columns"
            )

        for row_number, row in enumerate(reader, start=2):
            height_text = row["height_from_floor_mm"].strip()
            distance_text = row["roll_distance_m"].strip()
            if not height_text and not distance_text:
                continue
            try:
                height_mm = float(height_text)
                distance_m = float(distance_text)
            except ValueError as error:
                raise ValueError(f"Invalid number in row {row_number}") from error
            if not 0.0 <= height_mm <= 42.70:
                raise ValueError(f"Height out of ball range in row {row_number}: {height_mm}")
            if distance_m < 0.0:
                raise ValueError(f"Distance must be non-negative in row {row_number}")
            trials[height_mm].append(distance_m)
    if not trials:
        raise ValueError("No measurement rows were found")
    return trials


def summarise_trials(trials: dict[float, list[float]]) -> list[HeightSummary]:
    """Calculate mean distance and sample standard deviation per height."""
    summaries = []
    for height_mm, distances_m in trials.items():
        summaries.append(
            HeightSummary(
                height_from_floor_mm=height_mm,
                trial_count=len(distances_m),
                mean_distance_m=mean(distances_m),
                standard_deviation_m=stdev(distances_m) if len(distances_m) > 1 else 0.0,
            )
        )
    return sorted(summaries, key=lambda summary: summary.height_from_floor_mm)


def print_summary(summaries: list[HeightSummary]) -> None:
    """Print a compact table and the best measured height."""
    best = max(summaries, key=lambda summary: summary.mean_distance_m)
    print("Measured kick-height results")
    print("=" * 61)
    print("Height [mm]  Trials  Mean distance [m]  Std. dev. [m]")
    for summary in summaries:
        print(
            f"{summary.height_from_floor_mm:11.2f}"
            f"{summary.trial_count:8d}"
            f"{summary.mean_distance_m:19.3f}"
            f"{summary.standard_deviation_m:15.3f}"
        )
    print()
    print(f"Best measured height: {best.height_from_floor_mm:.2f} mm from floor")
    print(f"Mean stopped distance: {best.mean_distance_m:.3f} m")
    if best.trial_count < 3:
        print("Warning: use at least three trials per height before deciding.")


def parse_arguments() -> argparse.Namespace:
    """Read the input measurement file path."""
    parser = argparse.ArgumentParser(
        description="Find the best measured L-plate kick height."
    )
    parser.add_argument(
        "trials_csv",
        type=Path,
        help="CSV containing height_from_floor_mm and roll_distance_m",
    )
    return parser.parse_args()


def main() -> None:
    """Run the measurement analysis from the command line."""
    arguments = parse_arguments()
    print_summary(summarise_trials(read_trials(arguments.trials_csv)))


if __name__ == "__main__":
    main()
