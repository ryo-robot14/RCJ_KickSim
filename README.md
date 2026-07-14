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
