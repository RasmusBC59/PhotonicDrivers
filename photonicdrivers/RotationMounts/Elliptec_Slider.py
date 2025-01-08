import numpy as np
from pylablib.devices.Thorlabs.elliptec import ElliptecMotor
import serial
from photonicdrivers.Abstract.Connectable import Connectable
import pylablib.devices.Thorlabs.elliptec as ello
from photonicdrivers.RotationMounts.Elliptec_Driver import Elliptec_Driver

class Elliptec_Slider():
    """
    Class for controlling ELL6 rotation stage.
    """

    def __init__(self, driver: Elliptec_Driver, address = None):
        """
        Initializes the ELL6 instance with the specified port and address.

        Args:
            port (str): The connection port for the rotation stage.
            address (int): The new address to set, must be between 0 and 15.
                          Addresses above 10 represent letters (A, B, C, D, E, F) but cannot be used.
        """

        self.driver: Elliptec_Driver = driver
        self.address = address
        if self.address is None:
            self.address = self.driver.get_address()[0]

    def get_position(self) -> float:
        """
        Retrieves the current position of the ELL6 rotation stage.

        Returns:
            float: The current position.
        """
        return self.driver.get_position(address=self.address)

    def move_to_position(self, position: int) -> None:
        """
        Moves the rotation stage to a specific position (0 or 1).

        Args:
            position (int): The target position, must be either 0 or 1.

        Raises:
            ValueError: If the position is not 0 or 1.
        """
        if position not in [0, 1]:
            raise ValueError("Position must be either 0 or 1.")
        self.driver.move_to(position, address=self.address)
  

if __name__ == "__main__":
    driver = Elliptec_Driver("COM9", [10])
    driver.connect()
    slider_mount = Elliptec_Slider(driver=driver)

    print(slider_mount.get_position())

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





