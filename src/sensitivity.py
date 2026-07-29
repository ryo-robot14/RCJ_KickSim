"""Monte Carlo sweep over the model's unmeasured (MODEL ASSUMPTION) parameters.

Draws random combinations of coil inductance, restitution, floor friction,
and rolling deceleration from plausible exploration ranges (engineering
judgement, not measurements) and re-runs the full height-optimisation
pipeline for each draw. Reports how much the best height and total distance
move across that uncertainty, and which parameter correlates with the best
height the most -- i.e. which one is worth measuring first.
"""

import argparse
import random
import statistics

from dataclasses import dataclass

from simulation import find_best_kick_height, simulate_striker_to_end_of_stroke

# Exploration ranges for parameters with no measurement yet. These bounds are
# engineering judgement to probe uncertainty, not new ground truth; see the
# matching MODEL ASSUMPTION comments in constants.py for the point estimates
# used elsewhere in the project.
COIL_INDUCTANCE_RANGE_H = (0.0, 0.020)
RESTITUTION_RANGE = (0.45, 0.85)
FRICTION_RANGE = (0.20, 0.50)
ROLLING_DECELERATION_RANGE_M_S2 = (0.5, 1.5)


@dataclass(frozen=True)
class Sample:
    """One Monte Carlo draw: sampled parameters and the resulting optimum."""

    coil_inductance_h: float
    restitution: float
    friction_coefficient: float
    rolling_deceleration_m_s2: float
    best_height_mm: float
    best_total_distance_m: float


def draw_sample(rng: random.Random) -> Sample:
    """Sample one parameter combination and run the full pipeline on it."""
    coil_inductance_h = rng.uniform(*COIL_INDUCTANCE_RANGE_H)
    restitution = rng.uniform(*RESTITUTION_RANGE)
    friction_coefficient = rng.uniform(*FRICTION_RANGE)
    rolling_deceleration_m_s2 = rng.uniform(*ROLLING_DECELERATION_RANGE_M_S2)

    striker = simulate_striker_to_end_of_stroke(coil_inductance_h=coil_inductance_h)
    best = find_best_kick_height(
        striker.velocity_m_s,
        restitution=restitution,
        friction_coefficient=friction_coefficient,
        rolling_deceleration_m_s2=rolling_deceleration_m_s2,
    )
    return Sample(
        coil_inductance_h=coil_inductance_h,
        restitution=restitution,
        friction_coefficient=friction_coefficient,
        rolling_deceleration_m_s2=rolling_deceleration_m_s2,
        best_height_mm=best.height_from_floor_m * 1e3,
        best_total_distance_m=best.rolling.total_distance_m,
    )


def run_sweep(sample_count: int, seed: int) -> list[Sample]:
    """Draw ``sample_count`` independent samples with a reproducible seed."""
    rng = random.Random(seed)
    return [draw_sample(rng) for _ in range(sample_count)]


def pearson_correlation(xs: list[float], ys: list[float]) -> float:
    """Return the Pearson correlation coefficient between ``xs`` and ``ys``."""
    if len(xs) < 2 or statistics.pstdev(xs) == 0.0 or statistics.pstdev(ys) == 0.0:
        return 0.0
    mean_x, mean_y = statistics.fmean(xs), statistics.fmean(ys)
    covariance = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys)) / len(xs)
    return covariance / (statistics.pstdev(xs) * statistics.pstdev(ys))


def print_report(samples: list[Sample]) -> None:
    """Print the spread of outcomes and each parameter's correlation with it."""
    heights = [sample.best_height_mm for sample in samples]
    distances = [sample.best_total_distance_m for sample in samples]

    print("Sensitivity sweep over unmeasured MODEL ASSUMPTION parameters")
    print("=" * 63)
    print(f"Samples: {len(samples)}")
    print()
    print(
        f"Best height    : {min(heights):.2f} - {max(heights):.2f} mm "
        f"(mean {statistics.fmean(heights):.2f}, stdev {statistics.pstdev(heights):.2f})"
    )
    print(
        f"Total distance : {min(distances):.3f} - {max(distances):.3f} m "
        f"(mean {statistics.fmean(distances):.3f}, stdev {statistics.pstdev(distances):.3f})"
    )
    print()
    print("Correlation with best_height_mm (which unknown moves the design height most):")

    parameters = {
        "coil_inductance_h": [sample.coil_inductance_h for sample in samples],
        "restitution": [sample.restitution for sample in samples],
        "friction_coefficient": [sample.friction_coefficient for sample in samples],
        "rolling_deceleration_m_s2": [sample.rolling_deceleration_m_s2 for sample in samples],
    }
    correlations = {
        name: pearson_correlation(values, heights) for name, values in parameters.items()
    }
    for name, correlation in sorted(correlations.items(), key=lambda item: -abs(item[1])):
        print(f"  {name:<28}: r = {correlation:+.3f}")


def parse_arguments() -> argparse.Namespace:
    """Read the sample count and random seed."""
    parser = argparse.ArgumentParser(
        description="Monte Carlo sweep over unmeasured model assumptions."
    )
    parser.add_argument(
        "--samples", type=int, default=300, help="number of Monte Carlo draws"
    )
    parser.add_argument(
        "--seed", type=int, default=0, help="random seed for reproducibility"
    )
    return parser.parse_args()


def main() -> None:
    """Run the sensitivity sweep from the command line."""
    arguments = parse_arguments()
    samples = run_sweep(arguments.samples, arguments.seed)
    print_report(samples)


if __name__ == "__main__":
    main()
