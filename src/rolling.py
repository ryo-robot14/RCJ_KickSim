"""Sliding-to-rolling model for a ball kicked along a level floor."""

from dataclasses import dataclass

from ball import BallState
from constants import (
    BALL_INERTIA_KG_M2,
    BALL_MASS_KG,
    BALL_RADIUS_M,
    ROLLING_DECELERATION_M_S2,
    SLIDING_FRICTION_COEFFICIENT,
)

GRAVITY_M_S2 = 9.80665


@dataclass(frozen=True)
class RollingResult:
    """Distance and state after initial slip has settled into pure rolling."""

    slip_speed_m_s: float
    sliding_time_s: float
    sliding_distance_m: float
    rolling_velocity_m_s: float
    rolling_distance_m: float
    total_distance_m: float


def roll_to_stop(
    ball: BallState,
    friction_coefficient: float = SLIDING_FRICTION_COEFFICIENT,
    rolling_deceleration_m_s2: float = ROLLING_DECELERATION_M_S2,
) -> RollingResult:
    """Return distance from release until rest on a level horizontal field.

    Kinetic friction acts only while the contact point is slipping.  Once
    ``v + r*omega = 0``, the ball is in pure rolling and a measured constant
    rolling deceleration is used to estimate the remaining run-out distance.
    """
    if friction_coefficient <= 0.0:
        raise ValueError("friction_coefficient must be positive")
    if rolling_deceleration_m_s2 <= 0.0:
        raise ValueError("rolling_deceleration_m_s2 must be positive")

    velocity = ball.velocity_m_s
    angular_velocity = ball.angular_velocity_rad_s
    slip_speed = velocity + BALL_RADIUS_M * angular_velocity

    if abs(slip_speed) < 1e-12:
        sliding_time = 0.0
        sliding_distance = 0.0
        rolling_velocity = velocity
    else:
        friction_sign = -1.0 if slip_speed > 0.0 else 1.0
        linear_acceleration = friction_sign * friction_coefficient * GRAVITY_M_S2
        angular_acceleration = (
            friction_sign
            * friction_coefficient
            * BALL_MASS_KG
            * GRAVITY_M_S2
            * BALL_RADIUS_M
            / BALL_INERTIA_KG_M2
        )
        slip_acceleration = linear_acceleration + BALL_RADIUS_M * angular_acceleration
        sliding_time = -slip_speed / slip_acceleration
        sliding_distance = velocity * sliding_time + 0.5 * linear_acceleration * sliding_time**2
        rolling_velocity = velocity + linear_acceleration * sliding_time

    rolling_distance = max(rolling_velocity, 0.0) ** 2 / (2.0 * rolling_deceleration_m_s2)
    return RollingResult(
        slip_speed_m_s=slip_speed,
        sliding_time_s=sliding_time,
        sliding_distance_m=sliding_distance,
        rolling_velocity_m_s=rolling_velocity,
        rolling_distance_m=rolling_distance,
        total_distance_m=sliding_distance + rolling_distance,
    )
