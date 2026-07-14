"""
KickSim main program.
"""

from striker import Striker


def main():

    striker = Striker()

    # Simulation settings
    dt = 1e-5           # 10 µs
    total_time = 0.005  # 5 ms

    time = 0.0

    print(" Time [ms]   Position [mm]   Velocity [m/s]")

    while time <= total_time:

        striker.update(dt)

        if int(time * 100000) % 50 == 0:
            print(
                f"{time * 1000:8.3f}"
                f"{striker.position * 1000:15.3f}"
                f"{striker.velocity:15.3f}"
            )

        time += dt


if __name__ == "__main__":
    main()