"""
Striker dynamics model.

This module calculates the motion of the striker driven by the solenoid.
"""

from constants import STRIKER_MASS_KG
from solenoid import Solenoid


class Striker:
    """
    Striker model.
    """

    def __init__(self):
        # Position [m]
        self.position = 0.0

        # Velocity [m/s]
        self.velocity = 0.0

        # Solenoid model
        self.solenoid = Solenoid()

    def update(self, dt: float):
        """
        Update striker state using Euler integration.

        Parameters
        ----------
        dt : float
            Time step [s]
        """

        # Calculate force from the solenoid model
        force = self.solenoid.force(self.position)

        # Newton's second law
        acceleration = force / STRIKER_MASS_KG

        # Euler integration
        self.velocity += acceleration * dt
        self.position += self.velocity * dt