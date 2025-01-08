### Load libraries
import sys
import time

sys.path.append(r"C:\\Program Files\\Andor SDK\\Python\\pyAndorSDK2")
sys.path.append(r"C:\\Program Files\\Andor SDK\\Python\\pyAndorSpectrograph")

from pyAndorSDK2 import atmcd, atmcd_codes, atmcd_errors
from pyAndorSpectrograph.spectrograph import ATSpectrograph
codes = atmcd_codes

### Initialize Camera and Spectrograph ###

spc = ATSpectrograph(userPath="C:\\Program Files\\Andor SDK\\Python\\pyAndorSpectrograph\\pyAndorSpectrograph\\libs\\Windows\\64")
cam = atmcd(userPath="C:\\Program Files\\Andor SDK\\Python\\pyAndorSDK2\\pyAndorSDK2\\libs\\Windows\\64")
shm = spc.Initialize("")
ret = cam.Initialize("")
print("Function Initialize returned {}".format(
    spc.GetFunctionReturnDescription(shm, 64)[1]))

### SET READOUT MODE ###
cam.SetReadMode(4)
cam.SetImage(1,1,1,1600,1,200)

### SET ACQUISITION MODE ###
ret = cam.SetAcquisitionMode(codes.Acquisition_Mode.SINGLE_SCAN)
exposure_time = 0.5
spc.SetGrating(device=0, grating=1)
spc.SetWavelength(device=0, wavelength=940)
ret = cam.SetExposureTime(exposure_time)
ret = cam.PrepareAcquisition()
ret = cam.StartAcquisition()
ret = cam.WaitForAcquisition()


### COOL CAMERA ###
ret = cam.CoolerON()
ret = cam.SetTemperature(-65)
ret, temperature = cam.GetTemperature()
print(temperature)
print("Get Number Pixel", spc.GetNumberPixels(device=0))
print("Get Grating Info", spc.GetGratingInfo(device=0, Grating=1, maxBlazeStrLen= 12000))
print("Spectrograph Center Wavelength", spc.GetWavelength(device=0))
print("Camera Capabilities: ", cam.GetCapabilities())
print("Available Cameras: ", cam.GetAvailableCameras())
print("Current Camera: ", cam.GetCurrentCamera())
print(spc.GetWavelengthLimits(device=0, Grating=1))
print(spc.GetCalibration(device=0, NumberPixels=0))
print(spc.GetPixelCalibrationCoefficients(device=0))

### GET IMAGE ###
(ret, arr, validfirst, validlast) = cam.GetImages16(1,1, size=1600*200)

print(ret, ' ', arr)

cam.AbortAcquisition()
spc.Close()

import numpy as np
import matplotlib.pyplot as plt

# Generate a sample 1D array with length 200*1600 (for demonstration purposes)
length = 200 * 1600
array_1d = arr  # A 1D array from 0 to 255


# Reshape the 1D array to a 2D array with shape (200, 1600)
image = np.flip(np.flip(np.reshape(array_1d, (200, 1600)), axis=1),axis=0)
collapse = np.sum(image, axis=0)

# Plot the 2D array as an image
plt.imshow(image, cmap='gray', aspect='auto')
plt.colorbar()  # Add a colorbar to show the mapping of values to colors
plt.title("2D Image Representation of 1D Array")

plt.figure()
plt.plot(collapse)
plt.show()

