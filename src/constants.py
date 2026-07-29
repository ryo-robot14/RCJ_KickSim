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

# Electrical hardware, from the kicker-001-20260618 boost/NMOS schematic.
CAPACITOR_F = 4000e-6
INITIAL_VOLTAGE_V = 48.0
COIL_RESISTANCE_OHM = 10.0  # CB1037 "CB10370100" winding, per the TAKAHA catalogue.

# MODEL ASSUMPTION: the CB1037 catalogue does not publish coil inductance
# (it is strongly position-dependent for a push solenoid, so manufacturers
# do not characterise it). Current is therefore resistance-limited
# (I = V / R) until a value is measured, e.g. from the current-rise time
# across a shunt resistor on an oscilloscope, or an LCR meter at a few
# plunger positions.
COIL_INDUCTANCE_H = 0.0

# CB1037 data-sheet force curve conditions: the 57.6 W / 6% duty curve,
# i.e. rated current V/R = 24 V / 10 ohm = 2.4 A.
STATIC_FORCE_CURVE_VOLTAGE_V = 24.0

# MODEL ASSUMPTION: the data sheet only characterises force up to the rated
# 2.4 A curve above, not the ~4.8 A surge the 48 V supply produces. Force is
# scaled by the ratio of tanh(I / knee) so it saturates instead of growing as
# I**2 without bound. 3.6 A (1.5x rated) is an engineering guess for where
# the core starts to saturate; replace with a measured force-vs-current
# curve at fixed stroke position once available.
SATURATION_KNEE_CURRENT_A = 3.6

# MODEL ASSUMPTION: the kicker-001-20260618 schematic's one-shot monostable
# sets the NMOS gate-on time via t_s = -R*C*ln(1-(Vth/Vcc)); reading the
# printed component values off that schematic gives t_s ~= 1 ms, but this is
# an approximate transcription from a compressed image, not a verified
# measurement of R9/C7 on the physical board. Defaults to effectively
# unlimited (no cutoff) so it does not silently change existing results;
# confirm the real value against the board, then pass it explicitly (e.g.
# main.py --trigger-duration) to see its effect on stroke completion.
TRIGGER_PULSE_DURATION_S = 0.5

# Impact model.  MODEL ASSUMPTION: calibrate with a high-speed-video test.
STRIKER_BALL_RESTITUTION = 0.65

# Floor model.  MODEL ASSUMPTIONS: replace with RCJ-field measurements.
SLIDING_FRICTION_COEFFICIENT = 0.35
ROLLING_DECELERATION_M_S2 = 1.00

# Numerical settings.
TIME_STEP_S = 1e-5
KICK_HEIGHT_STEP_M = 0.0001

# Safety bound for the striker time-integration loop: with a finite trigger
# pulse duration, current (and force) can drop to zero before the striker
# reaches the end of its stroke, so the loop is no longer guaranteed to
# terminate on its own.
MAX_STRIKER_SIMULATION_TIME_S = 1.0
