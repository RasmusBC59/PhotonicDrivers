from photonicdrivers.Keithley.Keithley2450_Driver import Keithley2450_Driver

ip ="10.209.67.218"
device = Keithley2450_Driver(ip)

try:
    device.connect()

    print("Identification:", device.identify())
finally:
    device.disconnect()