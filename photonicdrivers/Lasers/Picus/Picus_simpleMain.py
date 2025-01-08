## Python sample script to communicate with RLS Picus laser

import pyvisa

from photonicdrivers.Lasers.Picus.Picus_Driver import Picus_Driver
# from Sysstatus_external import sys_status

rm = pyvisa.ResourceManager()
print("Available devices: ")
print(rm.list_resources())

port = 'ASRL3::INSTR'

# laser = Picus_Driver(_resource_manager=rm,_port=port,_connectionMethod="pyvisa")
laser = Picus_Driver(_resource_manager=rm,_port="COM3",_connectionMethod="serial")

laser.connect()

print("Enable state: " + str(laser.getEnabledState()))

laser.setEnabledState(False)
print("Enable state: " + str(laser.getEnabledState()))

print("Wavelength: " + str(laser.getWavelength()))

laser.setEnabledState(False)
print("Enable state: " + str(laser.getEnabledState()))

laser.disconnect()