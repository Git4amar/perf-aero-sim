import numpy as np

from . import ureg
from ambiance import Atmosphere


def max_thrust_model(thrust_max_sl, bpr, h, mach):
    """
    Compute the maximum thrust at a given altitude and Mach number.
    Refer the simulation assignmnet documentation for details about the propulsion system characteristics.

    Parameters:
    -----------
    thrust_max_sl : float
        Maximum thrust at sea level (in the same units as the output thrust).
    bpr : float
        Bypass ratio of the engine.
    h : Quantity
        Altitude as a pint Quantity with units of length (e.g., meters or feet).
    mach : float
        Mach number (dimensionless).

    Returns:
    --------
    float
        Maximum thrust at the given altitude and Mach number, rounded to 4 decimal places.

    Notes:
    ------
    - The function uses atmospheric pressure at the given altitude and sea level to compute
      intermediate parameters.
    - The calculation involves empirical coefficients and terms based on the bypass ratio,
      altitude, and Mach number.
    - The `Atmosphere` class and `ureg` are assumed to be part of the codebase, where `Atmosphere`
      provides atmospheric properties and `ureg` is used for unit handling.
    - The function also uses numpy (`np`) for mathematical operations.
    """

    # compute G0
    g_0 = 0.6375 + (0.0604 * bpr)

    # compute pressures
    p_h = Atmosphere(h.to("m").m).pressure[0] * ureg("Pa")  # pressure at altitude h
    p_sl = Atmosphere(0).pressure[0] * ureg("Pa")  # pressure at sea level

    # compute A, X, and Z
    a = (-0.4327 * (p_h / p_sl) ** 2) + (1.3855 * (p_h / p_sl)) + 0.0472
    x = (
        (0.9106 * (p_h / p_sl) ** 3)
        - (1.7736 * (p_h / p_sl) ** 2)
        + (1.8697 * (p_h / p_sl))
    )
    z = (
        (0.1377 * (p_h / p_sl) ** 3)
        - (0.4374 * (p_h / p_sl) ** 2)
        + (1.3003 * (p_h / p_sl))
    )

    temp_term_1 = z * mach * (0.377 * (1 + bpr)) / np.sqrt(g_0 * (1 + (0.82 * bpr)))
    temp_term_2 = (0.23 + (0.19 * np.sqrt(bpr))) * x * mach**2

    thrust_max_h = (a - temp_term_1 + temp_term_2) * thrust_max_sl

    return np.round(thrust_max_h, 4)


def fuel_flow(thrust, mach, h):
    """
    Calculate the fuel flow rate based on thrust, Mach number, and altitude.
    Refer the simulation assignmnet documentation for details about the propulsion system characteristics.

    Parameters:
        thrust (pint.Quantity): The thrust force in newtons (N).
        mach (float): The Mach number, representing the ratio of the object's speed to the speed of sound.
        h (pint.Quantity): The altitude in meters (m).

    Returns:
        pint.Quantity: The fuel flow rate in milligrams per second (mg/s).

    Notes:
        - The function computes the temperature ratio (theta) using the atmospheric temperature at the given altitude
          and sea-level temperature.
        - The thrust specific fuel consumption (TSFC) is calculated in units of mg/s per N, considering the Mach number
          and temperature ratio.
        - The final fuel flow is obtained by multiplying TSFC with the thrust and rounding to 4 decimal places.
    """

    # compute parameter theta
    temp_h = Atmosphere(h.to("m").m).temperature[0] * ureg("K")
    temp_sl = Atmosphere(0).temperature[0] * ureg("K")
    theta = temp_h / temp_sl

    # compute thrust specific fuel consumption in [mg/s /N]
    c_t = 11 * (1 + mach) * np.sqrt(theta) * ureg("mg/s /N")

    # compute and return fuel flow in [mg/s]
    return np.round((c_t * thrust).to_reduced_units(), 4)
