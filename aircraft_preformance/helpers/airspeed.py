import numpy as np

from . import ureg
from ambiance import Atmosphere


def cas2tas(v_cas, h):
    """
    Convert calibrated airspeed (CAS) to true airspeed (TAS).

    This function calculates the true airspeed (TAS) from the calibrated airspeed (CAS)
    and altitude using the International Standard Atmosphere (ISA) model. It accounts
    for changes in air density and pressure with altitude, as well as compressibility effects.

    Parameters:
    -----------
    v_cas : Quantity
        Calibrated airspeed (CAS) as a quantity with units of speed (e.g., meters per second).
    h : Quantity
        Altitude as a quantity with units of length (e.g., meters).

    Returns:
    --------
    Quantity
        True airspeed (TAS) as a quantity with units of speed, rounded to two decimal places.

    Notes:
    ------
    - The function assumes dry air with a constant ratio of specific heats (gamma = 1.4).
    - The input quantities must be compatible with the `pint` library for unit handling.
    - The `Atmosphere` class from the `ambiance` library is used to retrieve atmospheric
      properties (density, pressure, and speed of sound) at the given altitude.
    - Compressibility effects are considered in the calculations to ensure accuracy at higher speeds.

    Example:
    --------
    >>> from pint import UnitRegistry
    >>> ureg = UnitRegistry()
    >>> v_cas = 100 * ureg('m/s')
    >>> h = 2000 * ureg('m')
    >>> cas2tas(v_cas, h)
    <Quantity(105.34, 'meter / second')>
    """

    # compute densities
    rho_at_h = Atmosphere(h.to("m").m).density[0] * ureg(
        "kg/m**3"
    )  # density at altitude h
    rho_at_sl = Atmosphere(0).density[0] * ureg("kg/m**3")  # densioty at sea level
    # compute pressures
    p_at_h = Atmosphere(h.to("m").m).pressure[0] * ureg("Pa")
    p_at_sl = Atmosphere(0).pressure[0] * ureg("Pa")
    # ratio of specific heats
    gamma = 1.4  # for air

    # compute true airspeed
    g_r = gamma / (gamma - 1)
    p1 = 1 + (np.power((2 * g_r), -1) * (rho_at_sl / p_at_sl) * v_cas**2)
    p2 = np.power(p1, g_r)
    p3 = np.power(1 + ((p_at_sl / p_at_h) * (p2 - 1)), 1 / g_r)
    v_tas = np.sqrt(2 * g_r * (p_at_h / rho_at_h) * (p3 - 1))
    return np.round(v_tas.to_base_units(), 2)


def cas2mach(v_cas, h):
    """
    Convert calibrated airspeed (CAS) to Mach number at a given altitude.

    Parameters:
    -----------
    v_cas : Quantity
        Calibrated airspeed (CAS) as a pint Quantity with appropriate units (e.g., meters per second).
    h : Quantity
        Altitude as a pint Quantity with appropriate units (e.g., meters).

    Returns:
    --------
    float
        Mach number, rounded to three decimal places.

    Notes:
    ------
    - The function computes the true airspeed (TAS) from the given CAS and altitude.
    - The speed of sound is calculated based on the atmospheric conditions at the given altitude.
    - The Mach number is the ratio of the true airspeed to the speed of sound.
    """
    # compute true airspeed
    v_tas = cas2tas(v_cas, h)

    # compute speed of sound at altitude h
    v_sound = Atmosphere(h.to("m").m).speed_of_sound[0] * ureg("m/s")
    mach = v_tas / v_sound
    mach.ito_base_units()

    return np.round(mach, 3)


def tas2cas(v_tas, h):
    """
    Convert True Airspeed (TAS) to Calibrated Airspeed (CAS).

    Parameters:
    -----------
    v_tas : Quantity
        True airspeed, typically provided as a quantity with units (e.g., meters per second).
    h : Quantity
        Altitude, typically provided as a quantity with units (e.g., meters).

    Returns:
    --------
    Quantity
        Calibrated airspeed (CAS) as a quantity with units, rounded to two decimal places.

    Notes:
    ------
    - The function uses the International Standard Atmosphere (ISA) model to compute
      air density and pressure at the given altitude and at sea level.
    - Assumes air behaves as an ideal gas with a specific heat ratio (gamma) of 1.4.
    - The calculations involve compressibility effects and are based on the relationship
      between TAS and CAS under varying atmospheric conditions.
    """

    # compute densities
    rho_at_h = Atmosphere(h.to("m").m).density[0] * ureg(
        "kg/m**3"
    )  # density at altitude h
    rho_at_sl = Atmosphere(0).density[0] * ureg("kg/m**3")  # densioty at sea level
    # compute pressures
    p_at_h = Atmosphere(h.to("m").m).pressure[0] * ureg("Pa")
    p_at_sl = Atmosphere(0).pressure[0] * ureg("Pa")
    # ratio of specific heats
    gamma = 1.4  # for air

    # compute true airspeed
    g_r = gamma / (gamma - 1)
    p1 = 1 + (np.power((2 * g_r), -1) * (rho_at_h / p_at_h) * v_tas**2)
    p2 = np.power(p1, g_r) - 1
    p3 = np.power(((p_at_h / p_at_sl) * p2) + 1, 1 / g_r)
    p4 = p3 - 1
    v_cas = np.sqrt(2 * g_r * (p_at_sl / rho_at_sl) * p4)
    return np.round(v_cas.to_base_units(), 2)


def tas2mach(v_tas, h):
    """
    Convert true airspeed (TAS) to Mach number.

    Parameters:
    -----------
    v_tas : float or Quantity
        True airspeed in meters per second (m/s). If provided as a Quantity,
        it should have compatible units of speed.
    h : Quantity
        Altitude in meters (m). This should be provided as a Quantity with
        compatible units of length.

    Returns:
    --------
    float
        The Mach number, calculated as the ratio of true airspeed to the
        speed of sound at the given altitude. The result is rounded to
        three decimal places.

    Notes:
    ------
    - The speed of sound is determined using the `Atmosphere` class from the
      `ambiance` library, which calculates it based on the altitude.
    - Ensure that the altitude (`h`) is provided with proper units to avoid
      calculation errors.
    """

    v_sound = Atmosphere(h.to("m").m).speed_of_sound[0] * ureg("m/s")
    mach = v_tas / v_sound
    mach.ito_base_units()
    return np.round(mach, 3)
