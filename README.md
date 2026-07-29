# RCJ_KickSim

Physics simulator for RoboCup Junior Soccer Open solenoid kickers.

## Objective

Develop a physics-based simulator capable of predicting:

- Striker motion
- Ball velocity
- Ball spin
- Rolling distance
- Optimal kick height

## Development

Author: Ryo KAIJIRI

Started: July 2026

## Run the preliminary kick-height sweep

From the repository root:

```bash
python3 src/main.py
```

The result for every 0.1 mm kick-plate height is written to
`output/kick_height_sweep.csv`. Open that CSV in Numbers, Excel, or Google
Sheets to compare height, ball speed, spin, slip, and estimated run-out.

When a striker speed at ball contact has been measured, use it instead of the
temporary 24 V data-sheet model:

```bash
python3 src/main.py --striker-speed 4.20
```

The current rolling-distance result is a screening estimate. It requires
calibration against the actual RCJ field before being used as an absolute
distance prediction.

## Determine the best height without measuring striker speed

Striker speed is difficult to measure during a solenoid kick and is not needed
to determine the best height experimentally.  Record the stopped distance for
several kicks at each fixed plate height, then run the included analyser.

1. Copy `data/measurements/kick_trials_template.csv` to
   `data/measurements/kick_trials.csv`.
2. Use `height_from_floor_mm` for the height of the plate's force line above the
   carpet.  Measure the ball's centre position before the kick and its centre
   position after it stops; their separation is `roll_distance_m`.
3. Add at least three trials at every height, keeping voltage, capacitor charge,
   ball, and field surface unchanged.
4. Analyse the result:

```bash
python3 src/analyze_trials.py data/measurements/kick_trials.csv
```

For a fast first pass, test 26, 28, 30, 32, 34, and 36 mm from the floor.  Then
test the best region in 0.5 mm increments with five trials per height.  This
directly gives the design height even before the 48 V electrical model has been
calibrated.
