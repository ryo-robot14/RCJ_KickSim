"""Striker dynamics model."""

from constants import STRIKER_MASS_KG
from solenoid import Solenoid


class Striker:
    """
    Striker model.
    """

    def __init__(self) -> None:
        """Create a striker initially at rest."""
        self.position = 0.0
        self.velocity = 0.0
        self.solenoid = Solenoid()

    def update(self, dt: float) -> float:
        """Advance the striker by ``dt`` and return the solenoid force [N]."""
        force = self.solenoid.force(self.position)
        acceleration = force / STRIKER_MASS_KG
        self.velocity += acceleration * dt
        self.position += self.velocity * dt
        return force
