import pyvisa
from photonicdrivers.Power_Meters.Thorlabs_PM.Thorlabs_Power_Meter_Driver import Thorlabs_Power_Meter_Driver


"""
Class for interfacing with Thorlabs powermeters.
Supported models: N7747A; PM100D; PM100USB; THORLABS PM101A TMC (e.g., model='PM100USB')
Supported units: {'W', 'mW', 'dBm'}
"""

class Thorlabs_PM100D_Driver(Thorlabs_Power_Meter_Driver):

    def __init__(self, resource_manager: pyvisa.ResourceManager, resource_name: str) -> None:
        """
        Initializes the Thorlabs_PM100D_driver instance.

        Args:
            resource_manager (pyvisa.ResourceManager): The VISA resource manager for handling VISA resources.
            port (str): The VISA resource string for connecting to the Thorlabs PM100D power meter.
        """
        self.resource_manager = resource_manager
        self.port = resource_name
        self.powerMeter = None
        
    def connect(self) -> None:
        """
        Establishes a connection to the Thorlabs PM100D power meter.
        """
        self.powerMeter = self.resource_manager.open_resource(self.port)

    def disconnect(self) -> None:
        """
        Closes the connection to the Thorlabs PM100D power meter.
        """
        if self.powerMeter:
            self.powerMeter.close()

    def is_connected(self) -> bool:
        """
        Checks if a connection to the Thorlabs PM100D power meter is established.

        Returns:
            bool: True if the device is connected, False otherwise.
        """
        try:
            return self.get_idn() is not None
        except ConnectionError:
            return False
        except Exception:
            return False

    def get_idn(self) -> str:
        """
        Retrieves the identification string of the Thorlabs PM100D power meter.

        Returns:
            str: The response from the *IDN? command.
        """
        return self._write('*IDN?')

    def get_averaging(self) -> int:
        """
        Retrieves the current number of averaging cycles configured on the power meter.

        Returns:
            int: The number of averaging cycles.
        """
        self._write(':SENS:AVER?')
        return int(self._read())

    def set_averaging(self, average: int) -> None:
        """
        Sets the number of averaging cycles on the power meter.

        Args:
            average (int): The number of averaging cycles to set.
        """
        self._write(f':SENS:AVER {average}')

    def set_config_power(self) -> None:
        """
        Configures the power meter for power measurements.
        """
        self._write(':SENS:CONF:POW')

    def set_auto_range(self, auto_range: str = 'ON') -> None:
        """
        Sets the auto range mode of the power meter.

        Args:
            auto_range (str): 'ON' to enable auto range, 'OFF' to disable.
        """
        self._write(f':SENS:POW:RANG:AUTO {auto_range}')

    def set_beam(self, beam: str = 'MIN') -> None:
        """
        Sets the beam correction type.

        Args:
            beam (str): The beam correction type ('MIN', 'MAX', etc.).
        """
        self._write(f':SENS:CORR:BEAM {beam}')

    def set_wavelength(self, wavelength_nm: float) -> None:
        """
        Sets the detector wavelength for calibration.

        Args:
            wavelength_nm (float): The wavelength in nanometers.
        """
        self._write(f':SENS:CORR:WAV {wavelength_nm}')

    def set_power_unit(self, unit: str) -> None:
        """
        Sets the units for power measurements.

        Args:
            unit (str): The unit to set ('W', 'mW', or 'dBm').
        """
        self._write(f':SENS:POW:UNIT {unit}')

    def get_power_unit(self) -> str:
        """
        Retrieves the current units for power measurements.

        Returns:
            str: The current units ('W', 'mW', or 'dBm').
        """
        self._write(':SENS:POW:UNIT?')
        return self._read()

    def get_power(self) -> float:
        """
        Retrieves the current power measurement from the detector.

        Returns:
            float: The measured power.
        """
        self._write('MEAS:POW?')
        return float(self._read())

    def get_wavelength(self) -> float:
        """
        Retrieves the current wavelength setting of the power meter.

        Returns:
            float: The wavelength in nanometers.
        """
        self._write(':SENS:CORR:WAV?')
        return float(self._read())

    def reset(self) -> None:
        """
        Resets the power meter to its default state.
        """
        self._write('*RST')

    def zero(self) -> None:
        """
        Initiates a zero correction procedure on the detector.
        """
        self._write("SENS:CORR:COLL:ZERO:INIT")

    #################################### PRIVATE METHODS ###########################################

    def _write(self, command: str) -> str:
        """
        Sends a command to the power meter and returns the response.

        Args:
            command (str): The command string to send.

        Returns:
            str: The response from the power meter.

        Raises:
            ConnectionError: If an error occurs while sending the command.
        """
        self.powerMeter.write(command)
        return self._read()

    def _read(self) -> str:
        """
        Reads a response from the power meter, cleaning up any extraneous characters.

        Returns:
            str: The cleaned response string.

        Raises:
            ConnectionError: If an error occurs while reading the response.
        """
        response = self.powerMeter.read()
        response = response.replace('\n', '').replace('\r', '')
        return response
    
    def _query(self, command: str) -> str:
        """
        Query a command to the power mete, and returns the response.

        Returns:
            str: The cleaned response string.

        Raises:
            ConnectionError: If an error occurs while reading the response.
        """
        response = self.powerMeter.query(command)
        response = response.strip()
        return response


