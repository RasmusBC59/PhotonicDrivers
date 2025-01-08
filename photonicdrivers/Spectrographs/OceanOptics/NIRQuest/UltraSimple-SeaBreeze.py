# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 16:49:20 2024

@author: NQCPW
"""

import seabreeze.spectrometers as sb

spec = sb.Spectrometer.from_serial_number()
sb.Spectrometer.open(spec)



spec.integration_time_micros(10000)



wls = spec.wavelengths()
cts = spec.intensities()

# import pandas 
import numpy as np
import matplotlib.pyplot as plt

plt.figure()
plt.plot(wls, cts, '.')

sb.Spectrometer.close(spec)