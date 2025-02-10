from photonicdrivers.BlueForsControlSoftware.BlueForsControlSoftware_Driver import BlueForsControlSoftware_Driver, OnOffError

# Must be executed on a computer running the control software
driver = BlueForsControlSoftware_Driver()
driver.connect()

get_temperatures = driver.get_temperatures()
get_pressures = driver.get_pressures()
get_valves = driver.get_valves()
get_pumps = driver.get_pumps()
get_heaters = driver.get_heaters()

for d in [get_temperatures, get_pressures, get_valves, get_pumps, get_heaters]:
    print(d)

pressure_ok = driver.get_values("pressure_ok")

print(pressure_ok)
