"""Striker dynamics model."""

from circuit import Circuit
from constants import STRIKER_MASS_KG
from solenoid import Solenoid


class Striker:
    """
    Striker driven by the 48 V capacitor-discharge coil current.
    """

    def __init__(self) -> None:
        """Create a striker initially at rest with a charged capacitor."""
        self.position = 0.0
        self.velocity = 0.0
        self.circuit = Circuit()
        self.solenoid = Solenoid()

    def update(self, dt: float) -> float:
        """Advance the striker by ``dt`` and return the solenoid force [N]."""
        current_a = self.circuit.step(dt)
        force = self.solenoid.force_at_current(self.position, current_a)
        acceleration = force / STRIKER_MASS_KG
        self.velocity += acceleration * dt
        self.position += self.velocity * dt
        return force
