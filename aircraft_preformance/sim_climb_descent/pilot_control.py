import numpy as np

from . import ureg
from ..helpers.airspeed import cas2mach, tas2cas
from ambiance import Atmosphere


def pilot_pitch_control(k_p, theta_trim, v_ref, v_ias, h, cruise_mach, phase):
    """Represents pilot pitch control to maintain a specific desired IAS (Indicated Airspeed) or Mach Number.

    This function models the pilot's pitch control response based on the current
    indicated airspeed, altitude, and the desired reference airspeed. It adjusts
    the pitch attitude to maintain the desired airspeed during climb or descent phases.

    Parameters:
        k_p (pint.Quantity): Proportional gain determined through trial and error
            using the simulation model.
        theta_trim (pint.Quantity): Trimmed pitch attitude at the start of the
            simulation phase.
        v_ref_ias (pint.Quantity): Reference constant IAS (Indicated Airspeed)
            to be maintained.
        v_ias (pint.Quantity): Instantaneous IAS of the aircraft.
        h (pint.Quantity): Instantaneous altitude of the aircraft.
        cruise_mach (float): Cruise Mach number, used as a reference for speed
            during climb or descent.
        phase (str): Simulation phase, either 'climb' or 'descent'.

    Returns:
        pint.Quantity: The pilot's instantaneous pitch response in radians.
    """

    # Calculate the speed of sound at the current altitude
    v_sound = Atmosphere(h.to("m").m).speed_of_sound[0] * ureg("m/s")

    # Determine the error in airspeed based on the phase of flight
    if phase == "climb":
        if np.round(cas2mach(v_ias, h), 2) < cruise_mach:
            v_error = v_ias - v_ref
        else:
            v_error = v_ias - tas2cas(cruise_mach * v_sound, h)
    else:  # Descent phase
        if np.round(v_ias) < v_ref:
            v_error = v_ias - tas2cas(cruise_mach * v_sound, h)
        else:
            v_error = v_ias - v_ref

    # Calculate the pitch response based on the error and trim value
    return ((v_error * k_p) * ureg("1 rad")) + theta_trim
