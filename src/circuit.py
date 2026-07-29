"""Capacitor discharge circuit driving the CB1037 solenoid coil."""

from dataclasses import dataclass

from constants import (
    CAPACITOR_F,
    COIL_INDUCTANCE_H,
    COIL_RESISTANCE_OHM,
    INITIAL_VOLTAGE_V,
)


@dataclass
class Circuit:
    """State of the capacitor-coil discharge loop.

    MODEL ASSUMPTION: COIL_INDUCTANCE_H defaults to 0, so current is
    resistance-limited (I = V / R) rather than following a full R-L-C
    transient. Set COIL_INDUCTANCE_H from a measured value to enable the
    inductive current-rise delay.
    """

    capacitor_voltage_v: float = INITIAL_VOLTAGE_V
    current_a: float = 0.0

    def step(self, dt: float) -> float:
        """Advance the circuit by ``dt`` and return the coil current [A]."""
        if COIL_INDUCTANCE_H > 0.0:
            voltage_across_coil_v = (
                self.capacitor_voltage_v - self.current_a * COIL_RESISTANCE_OHM
            )
            self.current_a += (voltage_across_coil_v / COIL_INDUCTANCE_H) * dt
        else:
            self.current_a = self.capacitor_voltage_v / COIL_RESISTANCE_OHM

        self.capacitor_voltage_v -= self.current_a / CAPACITOR_F * dt
        return self.current_a
