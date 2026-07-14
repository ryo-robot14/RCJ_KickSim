"""Impulse-based planar impact model for the L-shaped kick plate and ball."""

from dataclasses import dataclass

from ball import BallState
from constants import (
    BALL_INERTIA_KG_M2,
    BALL_MASS_KG,
    STRIKER_BALL_RESTITUTION,
    STRIKER_MASS_KG,
)


@dataclass(frozen=True)
class ImpactResult:
    """State immediately after a striker-ball impact."""

    ball: BallState
    striker_velocity_m_s: float
    normal_impulse_n_s: float


def impact_ball(
    striker_velocity_m_s: float,
    impact_height_above_center_m: float,
    restitution: float = STRIKER_BALL_RESTITUTION,
) -> ImpactResult:
    """Calculate a horizontal impact at a specified height on the ball.

    The plate supplies a horizontal impulse.  Its line of action is ``b`` above
    the ball centre, so the same impulse both translates the ball and gives it
    clockwise spin.  This is a rigid-body approximation; contact deformation is
    represented only through the coefficient of restitution.
    """
    if striker_velocity_m_s < 0.0:
        raise ValueError("striker_velocity_m_s must be non-negative")
    if not 0.0 <= restitution <= 1.0:
        raise ValueError("restitution must be between 0 and 1")

    b_m = impact_height_above_center_m
    inverse_effective_mass = (
        1.0 / STRIKER_MASS_KG
        + 1.0 / BALL_MASS_KG
        + b_m**2 / BALL_INERTIA_KG_M2
    )
    impulse_n_s = (1.0 + restitution) * striker_velocity_m_s / inverse_effective_mass

    ball_velocity_m_s = impulse_n_s / BALL_MASS_KG
    ball_angular_velocity_rad_s = -b_m * impulse_n_s / BALL_INERTIA_KG_M2
    striker_after_m_s = striker_velocity_m_s - impulse_n_s / STRIKER_MASS_KG

    return ImpactResult(
        ball=BallState(ball_velocity_m_s, ball_angular_velocity_rad_s),
        striker_velocity_m_s=striker_after_m_s,
        normal_impulse_n_s=impulse_n_s,
    )
