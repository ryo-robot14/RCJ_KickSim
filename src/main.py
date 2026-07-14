"""Run the preliminary kick-height screening simulation."""

from constants import BALL_RADIUS_M
from simulation import find_best_kick_height, simulate_striker_to_end_of_stroke


def main() -> None:
    """Print a clearly labelled preliminary design result."""
    striker = simulate_striker_to_end_of_stroke()
    best = find_best_kick_height(striker.velocity_m_s)

    theoretical_height_m = BALL_RADIUS_M + 2.0 / 5.0 * BALL_RADIUS_M

    print("KickSim preliminary kick-height screening")
    print("=" * 46)
    print("WARNING: absolute distance is uncalibrated.")
    print("The current striker model uses a 24 V static data-sheet curve.")
    print()
    print(f"Striker end-of-stroke time : {striker.time_s * 1e3:.3f} ms")
    print(f"Striker end-of-stroke speed: {striker.velocity_m_s:.3f} m/s")
    print()
    print(f"Best plate height from floor: {best.height_from_floor_m * 1e3:.2f} mm")
    print(f"Best plate height above centre: {(best.height_from_floor_m - BALL_RADIUS_M) * 1e3:.2f} mm")
    print(f"Theoretical no-slip height   : {theoretical_height_m * 1e3:.2f} mm")
    print(f"Ball release speed           : {best.impact.ball.velocity_m_s:.3f} m/s")
    print(f"Ball angular velocity        : {best.impact.ball.angular_velocity_rad_s:.1f} rad/s")
    print(f"Initial slip speed           : {best.rolling.slip_speed_m_s:.4f} m/s")
    print(f"Preliminary run-out distance : {best.rolling.total_distance_m:.3f} m")


if __name__ == "__main__":
    main()
