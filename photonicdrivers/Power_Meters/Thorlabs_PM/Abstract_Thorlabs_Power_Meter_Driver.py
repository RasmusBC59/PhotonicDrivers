
from abc import abstractmethod, ABC

class Abstract_Thorlabs_Power_Meter_Driver(ABC):

    @abstractmethod
    def connect(self):
        """
        Establishes a connection to the power meter.

        Raises:
            NotImplementedError: This method must be overridden in a subclass.
        """
        pass

    @abstractmethod
    def disconnect(self):
        """
        Disconnects from the power meter.

        Raises:
            NotImplementedError: This method must be overridden in a subclass.
        """
        pass

    @abstractmethod
    def get_detector_power(self):
        pass

    @abstractmethod
    def set_power_meter_wavelength(self, wavelength_nm: float):
        pass

    @abstractmethod
    def get_power_meter_wavelength(self):
        pass

    @abstractmethod
    def set_averaging(self, average: int):
        pass

    @abstractmethod
    def get_averaging(self):
        pass

    @abstractmethod
    def set_auto_range(self):
        pass