"""Physical parameters used in KickSim.

All values use SI units.  Values labelled ``MODEL ASSUMPTION`` are not yet
calibrated from the actual robot; they must be replaced by measurements before
using absolute distance predictions for design approval.
"""

# Ball: standard golf-ball dimensions used by the current robot.
BALL_MASS_KG = 0.04593
BALL_RADIUS_M = 0.02135
BALL_INERTIA_KG_M2 = 2.0 / 5.0 * BALL_MASS_KG * BALL_RADIUS_M**2

# Striker, including the L-shaped kick plate.
STRIKER_MASS_KG = 0.026
STRIKER_STROKE_M = 0.010

# Electrical hardware.  These values will be used by the later circuit model.
CAPACITOR_F = 4000e-6
INITIAL_VOLTAGE_V = 48.0
COIL_RESISTANCE_OHM = 10.0

# CB1037 data-sheet force curve conditions.
STATIC_FORCE_CURVE_VOLTAGE_V = 24.0

# Impact model.  MODEL ASSUMPTION: calibrate with a high-speed-video test.
STRIKER_BALL_RESTITUTION = 0.65

# Floor model.  MODEL ASSUMPTIONS: replace with RCJ-field measurements.
SLIDING_FRICTION_COEFFICIENT = 0.35
ROLLING_DECELERATION_M_S2 = 1.00

# Numerical settings.
TIME_STEP_S = 1e-5
KICK_HEIGHT_STEP_M = 0.0001
