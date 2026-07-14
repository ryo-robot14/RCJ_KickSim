"""State of the golf ball in the planar kick model."""

from dataclasses import dataclass


@dataclass(frozen=True)
class BallState:
    """Horizontal velocity and spin of the ball.

    Positive angular velocity is counter-clockwise.  Therefore a ball rolling
    toward positive x has a negative angular velocity.
    """

    velocity_m_s: float
    angular_velocity_rad_s: float
