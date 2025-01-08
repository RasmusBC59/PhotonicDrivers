
from photonicdrivers.Spectrographs.Andor_Kymera import Andor_Kymera
from photonicdrivers.Spectrographs.Andor_Newton import Andor_Newton
import matplotlib.pyplot as plt
import numpy as np
from instruments.Implementations.Lasers.Toptica_CTL950 import Toptica_CTL950
from photonicdrivers.Lasers.Toptica.Toptica_DLC_Pro_Driver import Toptica_DLC_PRO_Driver
import time
import datetime    
import os
from configparser import ConfigParser
from mpl_toolkits.mplot3d import Axes3D
from itertools import product

class Andor_Spectrograph():

    def __init__(self, spectrograph: Andor_Kymera, camera: Andor_Newton):
        self.spectrograph: Andor_Kymera = spectrograph
        self.camera: Andor_Newton = camera
        self.calibration = None
        
    def load_settings(self) -> dict:
        pass

    def save_settings(self, settings: dict) -> None:
        pass

    def load_calibration(path):
        pass

    def calibration(pixel_list, center_wavelength):
        return


if __name__ == "__main__":

    
