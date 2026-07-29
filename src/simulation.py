"""High-level simulations used to select an L-plate kick height."""

from dataclasses import dataclass

from constants import (
    BALL_RADIUS_M,
    COIL_INDUCTANCE_H,
    KICK_HEIGHT_STEP_M,
    MAX_STRIKER_SIMULATION_TIME_S,
    ROLLING_DECELERATION_M_S2,
    SATURATION_KNEE_CURRENT_A,
    SLIDING_FRICTION_COEFFICIENT,
    STRIKER_BALL_RESTITUTION,
    STRIKER_STROKE_M,
    TIME_STEP_S,
    TRIGGER_PULSE_DURATION_S,
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


def simulate_striker_to_end_of_stroke(
    coil_inductance_h: float = COIL_INDUCTANCE_H,
    saturation_knee_current_a: float = SATURATION_KNEE_CURRENT_A,
    trigger_pulse_duration_s: float = TRIGGER_PULSE_DURATION_S,
) -> StrikerResult:
    """Run the 48 V capacitor-discharge striker model to 10 mm stroke.

    This is deliberately isolated from the impact and rolling models, so a
    future refinement (e.g. a measured coil inductance) can replace it
    without touching them.
    """
    striker = Striker(
        coil_inductance_h=coil_inductance_h,
        saturation_knee_current_a=saturation_knee_current_a,
        trigger_pulse_duration_s=trigger_pulse_duration_s,
    )
    time_s = 0.0
    while striker.position < STRIKER_STROKE_M:
        striker.update(TIME_STEP_S)
        time_s += TIME_STEP_S
        if time_s > MAX_STRIKER_SIMULATION_TIME_S:
            raise RuntimeError(
                "Striker did not reach the end of its stroke within "
                f"{MAX_STRIKER_SIMULATION_TIME_S} s; trigger_pulse_duration_s "
                "may be too short, or the coil parameters too weak, to "
                "complete this kick."
            )
    return StrikerResult(time_s=time_s, velocity_m_s=striker.velocity)


def simulate_kick_height(
    striker_velocity_m_s: float,
    height_from_floor_m: float,
    restitution: float = STRIKER_BALL_RESTITUTION,
    friction_coefficient: float = SLIDING_FRICTION_COEFFICIENT,
    rolling_deceleration_m_s2: float = ROLLING_DECELERATION_M_S2,
) -> HeightResult:
    """Simulate impact and roll-out for one L-plate contact height."""
    if not 0.0 <= height_from_floor_m <= 2.0 * BALL_RADIUS_M:
        raise ValueError("height_from_floor_m must lie on the ball: 0 <= h <= 2r")
    impact_height_above_center_m = height_from_floor_m - BALL_RADIUS_M
    impact = impact_ball(striker_velocity_m_s, impact_height_above_center_m, restitution)
    rolling = roll_to_stop(impact.ball, friction_coefficient, rolling_deceleration_m_s2)
    return HeightResult(height_from_floor_m, impact, rolling)


def find_best_kick_height(
    striker_velocity_m_s: float,
    restitution: float = STRIKER_BALL_RESTITUTION,
    friction_coefficient: float = SLIDING_FRICTION_COEFFICIENT,
    rolling_deceleration_m_s2: float = ROLLING_DECELERATION_M_S2,
) -> HeightResult:
    """Search all plate heights on the ball in 0.1 mm increments."""
    return max(
        sweep_kick_heights(
            striker_velocity_m_s, restitution, friction_coefficient, rolling_deceleration_m_s2
        ),
        key=lambda result: result.rolling.total_distance_m,
    )


def sweep_kick_heights(
    striker_velocity_m_s: float,
    restitution: float = STRIKER_BALL_RESTITUTION,
    friction_coefficient: float = SLIDING_FRICTION_COEFFICIENT,
    rolling_deceleration_m_s2: float = ROLLING_DECELERATION_M_S2,
) -> list[HeightResult]:
    """Simulate every valid contact height on the ball in 0.1 mm increments."""
    number_of_steps = round(2.0 * BALL_RADIUS_M / KICK_HEIGHT_STEP_M)
    return [
        simulate_kick_height(
            striker_velocity_m_s,
            index * KICK_HEIGHT_STEP_M,
            restitution,
            friction_coefficient,
            rolling_deceleration_m_s2,
        )
        for index in range(number_of_steps + 1)
    ]
