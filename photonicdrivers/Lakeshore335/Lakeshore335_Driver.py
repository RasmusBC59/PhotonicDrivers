# https://pypi.org/project/lakeshore/
# https://lake-shore-python-driver.readthedocs.io/en/latest/model_335.html 

from lakeshore import Model335, Model335InputSensorSettings
from photonicdrivers.Abstract.Connectable import Connectable

class Lakeshore335_Driver(Connectable):
    def __init__(self, com_port:str, baud_rate:int=57600) -> None:
        self.port = com_port
        self.baud = baud_rate

    def connect(self) -> None:
        self.connection = Model335(57600 , com_port="COM5")
        # self.connection.connect_usb

    def disconnect(self) -> None:
        # self.connection.disconnect_usb() # it does not seem necessary to execute this command
        pass

    def is_connected(self) -> bool:
        try:
            self.get_id()
            return True
        except:
            return False

    def get_id(self) -> str:
        return self.connection.query('*IDN?')
    
    def get_all_kelvin(self) -> tuple[float]:
        '''
        Returns temperature reading in kelvin for all sensors in an array of floats
        '''
        return self.connection.get_all_kelvin_reading()