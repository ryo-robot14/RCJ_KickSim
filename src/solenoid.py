"""
Solenoid model for CB1037.

The force is approximated from the manufacturer's datasheet.
"""

import numpy as np


# Stroke [mm]
stroke_mm = np.array([
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10
])

# Force [N]
force_n = np.array([
    28.5,
    22.5,
    19.2,
    17.8,
    16.8,
    15.8,
    14.4,
    12.6,
    10.7,
    8.9,
    7.2
])


class Solenoid:

    def force(self, position_m: float) -> float:
        """
        Return force [N] from striker position.
        """

        position_mm = position_m * 1000

        return float(
            np.interp(
                position_mm,
                stroke_mm,
                force_n
            )
        )