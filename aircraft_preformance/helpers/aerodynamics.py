import numpy as np

from . import ureg
from .airspeed import cas2tas
from ambiance import Atmosphere


def c_l_steady(v_cas, altitude, weight, wing_area):
    """
    Calculate the steady-state lift coefficient (C_L) for an aircraft.

    Parameters:
        v_cas (Quantity): Calibrated airspeed (CAS) of the aircraft, typically in units of speed (e.g., meters per second or knots).
        altitude (Quantity): Altitude of the aircraft, typically in units of length (e.g., meters or feet).
        weight (Quantity): Weight of the aircraft, typically in units of force (e.g., newtons or pounds-force).
        wing_area (Quantity): Wing area of the aircraft, typically in units of area (e.g., square meters or square feet).

    Returns:
        Quantity: The steady-state lift coefficient (C_L), a dimensionless value rounded to 4 decimal places.

    Notes:
        - The lift coefficient is calculated under the assumption of steady flight, where lift equals weight.
        - The function uses the lift equation: C_L = (2 * Lift) / (ρ * S * V^2), where:
            - ρ is the air density at the given altitude.
            - S is the wing area.
            - V is the true airspeed (TAS), derived from the calibrated airspeed (CAS).
        - The function internally uses the `Atmosphere` class to determine air density and the `cas2tas` function to convert CAS to TAS.
    """

    # based lift = weight in steady flight condition, calculate lift coeff.
    rho_at_h = Atmosphere(altitude.magnitude).density[0] * ureg(
        "kg/m**3"
    )  # density at altitude h
    v_tas = cas2tas(v_cas, altitude)  # true airspeed

    lift = weight

    # from lift equation
    lift_coeff = (2 * lift) / (rho_at_h * wing_area * v_tas**2)

    return np.round(lift_coeff.to_reduced_units(), 4)
