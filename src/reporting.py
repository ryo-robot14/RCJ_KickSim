"""Export simulation results in a spreadsheet-friendly format."""

import csv
from pathlib import Path

from constants import BALL_RADIUS_M
from simulation import HeightResult


def write_height_sweep_csv(path: Path, results: list[HeightResult]) -> None:
    """Write one kick-height simulation result per row to ``path``.

    The CSV is intentionally simple so it can be opened directly in Excel,
    Numbers, or Google Sheets for design comparison.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    field_names = [
        "height_from_floor_mm",
        "height_above_center_mm",
        "ball_release_speed_m_s",
        "ball_angular_velocity_rad_s",
        "initial_slip_speed_m_s",
        "sliding_time_ms",
        "sliding_distance_m",
        "rolling_velocity_m_s",
        "rolling_distance_m",
        "total_distance_m",
    ]

    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()
        for result in results:
            impact = result.impact
            rolling = result.rolling
            writer.writerow(
                {
                    "height_from_floor_mm": f"{result.height_from_floor_m * 1e3:.3f}",
                    "height_above_center_mm": (
                        f"{(result.height_from_floor_m - BALL_RADIUS_M) * 1e3:.3f}"
                    ),
                    "ball_release_speed_m_s": f"{impact.ball.velocity_m_s:.6f}",
                    "ball_angular_velocity_rad_s": (
                        f"{impact.ball.angular_velocity_rad_s:.6f}"
                    ),
                    "initial_slip_speed_m_s": f"{rolling.slip_speed_m_s:.6f}",
                    "sliding_time_ms": f"{rolling.sliding_time_s * 1e3:.6f}",
                    "sliding_distance_m": f"{rolling.sliding_distance_m:.6f}",
                    "rolling_velocity_m_s": f"{rolling.rolling_velocity_m_s:.6f}",
                    "rolling_distance_m": f"{rolling.rolling_distance_m:.6f}",
                    "total_distance_m": f"{rolling.total_distance_m:.6f}",
                }
            )
