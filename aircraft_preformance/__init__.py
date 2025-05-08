from pint import UnitRegistry

ureg = UnitRegistry()

preferred_units = [ureg.N]  # force

ureg.default_system = "SI"
ureg.default_preferred_units = preferred_units
