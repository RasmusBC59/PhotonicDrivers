from anyvisa import AnyVisa
from photonicdrivers.Power_Meters.Thorlabs_PM.Thorlabs_Power_Meter_Driver import Thorlabs_Power_Meter_Driver

"""
Class for interfacing with Thorlab powermeters.
Supported models: PM103E
Supported units: {'W', 'mW', 'dBm'}
Anyvisa: Navigate to the folder with the anyvisa .whl file and write "pip install anyvisa-0.3.0-py3-none-any.whl"

TCPIP0::10.209.67.184::PM103E-4E_M01027537::INSTR
TCPIP0::10.209.67.196::PM103E-A0_M01080977::INSTR
"""


class Thorlabs_PM103E_Driver(Thorlabs_Power_Meter_Driver):
    
    def __init__(self, port: str) -> None:
        """
        Initializes the Thorlabs PM103E Driver instance.

        Args:
            port (str): The VISA resource string for connecting to the Thorlabs PM103E power meter.
        """
        self.port = port
        self.power_meter = None

    def connect(self) -> None:
        """
        Opens a connection to the Thorlabs PM103E power meter and configures it for power measurements.
        """
        self.power_meter = AnyVisa.TL_Open(self.port)
        self.power_meter.open()

    def disconnect(self) -> None:
        """
        Closes the connection to the Thorlabs PM103E power meter.
        """
        #self.power_meter.close()

        print("Power meter cannot close in same session due to an error in PyVisa. To be fixed")

    def is_connected(self) -> bool:
        """
        Checks if a connection to the Thorlabs PM103E power meter is established.

        Returns:
            bool: True if the device is connected, False otherwise.
        """
        try:
            return bool(self.get_idn()) is not None
        except Exception:
            return False

    def get_idn(self) -> str:
        """
        Retrieves the identification string of the Thorlabs PM103E power meter.

        Returns:
            str: The response from the *IDN? command.
        """
        return self._query("*IDN?")

    def get_averaging(self) -> int:
        """
        Gets the current number of averaging cycles configured on the power meter.

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

    def set_power_unit(self, power_unit_str: str) -> None:
        """
        Sets the units for power measurements.

        Args:
            unit (str): The unit to set ('W', 'mW', or 'dBm').
        """
        self._write(f':SENS:POW:UNIT {power_unit_str}')

    def get_power_unit(self) -> str:
        """
        Retrieves the current units for power measurements.

        Returns:
            str: The current units ('W', 'mW', or 'dBm').
        """
        return self._query(':SENS:POW:UNIT?')

    def get_power(self) -> float:
        """
        Retrieves the current power measurement from the detector.

        Returns:
            float: The measured power.
        """
        return float(self._query("MEAS:SCAL:POW?"))

    def get_wavelength(self) -> float:
        """
        Retrieves the current wavelength setting of the detector.

        Returns:
            float: The wavelength in nanometers.
        """
        return float(self._query(':SENS:CORR:WAV?'))

    def reset(self) -> None:
        """
        Resets the power meter to its default state.
        """
        self._write('*RST')

    def get_auto_range(self) -> bool:
        """
        Retrieves the current status of the auto range mode.

        Returns:
            bool: True if auto range is enabled, False otherwise.
        """
        return bool(int(self._query("SENS:POW:RANG:AUTO?")))

    def set_auto_range(self, auto: bool) -> None:
        """
        Enables or disables the auto range mode.

        Args:
            auto (bool): True to enable auto range, False to disable.
        """
        self._write(f"SENS:POW:RANG:AUTO {'ON' if auto else 'OFF'}")

    def get_zero_magnitude(self) -> float:
        """
        Retrieves the zero magnitude of the detector.

        Returns:
            float: The zero magnitude value.
        """
        return float(self._query("SENS:CORR:COLL:ZERO:MAGN?"))

    def get_zero_state(self) -> bool:
        """
        Retrieves the current zero state of the detector.

        Returns:
            bool: True if the zero state is active, False otherwise.
        """
        return bool(int(self._query("SENS:CORR:COLL:ZERO:STAT?")))

    def zero(self) -> None:
        """
        Initiates a zero correction procedure on the detector.
        """
        self._write("SENS:CORR:COLL:ZERO:INIT")

    #################################### PRIVATE METHODS ###########################################

    def _write(self, command: str) -> None:
        """
        Sends a command to the power meter.

        Args:
            command (str): The command string to send.

        Raises:
            ConnectionError: If an error occurs while writing to the power meter.
        """
        try:
            self.power_meter.write(command)
        except Exception as exception:
            raise ConnectionError("An error occurred while writing to the power meter") from exception

    def _read(self) -> str:
        """
        Reads a response from the power meter.

        Returns:
            str: The response string.

        Raises:
            ConnectionError: If an error occurs while reading from the power meter.
        """
        try:
            return self.power_meter.read()
        except Exception as exception:
            raise ConnectionError("An error occurred while reading the power meter") from exception

    def _query(self, command: str) -> str:
        """
        Sends a command to the power meter and retrieves the response.

        Args:
            command (str): The command string to query.

        Returns:
            str: The response from the power meter.

        Raises:
            ConnectionError: If an error occurs while querying the power meter.
        """
        try:
            return self.power_meter.query(command)
        except Exception as exception:
            raise ConnectionError("An error occurred while querying the power meter") from exception
