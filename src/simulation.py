"""High-level simulations used to select an L-plate kick height."""

from dataclasses import dataclass

from constants import (
    BALL_RADIUS_M,
    KICK_HEIGHT_STEP_M,
    STRIKER_STROKE_M,
    TIME_STEP_S,
)
from impact import ImpactResult, impact_ball
from rolling import RollingResult, roll_to_stop
from striker import Striker


@dataclass(frozen=True)
class StrikerResult:
    """State when the striker reaches the end of its available stroke."""

    time_s: float
    velocity_m_s: float


@dataclass(frozen=True)
class HeightResult:
    """Predicted outcome for one kick-plate height measured from the floor."""

    height_from_floor_m: float
    impact: ImpactResult
    rolling: RollingResult


def simulate_striker_to_end_of_stroke() -> StrikerResult:
    """Run the current *24 V static-curve* striker model to 10 mm stroke.

    This is deliberately isolated: the later 48 V capacitor-discharge model can
    replace this function without altering the impact or rolling models.
    """
    striker = Striker()
    time_s = 0.0
    while striker.position < STRIKER_STROKE_M:
        striker.update(TIME_STEP_S)
        time_s += TIME_STEP_S
    return StrikerResult(time_s=time_s, velocity_m_s=striker.velocity)


def simulate_kick_height(
    striker_velocity_m_s: float,
    height_from_floor_m: float,
) -> HeightResult:
    """Simulate impact and roll-out for one L-plate contact height."""
    if not 0.0 <= height_from_floor_m <= 2.0 * BALL_RADIUS_M:
        raise ValueError("height_from_floor_m must lie on the ball: 0 <= h <= 2r")
    impact_height_above_center_m = height_from_floor_m - BALL_RADIUS_M
    impact = impact_ball(striker_velocity_m_s, impact_height_above_center_m)
    rolling = roll_to_stop(impact.ball)
    return HeightResult(height_from_floor_m, impact, rolling)


def find_best_kick_height(striker_velocity_m_s: float) -> HeightResult:
    """Search all plate heights on the ball in 0.1 mm increments."""
    return max(
        sweep_kick_heights(striker_velocity_m_s),
        key=lambda result: result.rolling.total_distance_m,
    )


def sweep_kick_heights(striker_velocity_m_s: float) -> list[HeightResult]:
    """Simulate every valid contact height on the ball in 0.1 mm increments."""
    number_of_steps = round(2.0 * BALL_RADIUS_M / KICK_HEIGHT_STEP_M)
    return [
        simulate_kick_height(striker_velocity_m_s, index * KICK_HEIGHT_STEP_M)
        for index in range(number_of_steps + 1)
    ]
