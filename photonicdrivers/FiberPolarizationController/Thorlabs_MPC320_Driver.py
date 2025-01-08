import clr
from photonicdrivers.utils.execution_time import execution_time
from abc import ABC, abstractmethod
import socket

# To use this driver the software Kinesis from Thorlabs must be installed to match the following
# Also consider attaching the path to settings.JSON file to access the code
try:
    clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.DeviceManagerCLI.dll")
    clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.GenericMotorCLI.dll")
    clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\ThorLabs.MotionControl.PolarizerCLI.dll")
    from Thorlabs.MotionControl.DeviceManagerCLI import *
    from Thorlabs.MotionControl.GenericMotorCLI import *
    from Thorlabs.MotionControl.PolarizerCLI import *
except:
    print("Thorlabs Kinsesis not installed or installed in the wrong location")
from System import Decimal

from photonicdrivers.Abstract.Connectable import Connectable

class Thorlabs_MPC320_Driver(Connectable):

    def __init__(self, serial_number): # serial number S/N can be found underneath the device 
        """Connect to and reset Thorlabs PM101USB"""
        DeviceManagerCLI.BuildDeviceList()
        self.polarization_controller = Polarizer.CreatePolarizer(serial_number)
        self.paddle_1 = PolarizerPaddles.Paddle1
        self.paddle_2 = PolarizerPaddles.Paddle2
        self.paddle_3 = PolarizerPaddles.Paddle3
        self.serial_number = serial_number
        self.polling_rate = 250
        self.time_out = 60000 # 60 seconds to complete move.

    def connect(self):
        self.polarization_controller.Connect(self.serial_number)
        if not self.polarization_controller.IsSettingsInitialized():
            self.polarization_controller.WaitForSettingsInitialized(10000)  # 10 second timeout.
            assert self.polarization_controller.IsSettingsInitialized() is True
        self.polarization_controller.StartPolling(self.polling_rate)  
        self.polarization_controller.EnableDevice()
    
    def set_position_0(self,position:float):
        """
        Moves the first padlets to its specified positions
        """
        self.polarization_controller.MoveTo(Decimal(position), self.paddle_1, self.time_out)

    def set_position_1(self,position:float):
        """
        Moves the first padlets to its specified positions
        """
        self.polarization_controller.MoveTo(Decimal(position), self.paddle_2, self.time_out)

    def set_position_2(self,position:float):
        """
        Moves the first padlets to its specified positions
        """
        self.polarization_controller.MoveTo(Decimal(position), self.paddle_3, self.time_out)
        
    def disconnect(self):
        pass

    def is_connected(self):
        return True
    