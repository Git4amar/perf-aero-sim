import matplotlib.pyplot as plt
import numpy as np

from . import ureg
from ..helpers.airspeed import cas2tas

ureg.setup_matplotlib(True)  # Enable matplotlib integration
# Optional: Set a custom formatter for unit-aware labels
ureg.mpl_formatter = "{:~P}"  # Compact formatting for units (e.g., 'km', 'min')


def plot_horizontal_distance_vs_time(result):
    """
    Plots the horizontal distance traveled relative to the ground versus time.

    This function generates a plot that visualizes the horizontal distance
    traveled over time, with annotations for the total distance and the
    distance traveled to an altitude of 5 km (if applicable). The plot includes
    gridlines, units for axes, and labeled annotations.

    Parameters:
    -----------
    result : dict
        A dictionary containing the following keys:
        - "t" : array-like
            Time data (assumed to be in units compatible with `ureg.min`).
        - "x" : array-like
            Horizontal distance data (assumed to be in units compatible with `ureg.km`).
        - "h" : array-like
            Altitude data (assumed to be in units compatible with `ureg.km`).

    Notes:
    ------
    - The function uses `matplotlib` for plotting.
    - The `ureg` object is assumed to be a unit registry (e.g., from the `pint` library).
    - The function adds annotations for:
        1. The total horizontal distance traveled.
        2. The horizontal distance traveled to an altitude of 5 km, if such an altitude is reached.
    - Gridlines (both major and minor) are added to the plot for better readability.

    Returns:
    --------
    None
        The function displays the plot but does not return any value.
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(result["t"], result["x"], label="Horizontal Distance")
    ax.set_title("Horiz. distance travelled relative to the ground vs Time")
    ax.xaxis.set_units(ureg.min)
    ax.yaxis.set_units(ureg.km)

    # Add major and minor gridlines
    ax.grid(which="major", color="k", linestyle="-.", linewidth=0.5)
    ax.grid(which="minor", color="gray", linestyle=":", linewidth=0.4)
    ax.minorticks_on()

    # Add annotation for total distance
    ax.annotate(
        "",
        xy=(result["t"][-1], result["x"][-1]),
        xytext=(result["t"][-1], result["x"][0]),
        arrowprops=dict(arrowstyle="<->", ls="-.", lw=1, color="r"),
    )
    ax.text(
        result["t"][-1],
        (result["x"][0] + result["x"][-1]) / 2,
        f"Distance {np.round(result['x'][-1].to(ureg.km), 1):~}",
        rotation=0,
        horizontalalignment="center",
        bbox=dict(facecolor="wheat", alpha=0.5),
    )

    # Add annotation and text for horizontal distance at altitude of 5 km
    altitude_5km_indices = np.where(result["h"] >= 5 * ureg.km)[0]
    if len(altitude_5km_indices) > 0:
        altitude_5km_index = (
            altitude_5km_indices[0]
            if result["h"][0] < 5 * ureg.km
            else altitude_5km_indices[-1]
        )
        ax.annotate(
            "",
            xy=(result["t"][altitude_5km_index], result["x"][altitude_5km_index]),
            xytext=(result["t"][altitude_5km_index], result["x"][0]),
            arrowprops=dict(arrowstyle="<->", ls="-.", lw=1, color="b"),
        )
        ax.text(
            result["t"][altitude_5km_index],
            (result["x"][0] + result["x"][altitude_5km_index]) / 2,
            f"Distance {np.round(result['x'][altitude_5km_index].to(ureg.km), 1):~} @ 5 km",
            rotation=0,
            horizontalalignment="center",
            bbox=dict(facecolor="lightblue", alpha=0.5),
        )

    plt.legend()
    plt.show()


def plot_altitude_vs_time(result):
    """
    Plots altitude versus time and adds annotations for total time and time to reach an altitude of 5 km (if applicable).

    Parameters:
    -----------
    result : dict
        A dictionary containing the following keys:
        - "t": array-like, time values with units (e.g., seconds or minutes).
        - "h": array-like, altitude values with units (e.g., meters or kilometers).

    Description:
    ------------
    This function creates a plot of altitude (y-axis) versus time (x-axis) using the data
    provided in the `result` dictionary. It includes the following features:
    - Major and minor gridlines for better readability.
    - An annotation indicating the total time duration of the flight.
    - An annotation and text indicating the time at which the altitude reaches 5 km
      (if applicable).

    Notes:
    ------
    - The function assumes that the time and altitude values in `result` are compatible
      with the `pint` unit registry (`ureg`).

    Returns:
    --------
    None
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(result["t"], result["h"], label="Altitude")
    ax.set_title("Altitude vs Time")
    ax.xaxis.set_units(ureg.min)
    ax.yaxis.set_units(ureg.km)

    # Add major and minor gridlines
    ax.grid(which="major", color="k", linestyle="-.", linewidth=0.5)
    ax.grid(which="minor", color="gray", linestyle=":", linewidth=0.4)
    ax.minorticks_on()

    # Add annotation for total time
    ax.annotate(
        "",
        xy=(result["t"][0], result["h"][-1]),
        xytext=(result["t"][-1], result["h"][-1]),
        arrowprops=dict(arrowstyle="<->", ls="-.", lw=1, color="r"),
    )
    ax.text(
        (result["t"][0] + result["t"][-1]) / 2,
        result["h"][-1],
        f"Time {np.round(result['t'][-1].to(ureg.min), 1):~}",
        rotation=0,
        horizontalalignment="center",
        bbox=dict(facecolor="wheat", alpha=0.5),
    )

    # Add annotation and text for time at altitude of 5 km
    altitude_5km_indices = np.where(result["h"] >= 5 * ureg.km)[0]
    if len(altitude_5km_indices) > 0:
        altitude_5km_index = (
            altitude_5km_indices[0]
            if result["h"][0] < 5 * ureg.km
            else altitude_5km_indices[-1]
        )
        ax.annotate(
            "",
            xy=(result["t"][altitude_5km_index], result["h"][altitude_5km_index]),
            xytext=(result["t"][0], result["h"][altitude_5km_index]),
            arrowprops=dict(arrowstyle="<->", ls="-.", lw=1, color="b"),
        )
        ax.text(
            (result["t"][0] + result["t"][altitude_5km_index]) / 2,
            result["h"][altitude_5km_index],
            f"Time {np.round(result['t'][altitude_5km_index].to(ureg.min), 1):~} @ 5 km",
            rotation=0,
            horizontalalignment="center",
            bbox=dict(facecolor="lightblue", alpha=0.5),
        )

    plt.legend()
    plt.show()


def plot_altitude_vs_distance(result):
    """
    Plots the altitude versus horizontal distance from the given simulation results.

    The function generates a plot with the following features:
    - A line plot of altitude (`h`) versus horizontal distance (`x`).
    - Major and minor gridlines for better readability.
    - An annotation indicating the total horizontal distance covered.
    - An annotation and text indicating the horizontal distance to reach an altitude of 5 km, if applicable.

    Parameters:
    -----------
    result : dict
        A dictionary containing the simulation results with the following keys:
        - "x": Array-like, horizontal distance values (with units).
        - "h": Array-like, altitude values (with units).

    Notes:
    ------
    - The function assumes that the `result` dictionary contains quantities with units compatible
      with the `pint` library (`ureg`).
    - The plot uses `matplotlib` for visualization and requires `numpy` for array operations.

    Returns:
    --------
    None
        Displays the plot directly.
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(result["x"], result["h"], label="Altitude vs Distance")
    ax.set_title("Altitude vs Horiz. Distance")
    ax.xaxis.set_units(ureg.km)
    ax.yaxis.set_units(ureg.km)

    # Add major and minor gridlines
    ax.grid(which="major", color="k", linestyle="-.", linewidth=0.5)
    ax.grid(which="minor", color="gray", linestyle=":", linewidth=0.4)
    ax.minorticks_on()

    # Add annotation for total distance
    ax.annotate(
        "",
        xy=(result["x"][0], result["h"][-1]),
        xytext=(result["x"][-1], result["h"][-1]),
        arrowprops=dict(arrowstyle="<->", ls="-.", lw=1, color="r"),
    )
    ax.text(
        (result["x"][0] + result["x"][-1]) / 2,
        result["h"][-1],
        f"Distance {np.round(result['x'][-1].to(ureg.km), 1):~}",
        rotation=0,
        horizontalalignment="center",
        bbox=dict(facecolor="wheat", alpha=0.5),
    )

    # Add annotation and text for distance at altitude of 5 km
    altitude_5km_indices = np.where(result["h"] >= 5 * ureg.km)[0]
    if len(altitude_5km_indices) > 0:
        altitude_5km_index = (
            altitude_5km_indices[0]
            if result["h"][0] < 5 * ureg.km
            else altitude_5km_indices[-1]
        )
        ax.annotate(
            "",
            xy=(result["x"][altitude_5km_index], result["h"][altitude_5km_index]),
            xytext=(result["x"][0], result["h"][altitude_5km_index]),
            arrowprops=dict(arrowstyle="<->", ls="-.", lw=1, color="b"),
        )
        ax.text(
            (result["x"][0] + result["x"][altitude_5km_index]) / 2,
            result["h"][altitude_5km_index]
            - 0.5 * ureg.km,  # Offset text vertically for better visibility
            f"Distance {np.round(result['x'][altitude_5km_index].to(ureg.km), 1):~} @ 5 km",
            rotation=0,
            horizontalalignment="center",
            bbox=dict(facecolor="lightblue", alpha=0.5),
        )

    plt.legend()
    plt.show()


def plot_altitude_vs_tas(result, phase):
    """
    Plots altitude versus true airspeed (TAS) for a given flight phase.

    This function generates a plot of altitude against TAS, with annotations
    for specific altitudes and TAS values depending on the flight phase
    (e.g., climb, descent, or descent_approach). The plot includes gridlines,
    units for axes, and annotations for key points such as TAS at specific
    altitudes and crossover altitude.

    Parameters:
    -----------
    result : dict
        A dictionary containing flight data. Expected keys:
        - "v_ias": list of indicated airspeeds (IAS) (if phase is "descent_approach").
        - "v_tas": list of true airspeeds (TAS) (if phase is not "descent_approach").
        - "h": list of altitudes (in compatible units with `ureg`).

    phase : str
        The flight phase for which the plot is generated. Possible values:
        - "climb": Adds annotations for TAS at initial altitude and crossover altitude.
        - "descent": Adds annotations for TAS at final altitude.
        - "descent_approach": Computes TAS from IAS and altitude, and adds annotations.

    Annotations:
    ------------
    - TAS at 5 km altitude (if available).
    - TAS at 10 km altitude (if available).
    - Crossover altitude where TAS is maximum (for non-"descent_approach" phases).
    - TAS at initial altitude (for "climb" phase).
    - TAS at final altitude (for "descent" phase).

    Returns:
    --------
    None
        Displays the plot with annotations.

    Notes:
    ------
    - The function uses `pint`'s `ureg` for unit handling.
    - The `cas2tas` function is used to compute TAS from IAS and altitude
      during the "descent_approach" phase.
    - The plot includes major and minor gridlines for better readability.
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    tas = (
        ureg.Quantity.from_list(
            [cas2tas(v_ias, h) for v_ias, h in zip(result["v_ias"], result["h"])]
        )
        if phase == "descent_approach"
        else result["v_tas"]
    )
    ax.plot(np.round(tas, 1), result["h"], label="Altitude vs TAS")
    ax.set_title("Altitude vs True Airspeed")
    ax.xaxis.set_units(ureg.m / ureg.s)
    ax.yaxis.set_units(ureg.km)

    # Add major and minor gridlines
    ax.grid(which="major", color="k", linestyle="-.", linewidth=0.5)
    ax.grid(which="minor", color="gray", linestyle=":", linewidth=0.4)
    ax.minorticks_on()

    # Add annotation for TAS at 5 km altitude
    altitude_5km_indices = np.where(result["h"] >= 5 * ureg.km)[0]
    if len(altitude_5km_indices) > 0:
        altitude_5km_index = (
            altitude_5km_indices[0] if phase == "climb" else altitude_5km_indices[-1]
        )
        tas_5km = tas[altitude_5km_index]
        ax.annotate(
            f"TAS: {np.round(tas_5km.to(ureg.m / ureg.s), 1):~}\n@ Alt: {np.round(result['h'][altitude_5km_index].to(ureg.km), 1):~}",
            xy=(tas_5km, result["h"][altitude_5km_index]),
            xytext=(
                tas_5km + 10 * ureg.m / ureg.s,
                result["h"][altitude_5km_index] - 0.5 * ureg.km,
            ),
            arrowprops=dict(facecolor="blue", arrowstyle="->"),
            bbox=dict(facecolor="lightblue", alpha=0.5, edgecolor="blue"),
        )

    # Add annotation for TAS at 10 km altitude
    altitude_10km_indices = np.where(result["h"] >= 10 * ureg.km)[0]
    if len(altitude_10km_indices) > 0:
        altitude_10km_index = altitude_10km_indices[0]
        tas_10km = tas[altitude_10km_index]
        ax.annotate(
            f"TAS: {np.round(tas_10km.to(ureg.m / ureg.s), 1):~}\n@ Alt: {np.round(result['h'][altitude_10km_index].to(ureg.km), 1):~}",
            xy=(tas_10km, result["h"][altitude_10km_index]),
            xytext=(
                tas_10km + 10 * ureg.m / ureg.s,
                result["h"][altitude_10km_index] - 0.5 * ureg.km,
            ),
            arrowprops=dict(facecolor="green", arrowstyle="->"),
            bbox=dict(facecolor="lightgreen", alpha=0.5, edgecolor="green"),
        )

    # Add annotation for crossover altitude (where TAS is maximum)
    if phase != "descent_approach":
        max_tas_index = np.argmax(tas)
        max_tas = tas[max_tas_index]
        crossover_altitude = result["h"][max_tas_index]
        ax.annotate(
            f"Crossover TAS: {np.round(max_tas.to(ureg.m / ureg.s), 1):~}\n@ Alt: {np.round(crossover_altitude.to(ureg.km), 1):~}",
            xy=(max_tas, crossover_altitude),
            xytext=(max_tas + 10 * ureg.m / ureg.s, crossover_altitude - 0.5 * ureg.km),
            arrowprops=dict(facecolor="red", arrowstyle="->"),
            bbox=dict(facecolor="lightcoral", alpha=0.5, edgecolor="red"),
        )

    # for climb phase, add annotation for TAS at initial altitude
    if phase == "climb":
        initial_tas = tas[0]
        initial_altitude = result["h"][0]
        ax.annotate(
            f"TAS: {np.round(initial_tas.to(ureg.m / ureg.s), 1):~}\n@ Alt: {np.round(initial_altitude.to(ureg.km), 1):~}",
            xy=(initial_tas, initial_altitude),
            xytext=(
                initial_tas + 10 * ureg.m / ureg.s,
                initial_altitude - 0.5 * ureg.km,
            ),
            arrowprops=dict(facecolor="purple", arrowstyle="->"),
            bbox=dict(facecolor="purple", alpha=0.5, edgecolor="purple"),
        )

    # for descent phase, add annotation for TAS at final altitude
    if phase == "descent":
        final_tas = tas[-1]
        final_altitude = result["h"][-1]
        ax.annotate(
            f"TAS: {np.round(final_tas.to(ureg.m / ureg.s), 1):~}\n@ Alt: {np.round(final_altitude.to(ureg.km), 1):~}",
            xy=(final_tas, final_altitude),
            xytext=(
                final_tas + 10 * ureg.m / ureg.s,
                final_altitude - 0.5 * ureg.km,
            ),
            arrowprops=dict(facecolor="purple", arrowstyle="->"),
            bbox=dict(facecolor="purple", alpha=0.5, edgecolor="purple"),
        )

    plt.legend()
    plt.show()


def plot_mach_vs_time(result):
    """
    Plots the Mach number versus time and annotates the point where the Mach number
    first reaches or leaves the constant cruise Mach of 0.85.

    Parameters:
    -----------
    result : dict
        A dictionary containing the following keys:
        - "t" : array-like
            Time values (assumed to be in compatible units with `ureg`).
        - "mach" : array-like
            Corresponding Mach number values.

    Notes:
    ------
    - During the climb phase, the annotation marks the time when the Mach number
      first reaches the cruise Mach of 0.85.
    - During the descent phase, the annotation marks the time when the Mach number
      last leaves the cruise Mach of 0.85.
    - The plot includes major and minor gridlines for better readability.

    Returns:
    --------
    None
        Displays the plot with annotations.
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(result["t"], result["mach"], label="Mach Number")
    ax.set_title("Mach number vs Time")
    ax.xaxis.set_units(ureg.min)
    ax.set_ylabel("Mach")

    # Add major and minor gridlines
    ax.grid(which="major", color="k", linestyle="-.", linewidth=0.5)
    ax.grid(which="minor", color="gray", linestyle=":", linewidth=0.4)
    ax.minorticks_on()

    # Find the time when Mach first reaches constant cruise Mach of 0.85
    cruise_mach = 0.85
    rounded_mach = np.round(result["mach"], 2)  # Round Mach values to 2 decimal places
    mach_indices = np.where(rounded_mach >= cruise_mach)[0]
    if len(mach_indices) > 0:
        if result["mach"][0] < cruise_mach:  # Climb phase
            start_time = result["t"][mach_indices[0]]
            annotation_text = "Crossover to Cruise Mach"
            text_offset = -0.2
        else:  # Descent phase
            start_time = result["t"][mach_indices[-1]]
            annotation_text = "Crossover from Cruise Mach"
            text_offset = 0.2

        # Add annotation with arrow pointing from text to the point
        ax.annotate(
            f"Time: {np.round(start_time.to(ureg.min), 1):~}\n{annotation_text}",
            xy=(start_time, cruise_mach),  # Point of interest
            xytext=(
                start_time,
                cruise_mach - 0.2,  # Text positioned below the point
            ),
            arrowprops=dict(facecolor="blue", arrowstyle="->", lw=1.5),
            bbox=dict(facecolor="lightblue", alpha=0.5, edgecolor="blue"),
            horizontalalignment="center",
            verticalalignment="center",
            color="blue",
        )

    plt.legend()
    plt.show()


def plot_tas_vs_time(result, phase):
    """
    Plots True Airspeed (TAS) versus time with annotations for key points.

    Parameters:
        result (dict): A dictionary containing simulation results with the following keys:
            - "t": Array of time values (assumed to be in units compatible with `ureg`).
            - "v_tas": Array of True Airspeed (TAS) values (assumed to be in units compatible with `ureg`).
            - "h": Array of altitude values (assumed to be in units compatible with `ureg`).
        phase (str): The flight phase, either "climb" or "descent". Determines annotation positioning.

    Annotations:
        - Crossover TAS: The maximum TAS value in the dataset.
        - TAS at 10 km altitude: The TAS value when the altitude reaches 10 km.
        - TAS at 5 km altitude: The TAS value when the altitude reaches 5 km.

    Features:
        - Major and minor gridlines for better readability.
        - Annotations with arrows and styled bounding boxes for key points.
        - Units for axes are set using `ureg` (assumed to be a Pint UnitRegistry instance).

    Returns:
        None: Displays the plot with annotations.
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(result["t"], result["v_tas"], label="True Airspeed")
    ax.set_title("TAS vs Time")  # Add padding to avoid overlap with annotations
    ax.xaxis.set_units(ureg.min)
    ax.yaxis.set_units(ureg.m / ureg.s)

    # Add major and minor gridlines
    ax.grid(which="major", color="k", linestyle="-.", linewidth=0.5)
    ax.grid(which="minor", color="gray", linestyle=":", linewidth=0.4)
    ax.minorticks_on()

    # Add annotation for crossover TAS (where TAS is maximum)
    max_tas = max(result["v_tas"])
    max_time = result["t"][np.argmax(result["v_tas"])]
    ax.annotate(
        f"Crossover TAS: {np.round(max_tas.to(ureg.m / ureg.s), 1):~}",
        xy=(max_time, max_tas),
        xytext=(
            max_time - 2 * ureg("min"),
            max_tas - 15 * ureg("m/s"),
        ),  # Adjusted position for better visibility
        arrowprops=dict(facecolor="red", arrowstyle="->"),
        bbox=dict(facecolor="lightcoral", alpha=0.5, edgecolor="red"),
    )

    # Add annotation for TAS at 10 km altitude
    altitude_10km_index = np.where(result["h"] >= 10 * ureg.km)[0][0]
    tas_10km = result["v_tas"][altitude_10km_index]
    if phase == "climb":
        xytext_offset = (
            result["t"][altitude_10km_index] + 2 * ureg("min"),
            tas_10km - 10 * ureg("m/s"),
        )
    else:  # descent
        xytext_offset = (
            result["t"][altitude_10km_index] - 5 * ureg("min"),
            tas_10km - 10 * ureg("m/s"),
        )
    ax.annotate(
        f"TAS: {np.round(tas_10km.to(ureg.m / ureg.s), 1):~}\n@ Alt: 10 km",
        xy=(result["t"][altitude_10km_index], tas_10km),
        xytext=xytext_offset,  # Adjusted position based on phase
        arrowprops=dict(facecolor="blue", arrowstyle="->"),
        bbox=dict(facecolor="lightblue", alpha=0.5, edgecolor="blue"),
    )

    # Add annotation for TAS at 5 km altitude
    altitude_5km_indices = np.where(result["h"] >= 5 * ureg.km)[0]
    if len(altitude_5km_indices) > 0:
        altitude_5km_index = (
            altitude_5km_indices[0] if phase == "climb" else altitude_5km_indices[-1]
        )
        tas_5km = result["v_tas"][altitude_5km_index]
        ax.annotate(
            f"TAS: {np.round(tas_5km.to(ureg.m / ureg.s), 1):~}\n@ Alt: 5 km",
            xy=(result["t"][altitude_5km_index], tas_5km),
            xytext=(
                result["t"][altitude_5km_index] - 2 * ureg("min"),
                tas_5km + 10 * ureg("m/s"),
            ),  # Adjusted position for better visibility
            arrowprops=dict(facecolor="green", arrowstyle="->"),
            bbox=dict(facecolor="lightgreen", alpha=0.5, edgecolor="green"),
        )
    plt.legend()
    plt.show()


def plot_fuel_burn_vs_time(result):
    """
    Plots the fuel burn versus time and annotates key information on the plot.

    Parameters:
    -----------
    result : dict
        A dictionary containing the simulation results with the following keys:
        - "t" : array-like
            Time values (assumed to be in units compatible with `ureg.min`).
        - "fuel_burn" : array-like
            Fuel burn values (assumed to be in units compatible with `ureg.kg`).
        - "h" : array-like
            Altitude values (assumed to be in units compatible with `ureg.km`).

    Description:
    ------------
    This function generates a plot of fuel burn versus time. It includes:
    - Major and minor gridlines for better readability.
    - A double-arrow annotation indicating the total fuel burn over the entire time period.
    - A text box displaying the total fuel burn value.
    - An optional annotation and text box for the fuel burn at an altitude of 5 km, if such data exists in the input.

    The annotations use arrows and text boxes with customized styles for clarity.

    Returns:
    --------
    None
        Displays the plot.
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(result["t"], result["fuel_burn"], label="Fuel Burn")
    ax.set_title("Fuel Burn vs Time")
    ax.xaxis.set_units(ureg.min)
    ax.yaxis.set_units(ureg.kg)

    # Add major and minor gridlines
    ax.grid(which="major", color="k", linestyle="-.", linewidth=0.5)
    ax.grid(which="minor", color="gray", linestyle=":", linewidth=0.4)
    ax.minorticks_on()

    # Add annotation with double arrow
    total_fuel_burn = result["fuel_burn"][-1]
    ax.annotate(
        "",
        xy=(result["t"][-1], total_fuel_burn),
        xytext=(result["t"][-1], result["fuel_burn"][0]),
        arrowprops=dict(arrowstyle="<->", color="r", lw=1.5),
    )
    ax.text(
        result["t"][-1],
        (result["fuel_burn"][0] + total_fuel_burn) / 2,
        f"Total Fuel Burn: {np.round(total_fuel_burn.to(ureg.kg), 1):~}",
        horizontalalignment="center",
        verticalalignment="center",
        bbox=dict(facecolor="wheat", alpha=0.5),
    )

    # Add annotation for fuel burn at altitude of 5 km
    altitude_5km_indices = np.where(result["h"] >= 5 * ureg.km)[0]
    if len(altitude_5km_indices) > 0:
        altitude_5km_index = (
            altitude_5km_indices[0]
            if result["h"][0] < 5 * ureg.km
            else altitude_5km_indices[-1]
        )
        fuel_burn_5km = result["fuel_burn"][altitude_5km_index]
        ax.annotate(
            "",
            xy=(result["t"][altitude_5km_index], fuel_burn_5km),
            xytext=(result["t"][altitude_5km_index], result["fuel_burn"][0]),
            arrowprops=dict(arrowstyle="<->", color="b", lw=1.5),
        )
        ax.text(
            result["t"][altitude_5km_index],
            (result["fuel_burn"][0] + fuel_burn_5km) / 2,
            f"Fuel Burn to 5 km Altitude: {np.round(fuel_burn_5km.to(ureg.kg), 1):~}",
            horizontalalignment="center",
            verticalalignment="center",
            bbox=dict(facecolor="lightblue", alpha=0.5),
        )
    plt.legend()
    plt.show()


def plot_gamma_vs_time(result, phase):
    """
    Plots the flight path angle (gamma) or descent angle versus time for a given flight phase.
    Parameters:
    -----------
    result : dict
        A dictionary containing simulation results with the following keys:
        - "t": Time array (assumed to be in units compatible with `ureg`).
        - "gamma": Flight path angle array (in radians).
        - "h": Altitude array (assumed to be in units compatible with `ureg`).
    phase : str
        The flight phase, either "climb" or "descent". Determines the sign of the
        flight path angle and the labels for the plot.
    Behavior:
    ---------
    - The function generates a plot of the flight path angle (or descent angle) versus time.
    - It adjusts the sign of the flight path angle based on the flight phase.
    - The plot includes major and minor gridlines for better readability.
    - Annotates the flight path angle at altitudes of 5 km and 10 km with arrows and text.
    Notes:
    ------
    - The function assumes that the `result` dictionary contains altitude values (`h`)
      in units compatible with `ureg.km`.
    - The time values (`t`) are assumed to be in units compatible with `ureg.min`.
    - The function uses `matplotlib` for plotting and requires `ureg` for unit handling.
    Returns:
    --------
    None
        Displays the plot directly.
    """

    fig, ax = plt.subplots(figsize=(10, 5))
    gamma = (
        -np.degrees(result["gamma"])
        if phase == "descent"
        else np.degrees(result["gamma"])
    )
    ax.plot(
        result["t"],
        gamma,
        label="Descent Angle" if phase == "descent" else "Flight Path Angle",
    )
    ax.set_title(
        "Descent Angle vs Time" if phase == "descent" else "Flight Path Angle vs Time"
    )
    ax.xaxis.set_units(ureg.min)
    ax.yaxis.set_units(ureg.deg)

    # Add major and minor gridlines
    ax.grid(which="major", color="k", linestyle="-.", linewidth=0.5)
    ax.grid(which="minor", color="gray", linestyle=":", linewidth=0.4)
    ax.minorticks_on()

    # Add annotation for flight path angle at 5 km, and at 10 km
    altitude_5km_indices = np.where(result["h"] >= 5 * ureg.km)[0]
    if len(altitude_5km_indices) > 0:
        altitude_5km_index = (
            altitude_5km_indices[0] if phase == "climb" else altitude_5km_indices[-1]
        )
        gamma_5km = gamma[altitude_5km_index]
        if phase == "descent":
            xytext_offset = (
                result["t"][altitude_5km_index].to(ureg.min) - 0.5 * ureg.min,
                gamma_5km + 0.5 * ureg.deg,
            )
        else:  # climb
            xytext_offset = (
                result["t"][altitude_5km_index].to(ureg.min) - 0.5 * ureg.min,
                gamma_5km - 0.5 * ureg.deg,
            )
        ax.annotate(
            f"@ 5 km: {np.round(gamma_5km, 1)}°",
            xy=(result["t"][altitude_5km_index].to(ureg.min), gamma_5km),
            xytext=xytext_offset,
            arrowprops=dict(facecolor="blue", arrowstyle="->"),
            bbox=dict(facecolor="lightblue", alpha=0.5),
        )
    altitude_10km_index = np.where(result["h"] >= 10 * ureg.km)[0][0]
    gamma_10km = gamma[altitude_10km_index]
    if phase == "descent":
        xytext_offset = (
            result["t"][altitude_10km_index].to(ureg.min) - 0.5 * ureg.min,
            gamma_10km + 0.5 * ureg.deg,
        )
    else:  # climb
        xytext_offset = (
            result["t"][altitude_10km_index].to(ureg.min) - 0.5 * ureg.min,
            gamma_10km - 0.5 * ureg.deg,
        )
    ax.annotate(
        f"@ 10 km: {np.round(gamma_10km, 1)}°",
        xy=(result["t"][altitude_10km_index].to(ureg.min), gamma_10km),
        xytext=xytext_offset,
        arrowprops=dict(facecolor="green", arrowstyle="->"),
        bbox=dict(facecolor="lightgreen", alpha=0.5),
    )
    plt.legend()
    plt.show()


def plot_aoa_vs_time(result):
    """
    Plots the angle of attack (AoA) versus time from the simulation results for approach phase of the descent.

    This function generates a plot of the angle of attack (AoA) against time,
    with annotations for the start and end of the simulation phase. The plot
    includes gridlines, units for the axes, and a legend.

    Parameters:
    -----------
    result : dict
        A dictionary containing the simulation results with the following keys:
        - "t": Time values (assumed to be in units compatible with `ureg.min`).
        - "aoa": Angle of attack values (assumed to be in units compatible with `ureg.deg`).
        - "h": Altitude values (assumed to be in units compatible with `ureg.km` and `ureg.ft`).

    Notes:
    ------
    - The function uses `matplotlib` for plotting.
    - The `ureg` object is assumed to be a unit registry (e.g., from the `pint` library)
      for handling units.
    - The `np` object is assumed to be the `numpy` library.

    Annotations:
    ------------
    - The start of the simulation phase is annotated with the AoA and altitude
      at the first time step.
    - The end of the approach phase is annotated with the AoA and altitude
      at the last time step.

    Gridlines:
    ----------
    - Major gridlines are styled with a dashed-dot line.
    - Minor gridlines are styled with a dotted line.

    Returns:
    --------
    None
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(result["t"], result["aoa"], label="Angle of Attack")
    ax.set_title("AoA (Angle of Attack) vs Time")
    ax.xaxis.set_units(ureg.min)
    ax.yaxis.set_units(ureg.deg)

    # Add major and minor gridlines
    ax.grid(which="major", color="k", linestyle="-.", linewidth=0.5)
    ax.grid(which="minor", color="gray", linestyle=":", linewidth=0.4)
    ax.minorticks_on()

    # Add annotation for start of simulation phase
    ax.annotate(
        f"AoA: {np.round(result['aoa'][0].to(ureg.deg).m, 1)}°\n@ Alt: {np.round(result['h'][0].to(ureg.km), 1):~}",
        xy=(result["t"][0], result["aoa"][0]),
        xytext=(result["t"][0], result["aoa"][0] - 0.5 * ureg.deg),
        arrowprops=dict(facecolor="green", arrowstyle="->"),
        bbox=dict(facecolor="lightgreen", alpha=0.5, edgecolor="green"),
    )

    # Add annotation for end of approach phase
    ax.annotate(
        f"AoA: {np.round(result['aoa'][-1].to(ureg.deg).m, 1)}°\n@ Alt: {np.round(result['h'][-1].to(ureg.ft), 1):~}",
        xy=(result["t"][-1], result["aoa"][-1]),
        xytext=(result["t"][-1] - 0.5 * ureg.min, result["aoa"][-1] + 0.5 * ureg.deg),
        arrowprops=dict(facecolor="red", arrowstyle="->"),
        bbox=dict(facecolor="lightcoral", alpha=0.5, edgecolor="red"),
    )

    plt.legend()
    plt.show()


def plot_pitch_angle_vs_time(result):
    """
    Plots the pitch angle (in degrees) versus time (in minutes) from the given simulation results for approach phase of the descent.

    The function creates a line plot of the pitch angle over time, adds gridlines, and annotates
    the pitch angle and altitude at the start and end of the approach phase.

    Parameters:
    -----------
    result : dict
        A dictionary containing the simulation results with the following keys:
        - "t" : array-like
            Time values (assumed to be in units compatible with `ureg.min`).
        - "theta" : array-like
            Pitch angle values (assumed to be in units compatible with `ureg.rad`).
        - "h" : array-like
            Altitude values (assumed to be in units compatible with `ureg.km` or `ureg.ft`).

    Annotations:
    ------------
    - The pitch angle and altitude at the start of the approach phase are annotated with a blue arrow.
    - The pitch angle and altitude at the end of the approach phase are annotated with a red arrow.

    Gridlines:
    ----------
    - Major gridlines are styled with a black dashed line.
    - Minor gridlines are styled with a gray dotted line.

    Returns:
    --------
    None
        Displays the plot.

    Notes:
    ------
    - The function assumes that the `result` dictionary contains quantities with units
      compatible with the `pint` library (`ureg`).
    - The `ureg` object and `np` (NumPy) must be imported and properly configured in the
      script where this function is used.
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(result["t"], np.degrees(result["theta"]), label="Pitch Angle")
    ax.set_title("Pitch Angle vs Time")
    ax.xaxis.set_units(ureg.min)
    ax.yaxis.set_units(ureg.deg)

    # Add major and minor gridlines
    ax.grid(which="major", color="k", linestyle="-.", linewidth=0.5)
    ax.grid(which="minor", color="gray", linestyle=":", linewidth=0.4)
    ax.minorticks_on()

    # Add annotation for pitch angle at the start of approach phase
    ax.annotate(
        f"Pitch: {np.round(result['theta'][0].to('deg').m, 1)}°\n@ Alt: {np.round(result['h'][0].to(ureg.km), 1):~}",
        xy=(result["t"][0], np.degrees(result["theta"][0])),
        xytext=(
            result["t"][0] + 0.5 * ureg.min,
            np.degrees(result["theta"][0]) - 1 * ureg.deg,
        ),
        arrowprops=dict(facecolor="blue", arrowstyle="->"),
        bbox=dict(facecolor="lightblue", alpha=0.5, edgecolor="blue"),
    )

    # Add annotation for pitch angle at the end of approach phase
    ax.annotate(
        f"Pitch: {np.round(result['theta'][-1].to('deg').m, 1)}°\n@ Alt: {np.round(result['h'][-1].to(ureg.ft), 1):~}",
        xy=(result["t"][-1], np.degrees(result["theta"][-1])),
        xytext=(
            result["t"][-1] - 1 * ureg.min,
            np.degrees(result["theta"][-1]) + 1 * ureg.deg,
        ),
        arrowprops=dict(facecolor="red", arrowstyle="->"),
        bbox=dict(facecolor="lightcoral", alpha=0.5, edgecolor="red"),
    )
    plt.legend()
    plt.show()


def plot_thrust_vs_time(result):
    """
    Plots thrust versus time and annotates the start and end of the approach phase of the descent.

    Parameters:
    -----------
    result : dict
        A dictionary containing the following keys:
        - "t" : array-like
            Time data (assumed to be in units compatible with `ureg.min`).
        - "thrust" : array-like
            Thrust data (assumed to be in units compatible with `ureg.N`).
        - "h" : array-like
            Altitude data (assumed to be in units compatible with `ureg.km` or `ureg.ft`).

    Features:
    ---------
    - Plots thrust as a function of time.
    - Adds major and minor gridlines for better readability.
    - Annotates the start of the approach phase with thrust and altitude information.
    - Annotates the end of the approach phase with thrust and altitude information.
    - Uses arrows and styled bounding boxes for annotations.

    Notes:
    ------
    - The function assumes that the `result` dictionary contains data in compatible units
      with the `ureg` unit registry.
    - The annotations include thrust values converted to kilonewtons (kN) and altitude
      values converted to kilometers (km) or feet (ft) as appropriate.

    Dependencies:
    -------------
    - Requires `matplotlib.pyplot` as `plt`.
    - Requires `numpy` as `np`.
    - Requires a unit registry object `ureg` for handling units.
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(result["t"], result["thrust"], label="Thrust")
    ax.set_title("Thrust vs Time")
    ax.xaxis.set_units(ureg.min)
    ax.yaxis.set_units(ureg.N)

    # Add major and minor gridlines
    ax.grid(which="major", color="k", linestyle="-.", linewidth=0.5)
    ax.grid(which="minor", color="gray", linestyle=":", linewidth=0.4)
    ax.minorticks_on()

    # Add annotation for start of approach phase
    ax.annotate(
        f"Start of Approach\nThrust: {np.round(result['thrust'][0].to(ureg.kN), 1):~}\n@ Alt: {np.round(result['h'][0].to(ureg.km), 1):~}",
        xy=(result["t"][0], result["thrust"][0]),
        xytext=(
            result["t"][0],
            result["thrust"][0] - 0.05 * result["thrust"][0],
        ),
        arrowprops=dict(facecolor="blue", arrowstyle="->"),
        bbox=dict(facecolor="lightblue", alpha=0.5, edgecolor="blue"),
    )

    # Add annotation for end of approach phase
    ax.annotate(
        f"End of Approach\nThrust: {np.round(result['thrust'][-1].to(ureg.kN), 1):~}\n@ Alt: {np.round(result['h'][-1].to(ureg.ft), 1):~}",
        xy=(result["t"][-1], result["thrust"][-1]),
        xytext=(
            result["t"][-1] - 1 * ureg.min,  # Move left by 1 minute
            result["thrust"][-1] + 0.05 * result["thrust"][-1],
        ),
        arrowprops=dict(facecolor="red", arrowstyle="->"),
        bbox=dict(facecolor="lightcoral", alpha=0.5, edgecolor="red"),
    )
    plt.legend()
    plt.show()


def plot_ias_vs_altitude(result, phase):
    """
    Plots Indicated Airspeed (IAS) versus Altitude for a given flight phase.

    Parameters:
        result (dict): A dictionary containing flight data.
                       Expected keys are:
                       - "h": Altitude data (array-like).
                       - "v_ias": Indicated Airspeed data (array-like).
        phase (str): The flight phase, either "climb", "descent", or "descent_approach"
                     If the phase is "climb" or "descent", the IAS values are rounded.

    Returns:
        None: Displays a plot of IAS vs Altitude.

    Notes:
        - The x-axis represents altitude and uses units of kilometers (km).
        - The y-axis represents indicated airspeed and uses units of meters per second (m/s).
        - The plot includes major and minor gridlines for better readability.
        - A legend is added to identify the plotted data.

    Example:
        plot_ias_vs_altitude(result={"h": [0, 1, 2], "v_ias": [100, 150, 200]}, phase="climb")
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    ias = (
        np.round(result["v_ias"]) if phase in ["climb", "descent"] else result["v_ias"]
    )
    ax.plot(result["h"], ias, label="Indicated Airspeed")
    ax.set_title("IAS (Indicated Airspeed) vs Altitude")
    ax.xaxis.set_units(ureg.km)
    ax.yaxis.set_units(ureg.m / ureg.s)

    # Add major and minor gridlines
    ax.grid(which="major", color="k", linestyle="-.", linewidth=0.5)
    ax.grid(which="minor", color="gray", linestyle=":", linewidth=0.4)
    ax.minorticks_on()

    plt.legend()
    plt.show()
