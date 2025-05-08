import numpy as np

from .const import Grav_const


def inst_dv_dt(thrust, drag, w, gamma):
    """
    Calculate the instantaneous rate of change of velocity (dv/dt) for an aircraft.

    Parameters:
        thrust (Quantity): The thrust force acting on the aircraft (e.g., in Newtons).
        drag (Quantity): The drag force acting on the aircraft (e.g., in Newtons).
        w (Quantity): The weight of the aircraft (e.g., in Newtons).
        gamma (Quantity): The flight path angle (e.g., in radians).

    Returns:
        Quantity: The instantaneous rate of change of velocity (dv/dt), rounded to 4 decimal places.

    Notes:
    - Grav_const is assumed to be a predefined constant representing the gravitational acceleration (in meters per second squared).
    - The formula is derived from the equations of motion for an aircraft in a climb or descent.
    """

    return np.round(
        ((Grav_const / w) * (thrust - drag - (w * np.sin(gamma)))).to_reduced_units(), 4
    )


def inst_dgamma_dt(lift, w, v_tas):
    """
    Calculate the instantaneous rate of change of the flight path angle (gamma) with respect to time.

    Parameters:
    lift (float): The lift force acting on the aircraft (in Newtons).
    w (float): The weight of the aircraft (in Newtons).
    v_tas (float): The true airspeed of the aircraft (in meters per second).

    Returns:
    float: The rate of change of the flight path angle (gamma) with respect to time (in radians per second).

    Notes:
    - Grav_const is assumed to be a predefined constant representing the gravitational acceleration (in meters per second squared).
    - The formula is derived from the equations of motion for an aircraft in a climb or descent.
    """
    return (Grav_const / w) * (1 / v_tas) * (lift - w)
