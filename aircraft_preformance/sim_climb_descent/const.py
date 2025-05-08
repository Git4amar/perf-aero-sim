from . import ureg

"""
This module defines constants used in the climb and descent simulation.

Constants:
    Grav_const (Quantity): The gravitational constant, defined as 9.80665 m/s².
    S (Quantity): The wing area of the aircraft, defined as 500 m².
    MTOW (Quantity): The maximum take-off weight of the aircraft, defined as 3600000 N.
    W_fuel (Quantity): The usable fuel weight, defined as 1600000 N.
    Max_Thrust_SE_SL (Quantity): The maximum thrust for a single engine at sea level, defined as 270 kN.
    BPR (int): The bypass ratio of the engine, defined as 5.
"""


Grav_const = ureg("9.80665 m/s**2")

S = ureg("500m**2")  # wing area
MTOW = ureg("3600000N")  # maximum take-off weight
W_fuel = ureg("1600000N")  # useable fuel mass

Max_Thrust_SE_SL = ureg("270kN")  # for single engine in N,
BPR = 5
