"""Run the preliminary kick-height screening simulation."""

import argparse
from pathlib import Path

from constants import BALL_RADIUS_M
from reporting import write_height_sweep_csv
from simulation import (
    find_best_kick_height,
    simulate_striker_to_end_of_stroke,
    sweep_kick_heights,
)


def parse_arguments() -> argparse.Namespace:
    """Read optional measured striker speed and CSV output path."""
    parser = argparse.ArgumentParser(description="Sweep L-plate kick height.")
    parser.add_argument(
        "--striker-speed",
        type=float,
        default=None,
        metavar="M_S",
        help="measured striker speed at ball contact [m/s]",
    )
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path("output/kick_height_sweep.csv"),
        metavar="PATH",
        help="destination for height-sweep results",
    )
    return parser.parse_args()


def main() -> None:
    """Print a clearly labelled preliminary design result."""
    arguments = parse_arguments()
    striker = simulate_striker_to_end_of_stroke()
    striker_velocity_m_s = (
        striker.velocity_m_s
        if arguments.striker_speed is None
        else arguments.striker_speed
    )
    sweep = sweep_kick_heights(striker_velocity_m_s)
    best = find_best_kick_height(striker_velocity_m_s)
    write_height_sweep_csv(arguments.csv, sweep)

    theoretical_height_m = BALL_RADIUS_M + 2.0 / 5.0 * BALL_RADIUS_M

    print("KickSim preliminary kick-height screening")
    print("=" * 46)
    print("WARNING: absolute distance is uncalibrated.")
    if arguments.striker_speed is None:
        print("Striker speed source: 24 V static data-sheet curve (temporary).")
    else:
        print("Striker speed source: user-supplied measured value.")
    print()
    print(f"Static-model end-of-stroke time: {striker.time_s * 1e3:.3f} ms")
    print(f"Striker speed used             : {striker_velocity_m_s:.3f} m/s")
    print()
    print(f"Best plate height from floor: {best.height_from_floor_m * 1e3:.2f} mm")
    print(f"Best plate height above centre: {(best.height_from_floor_m - BALL_RADIUS_M) * 1e3:.2f} mm")
    print(f"Theoretical no-slip height   : {theoretical_height_m * 1e3:.2f} mm")
    print(f"Ball release speed           : {best.impact.ball.velocity_m_s:.3f} m/s")
    print(f"Ball angular velocity        : {best.impact.ball.angular_velocity_rad_s:.1f} rad/s")
    print(f"Initial slip speed           : {best.rolling.slip_speed_m_s:.4f} m/s")
    print(f"Preliminary run-out distance : {best.rolling.total_distance_m:.3f} m")
    print()
    print(f"Height sweep CSV             : {arguments.csv}")


if __name__ == "__main__":
    main()
