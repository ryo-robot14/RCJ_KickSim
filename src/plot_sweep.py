"""Render a kick-height sweep CSV as a text-mode chart in the terminal."""

import argparse
import csv
import shutil
from pathlib import Path

FULL_BLOCK = "█"
PARTIAL_BLOCKS = " ▁▂▃▄▅▆▇█"


def read_sweep(path: Path, column: str) -> tuple[list[float], list[float]]:
    """Return (height_from_floor_mm, column values) in row order."""
    heights = []
    values = []
    with path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        if column not in (reader.fieldnames or []):
            raise ValueError(f"Column not found in CSV: {column}")
        for row in reader:
            heights.append(float(row["height_from_floor_mm"]))
            values.append(float(row[column]))
    if not values:
        raise ValueError("CSV contains no data rows")
    return heights, values


def resample(heights: list[float], values: list[float], width: int) -> tuple[list[float], list[float]]:
    """Average values into ``width`` evenly spaced height bins."""
    if len(values) <= width:
        return heights, values
    bin_size = len(values) / width
    resampled_heights = []
    resampled_values = []
    for bin_index in range(width):
        start = int(bin_index * bin_size)
        end = max(start + 1, int((bin_index + 1) * bin_size))
        chunk = values[start:end]
        resampled_values.append(sum(chunk) / len(chunk))
        resampled_heights.append(heights[start])
    return resampled_heights, resampled_values


def render_chart(
    heights: list[float],
    values: list[float],
    rows: int,
    column: str,
    max_at_height_mm: float,
) -> str:
    """Draw a bottom-up bar chart of ``values`` using Unicode block characters."""
    minimum = min(values)
    maximum = max(values)
    value_range = maximum - minimum or 1.0
    levels = [(value - minimum) / value_range * rows for value in values]

    lines = []
    for row in range(rows, 0, -1):
        label = f"{minimum + value_range * row / rows:10.3f} |"
        row_chars = []
        for level in levels:
            covered = level - (row - 1)
            if covered >= 1.0:
                row_chars.append(FULL_BLOCK)
            elif covered > 0.0:
                row_chars.append(PARTIAL_BLOCKS[min(8, max(1, round(covered * 8)))])
            else:
                row_chars.append(" ")
        lines.append(label + "".join(row_chars))
    lines.append(" " * 10 + "+" + "-" * len(values))

    lines.append("")
    lines.append(f"Height range : {heights[0]:.2f} mm (left) to {heights[-1]:.2f} mm (right)")
    lines.append(f"{column:<13}: min={minimum:.4f}  max={maximum:.4f}")
    lines.append(f"Max at height: {max_at_height_mm:.2f} mm from floor")
    return "\n".join(lines)


def parse_arguments() -> argparse.Namespace:
    """Read the CSV path, column to plot, and chart size."""
    parser = argparse.ArgumentParser(
        description="Plot a kick-height sweep CSV as a terminal chart."
    )
    parser.add_argument(
        "csv",
        type=Path,
        nargs="?",
        default=Path("output/kick_height_sweep.csv"),
        help="sweep CSV produced by main.py (default: output/kick_height_sweep.csv)",
    )
    parser.add_argument(
        "--column",
        default="total_distance_m",
        help="CSV column to plot against height_from_floor_mm",
    )
    parser.add_argument("--rows", type=int, default=20, help="chart height in text rows")
    parser.add_argument(
        "--width",
        type=int,
        default=None,
        help="chart width in columns (default: terminal width)",
    )
    return parser.parse_args()


def main() -> None:
    """Print the requested column's height-sweep trend as a terminal chart."""
    arguments = parse_arguments()
    heights, values = read_sweep(arguments.csv, arguments.column)
    max_index = max(range(len(values)), key=lambda i: values[i])
    max_at_height_mm = heights[max_index]

    width = arguments.width or min(len(values), shutil.get_terminal_size().columns - 12)
    heights, values = resample(heights, values, width)
    print(render_chart(heights, values, arguments.rows, arguments.column, max_at_height_mm))


if __name__ == "__main__":
    main()
