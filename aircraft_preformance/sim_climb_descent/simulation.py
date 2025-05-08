import os
import json
import numpy as np

from . import ureg
from ..helpers.airspeed import cas2tas, cas2mach, tas2cas, tas2mach
from ..helpers.aerodynamics import c_l_steady
from .thrust_model import max_thrust_model, fuel_flow
from .pilot_control import pilot_pitch_control
from .eom import inst_dgamma_dt, inst_dv_dt
from .const import Grav_const, Max_Thrust_SE_SL, BPR, S
from .aerodynamic_char import aoa_steady_staight, drag, gamma_steady_straight
from ambiance import Atmosphere


def serialize_and_write_results_file(res, w_initial, v_ref, phase):
    """
    Serializes simulation results and writes them to a JSON file.

    This function takes a dictionary of simulation results, converts the values
    (assumed to be quantities with units) into a serializable format, and writes
    the results to a JSON file. Each result is stored with its magnitude and units.

    Args:
        res (dict): A dictionary where keys are result names and values are
                    quantities (e.g., Pint Quantity objects) to be serialized.
        phase (str): A string representing the phase of the simulation
                     (e.g., "climb" or "descent"). This is used to name the
                     output JSON file.

    Raises:
        ValueError: If the input data cannot be serialized properly.
        IOError: If there is an issue writing to the output file.

    Output:
        A JSON file named `<phase>_simulation_result.json` containing the
        serialized results.
    """
    dump_res = {}
    for i in res:
        res[i] = ureg.Quantity.from_list(res[i])
        dump_res[i] = {}
        dump_res[i]["magnitude"] = json.dumps(res[i].magnitude.tolist())
        dump_res[i]["units"] = str(res[i].units)

    directory = "simulation_results"
    file_path = os.path.join(
        directory,
        f"{phase}_{int(np.round(w_initial.to('N').m))}_{int(np.round(v_ref.to('m/s').m))}_simulation_result.json",
    )
    # create directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # create a JSON result file
    with open(file_path, "w") as file:
        json.dump(dump_res, file, indent=4)


def simulation_euler(
    ics, time_step, pilot_control_model, k_p, v_ref, cruise_mach, phase
):
    """
    Simulates the climb or descent phase of an aircraft using the Euler method.

    Parameters:
        ics (dict): Initial conditions of the simulation, including:
            - "x" (float): Initial horizontal position.
            - "h" (float): Initial altitude.
            - "w" (float): Initial weight of the aircraft.
            - "v_ias" (float): Initial indicated airspeed (IAS).
        time_step (pint.Quantity): Time step for the simulation (e.g., in seconds).
        pilot_control_model (callable): Function to compute the pitch attitude based on control inputs.
        k_p (float): Proportional gain for the pilot control model.
        v_ref_ias (float): Reference indicated airspeed (IAS) for the control model.
        cruise_mach (float): Cruise Mach number for the simulation.
        phase (str): Phase of flight, either "climb" or "descent".
        take_off_weight (float): Initial take-off weight of the aircraft.

    Returns:
        dict: A dictionary containing the simulation results with the following keys:
            - "t": List of time steps.
            - "x": List of horizontal positions.
            - "h": List of altitudes.
            - "v_tas": List of true airspeeds (TAS).
            - "v_ias": List of indicated airspeeds (IAS).
            - "mach": List of Mach numbers.
            - "gamma": List of flight path angles.
            - "fuel_burn": List of fuel burned.
            - "aoa": List of angles of attack.
            - "theta": List of pitch attitudes.

    Notes:
        - The simulation stops when the aircraft reaches a cruise altitude of 10,000 m during climb
          or descends to 1,000 m during descent.
        - Results are serialized and saved to a JSON file named `<phase>_simulation_result.json`.

    Raises:
        ValueError: If the `phase` parameter is not "climb" or "descent".
    """

    t = ureg("0 s")
    dt = time_step

    # initialize state variable
    x = ics["x"]
    h = ics["h"]
    w = ics["w"]
    m_f_burnt = ureg("0 g")
    v_ias = ics["v_ias"]
    v_tas = cas2tas(v_ias, h)  # IAS is assumed same as CAS
    mach = cas2mach(v_ias, h)
    aoa = aoa_steady_staight(v_ias, h, w, S)
    # 95% of max thrust is applied for climb phase and 5% of max thrust is applied for descent phase
    thrust_app_perc = 0.95 if phase == "climb" else 0.05

    gamma = gamma_steady_straight(
        # total thrust of 4 engines and apply 95% of it
        4 * max_thrust_model(Max_Thrust_SE_SL, BPR, h, mach) * thrust_app_perc,
        drag(v_ias, h, c_l_steady(v_ias, h, w, S), S),
        w,
    )
    theta_trim = aoa + gamma

    # initialize result dictionary at t = 0
    res = {
        "t": [t],
        "x": [x],
        "h": [h],
        "v_tas": [v_tas],
        "v_ias": [v_ias],
        "mach": [mach],
        "gamma": [gamma],
        "fuel_burn": [m_f_burnt],
        "aoa": [aoa],
        "theta": [theta_trim],
    }

    while True:
        # re-evaluate control model at start of dt
        # compute pitch attitude in rad
        theta = pilot_control_model(
            k_p, theta_trim, v_ref, v_ias, h, cruise_mach, phase
        )
        # compute angle of attack
        aoa = theta - gamma
        # compute lift coeff based on angle of attack
        c_l = 0.03 + (4.4 * aoa)

        # compute forces at start of dt
        # compute instantaneous lift
        inst_lift = (
            (1 / 2)
            * c_l
            * (Atmosphere(h.to("m").m).density[0] * ureg("kg/m**3"))
            * S
            * v_tas**2
        )
        # compute instantaneous total thrust of 4 engines and apply 95% of it
        inst_thrust = (
            4 * max_thrust_model(Max_Thrust_SE_SL, BPR, h, mach) * thrust_app_perc
        )

        # compute instantaneous drag
        inst_drag = drag(v_ias, h, c_l, S)

        # simulate changes during dt
        dh = v_tas * np.sin(gamma) * dt
        dv_tas = inst_dv_dt(inst_thrust, inst_drag, w, gamma) * dt
        dgamma = inst_dgamma_dt(inst_lift, w, v_tas) * dt
        dm = -fuel_flow(inst_thrust, mach, h) * dt
        dw = dm * Grav_const
        dx = v_tas * np.cos(gamma) * dt

        # reflect changes after dt
        x += dx
        h += dh
        v_tas += dv_tas
        v_ias = tas2cas(v_tas, h)
        mach = cas2mach(v_ias, h)
        gamma += dgamma
        m_f_burnt += np.abs(dm)
        w += dw
        t += dt

        # append the results
        res["t"].append(t)
        res["x"].append(x)
        res["h"].append(h)
        res["v_tas"].append(v_tas)
        res["v_ias"].append(v_ias)
        res["mach"].append(mach)
        res["gamma"].append(gamma)
        res["fuel_burn"].append(m_f_burnt)
        res["aoa"].append(aoa)
        res["theta"].append(theta)

        # set stop condition i.e. aircraft reaches a cruise altitude of 10,000 m or descends to 1000m
        match phase:
            case "climb":
                if h >= ureg("10000 m"):
                    break
            case "descent":
                if h <= ureg("1000 m"):
                    break

    # serialize results and prepare for JSON results
    serialize_and_write_results_file(res, ics["w"], v_ref, phase)
    return res


def simulation_descent_approach_euler(
    ics, time_step, v_ref, glideslope_angle, screen_h, phase
):

    t = ureg("0 s")
    dt = time_step

    # initialize state variable
    x = ics["x"]
    h = ics["h"]
    w = ics["w"]
    m_f_burnt = ureg("0 g")
    v_tas = v_ref
    v_ias = tas2cas(v_tas, h)
    mach = tas2mach(v_tas, h)
    gamma = -1 * glideslope_angle.to("rad")

    # initialize result dictionary at t = 0
    res = {
        "t": [t],
        "x": [x],
        "h": [h],
        "v_ias": [v_ias],
        "mach": [mach],
        "fuel_burn": [m_f_burnt],
        "aoa": [],
        "theta": [],
        "thrust": [],
    }

    while True:
        # based on simplified EOM for steady straight powered glide flight compute pitch and thrust setting
        aoa = aoa_steady_staight(tas2cas(v_tas, h), h, w, S)
        theta = aoa + gamma
        res["aoa"].append(aoa)
        res["theta"].append(theta)

        c_l = c_l_steady(tas2cas(v_tas, h), h, w, S)
        inst_drag = drag(tas2cas(v_tas, h), h, c_l, S)
        inst_thrust = inst_drag + (w * np.sin(gamma))
        res["thrust"].append(inst_thrust)

        # compute changes during time_step dt
        dh = v_tas * np.sin(gamma) * dt
        dx = v_tas * np.cos(gamma) * dt
        dm = -fuel_flow(inst_thrust, mach, h) * dt
        dw = dm * Grav_const

        # reflect changes
        h += dh
        x += dx
        m_f_burnt += np.abs(dm)
        w += dw
        t += dt
        mach = tas2mach(v_tas, h)

        if h <= screen_h:
            break
        else:
            res["t"].append(t)
            res["x"].append(x)
            res["h"].append(h)
            res["v_ias"].append(tas2cas(v_tas, h))
            res["mach"].append(mach)
            res["fuel_burn"].append(m_f_burnt)

    # serialize results and prepare for JSON results
    serialize_and_write_results_file(res, ics["w"], v_ref, phase=phase)

    return res


def load_or_run_simulation(simulation, **kwargs):
    """
    Loads simulation results from a JSON file if available, or runs a simulation
    to generate the results if the file is not found.

    Args:
        ics (dict): Initial conditions for the simulation.
        time_step (float): Time step for the simulation.
        k_p (float): Proportional gain for the pilot pitch control.
        v_ref (float): Reference velocity for the simulation.
        cruise_mach (float): Cruise Mach number for the simulation.
        phase (str): Phase of the simulation ("climb", "descent", or "descent_approach").
        take_off_weight (float): Take-off weight of the aircraft.
        glideslope_angle (Quantity, optional): Glideslope angle for descent approach. Defaults to 3 degrees.
        screen_h (Quantity, optional): Screen height for descent approach. Defaults to 35 feet.

    Returns:
        dict: A dictionary containing the simulation results. If loaded from a file,
              the results are converted to quantities with units.

    Raises:
        ValueError: If the provided phase is not one of "climb", or "descent".
    """
    # extract parameters from kwargs to evaluate function logic
    phase = kwargs["phase"]
    ics = kwargs["ics"]
    v_ref = kwargs["v_ref"]

    # Ensure the phase is valid
    if kwargs["phase"] not in ["climb", "descent", "descent_approach"]:
        raise ValueError(
            "Phase must be either 'climb', 'descent', or 'descent_approach'."
        )

    result = {}

    directory = "simulation_results"
    file_path = os.path.join(
        directory,
        f"{phase}_{int(np.round(ics['w'].to('N').m))}_{int(np.round(v_ref.to('m/s').m))}_simulation_result.json",
    )

    # Check if the results file exists
    if os.path.exists(file_path):
        print("Simulation results file found")
        with open(file_path, "r") as file:
            loaded_res = json.load(file)
            for i in loaded_res:
                result[i] = json.loads(loaded_res[i]["magnitude"]) * ureg(
                    loaded_res[i]["units"]
                )
        print("Simulation results loaded")
    else:
        print("No simulation results file found")
        print(f"Running simulation to generate results file for {phase} phase....")
        result = simulation(**kwargs)
        print("Simulation completed")

    return result
