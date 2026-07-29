"""
Solenoid model for CB1037.

The force is approximated from the manufacturer's datasheet.
"""

import numpy as np

from constants import COIL_RESISTANCE_OHM, STATIC_FORCE_CURVE_VOLTAGE_V

# Coil current at which the data-sheet force curve was measured [A].
RATED_CURRENT_A = STATIC_FORCE_CURVE_VOLTAGE_V / COIL_RESISTANCE_OHM

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

    def force_at_current(self, position_m: float, current_a: float) -> float:
        """Return force [N] for an arbitrary coil current at ``position_m``.

        MODEL ASSUMPTION: scales the rated-current data-sheet force by
        ``(current_a / RATED_CURRENT_A) ** 2``, the standard relation for an
        unsaturated reluctance actuator at fixed plunger position. The core
        may saturate before the 48 V surge current is reached, so this can
        overestimate peak force until checked against a measured stroke time.
        """
        return self.force(position_m) * (current_a / RATED_CURRENT_A) ** 2