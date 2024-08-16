## Python sample script to communicate with RLS Picus laser

import pyvisa
from matplotlib import pyplot as plt

from Picus import Picus

rm = pyvisa.ResourceManager()
print(rm.list_resources())

port = 'ASRL3::INSTR'

laser = Picus(_resource_manager=rm,_port=port,_connectionMethod="pyvisa")
# laser = Picus(_connectionMethod="serial")
laser.connect()
print("Enable state: " + str(laser.getEnabledState()))
print("Wavelength: " + str(laser.getWavelength()))

laser.disconnect()