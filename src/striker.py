"""Striker dynamics model."""

from circuit import Circuit
from constants import (
    COIL_INDUCTANCE_H,
    SATURATION_KNEE_CURRENT_A,
    STRIKER_MASS_KG,
    TRIGGER_PULSE_DURATION_S,
)
from solenoid import Solenoid


class Striker:
    """
    Striker driven by the 48 V capacitor-discharge coil current.
    """

    def __init__(
        self,
        coil_inductance_h: float = COIL_INDUCTANCE_H,
        saturation_knee_current_a: float = SATURATION_KNEE_CURRENT_A,
        trigger_pulse_duration_s: float = TRIGGER_PULSE_DURATION_S,
    ) -> None:
        """Create a striker initially at rest with a charged capacitor."""
        self.position = 0.0
        self.velocity = 0.0
        self.elapsed_s = 0.0
        self.circuit = Circuit(coil_inductance_h=coil_inductance_h)
        self.solenoid = Solenoid()
        self.saturation_knee_current_a = saturation_knee_current_a
        self.trigger_pulse_duration_s = trigger_pulse_duration_s

    def update(self, dt: float) -> float:
        """Advance the striker by ``dt`` and return the solenoid force [N]."""
        if self.elapsed_s < self.trigger_pulse_duration_s:
            current_a = self.circuit.step(dt)
        else:
            current_a = 0.0  # NMOS switch has turned off; capacitor disconnected.

        force = self.solenoid.force_at_current(
            self.position, current_a, self.saturation_knee_current_a
        )
        acceleration = force / STRIKER_MASS_KG
        self.velocity += acceleration * dt
        self.position += self.velocity * dt
        self.elapsed_s += dt
        return force
