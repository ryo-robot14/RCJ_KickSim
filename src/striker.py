"""
Striker dynamics model.

This module calculates the motion of the striker.
"""

from constants import STRIKER_MASS_KG


class Striker:
    """
    Striker model.
    """

    def __init__(self):
        self.position = 0.0      # [m]
        self.velocity = 0.0      # [m/s]

    def update(self, force: float, dt: float):
        """
        Update striker state using Euler integration.

        Parameters
        ----------
        force : float
            Applied force [N]

        dt : float
            Time step [s]
        """

        # Newton's second law
        acceleration = force / STRIKER_MASS_KG

        # Euler integration
        self.velocity += acceleration * dt
        self.position += self.velocity * dt