import numpy as np
from pylablib.devices.Thorlabs.elliptec import ElliptecMotor
import serial
from photonicdrivers.Abstract.Connectable import Connectable
import pylablib.devices.Thorlabs.elliptec as ello
from photonicdrivers.RotationMounts.Elliptec_Driver import Elliptec_Driver

class Elliptec_Rotation_Mount():
    """
    Class for controlling ELL14 rotation stage.
    """

    def __init__(self, driver: Elliptec_Driver, address = None):
        """
        Initializes the ELL14 instance with the specified port and address.

        Args:
            port (str): The connection port for the rotation stage.
            address (str): The address of the rotation stage (default is 'all'). Must be between 0 and 15. Addresses above 10 represent letters (A, B, C, D, E, F) but cannot be used.
        """
        self.driver: Elliptec_Driver = driver
        self.address = address
        if self.address is None:
            self.address = self.driver.get_address()[0]

    def move_to(self, angle: float) -> None:
        """
        Moves the rotation stage to a specific angle.

        Args:
            angle (float): The target angle in degrees.
        """
        if angle < -360:
            angle = np.mod(angle, -360)
        if angle > 360:
            angle = np.mod(angle, 360)
        self.driver.move_to(angle, self.address)

    def move_by(self, angle: float) -> None:
        """
        Moves the rotation stage by a specified angle.

        Args:
            angle (float): The angle to move by, in degrees.
        """
        self.driver.move_by(angle, self.address)

    def home(self) -> None:
        """
        Homes the rotation stage, returning it to the reference position.
        """
        self.driver.home(self.address)

    def get_position(self) -> float:
        """
        Retrieves the current position of the rotation stage.

        Returns:
            float: The current position in degrees.
        """
        return self.driver.get_position(self.address)


if __name__ == "__main__":
    driver = Elliptec_Driver(port="COM8", addresses=[10,11,12,13])
    driver.connect()
    rotation_mount_1 = Elliptec_Rotation_Mount(driver= driver, address=10)
    rotation_mount_2 = Elliptec_Rotation_Mount(driver= driver, address=11)
    rotation_mount_3 = Elliptec_Rotation_Mount(driver= driver, address=12)
    rotation_mount_4 = Elliptec_Rotation_Mount(driver= driver, address=13)

    print(rotation_mount_1.get_position())    
    rotation_mount_1.move_to(90)
    rotation_mount_1.move_by(90)
    print(rotation_mount_1.get_position()) 

    print(rotation_mount_2.get_position())    
    rotation_mount_2.move_to(90)
    rotation_mount_2.move_by(90)
    print(rotation_mount_2.get_position()) 

    print(rotation_mount_3.get_position())    
    rotation_mount_3.move_to(90)
    rotation_mount_3.move_by(90)
    print(rotation_mount_3.get_position())  
      
    print(rotation_mount_4.get_position())    
    rotation_mount_4.move_to(90)
    rotation_mount_4.move_by(90)
    print(rotation_mount_4.get_position())   
    
    driver.disconnect()

# if __name__ == "__main__":

#     slider_mount = ELL6(port="COM10", address=[10])
#     slider_mount.connect()
#     print(slider_mount.get_address())
#     print(slider_mount.is_connected())
#     print(slider_mount.move_to(1))
#     print(slider_mount.get_position())
#     slider_mount.disconnect()
#     print(slider_mount.is_connected())

    
# if __name__ == "__main__":

#     rotation_mount = ELL14(port="COM9", address=[5])
#     rotation_mount.connect()
#     print(rotation_mount.get_address())
#     print(rotation_mount.get_position())    
#     print(rotation_mount.is_connected())
#     rotation_mount.move_to(90)
#     rotation_mount.move_by(90)
#     rotation_mount.disconnect()
#     print(rotation_mount.is_connected())





