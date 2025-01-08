
### Load libraries
import sys
import time
import numpy as np


import numpy as np
import matplotlib.pyplot as plt
from photonicdrivers.utils.Range import Range

try:
    sys.path.append(r"C:\\Program Files\\Andor SDK\\Python\\pyAndorSpectrograph")
    sys.path.append(r"C:\\Program Files\\Andor SDK\\Python\\pyAndorSDK2")
    from pyAndorSDK2 import atmcd, atmcd_codes, atmcd_errors
    codes = atmcd_codes
except:
    print("Andor Solis is not installed ")



class Andor_Newton:

    def __init__(self) -> None:
        self.camera = atmcd(userPath="C:\\Program Files\\Andor SDK\\Python\\pyAndorSDK2\\pyAndorSDK2\\libs\\Windows\\64")
        self.num_pixel_y = 200
        self.num_pixel_x = 1600

    def connect(self):
        self.camera.Initialize("")
        self.camera.SetReadMode(4)
        self.camera.SetImage(1,1,1,self.num_pixel_x,1,self.num_pixel_y)
        self.camera.SetAcquisitionMode(codes.Acquisition_Mode.SINGLE_SCAN)
        self.set_temperature(-70)
        self.cooler_on()
        self.set_exposure_time_s(0.1)
        self.roi = [49,53]

    def set_exposure_time_s(self, exposure_time_s):
        self.camera.SetExposureTime(exposure_time_s)

    def get_exposure_time_s(self):
        (message, exposure_time) = self.camera.GetMaximumExposure()
        return exposure_time

    def get_image(self):
        self.camera.PrepareAcquisition()
        self.camera.StartAcquisition()
        self.camera.WaitForAcquisition()
        (ret, arr, validfirst, validlast) = self.camera.GetImages(1,1, size=self.num_pixel_x*self.num_pixel_y)
        image = np.flip(np.flip(np.reshape(arr, (self.num_pixel_y, self.num_pixel_x)), axis=1),axis=0)
        return image

    def get_ROI_counts(self):
        '''return an array of counts from the image where we sum all rows within the region of interest (ROI)'''
        image = self.get_image()
        return np.sum(image[self.roi[0]:self.roi[1]], axis=0)/(self.roi[1] - self.roi[0])

    def get_trace(self):
        image = self.get_image()
        trace = np.sum(image, axis=0)
        return trace.tolist()

    def cooler_on(self):
        self.camera.CoolerON()

    def coolor_off(self):
        self.camera.CoolerOFF()

    def set_temperature(self, temperature_celsius):
        self.camera.SetTemperature(temperature_celsius)

    def get_temperature(self):
        (message, temperature) = self.camera.GetTemperature()
        return temperature

    def get_serial_number(self):
        (message, serial_number) = self.camera.GetCameraSerialNumber()
        return serial_number
    
    def get_id(self):
        return self.get_serial_number()

    def get_gain_range(self):
        (message, min_gain, max_gain) = self.camera.GetEMGainRange()
        return Range(min_gain, max_gain)
    
    def get_gain(self):
        """
        Get the electron multiplier (EM) gain from (0, 256)
        """
        (message, gain) = self.camera.GetEMCCDGain()
        return gain

    def set_gain(self, gain):
        gain_range = self.get_gain_range()
        if gain_range.contains(gain):
            self.camera.SetGain
        else:
            print("Gain out of range: " + gain_range)

    def disconnect(self):
        self.camera.AbortAcquisition()
    
    def is_connected(self):
        return bool(self.get_serial_number())
        
    def get_settings(self):
        return {
            "id": self.get_serial_number(),
            "temperature": self.get_temperature(),
            "gain": self.get_gain(),
            "exposure_time": self.get_exposure_time_s()
        }

