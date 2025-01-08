import pyvisa
from serial import Serial
from time import sleep

from photonicdrivers.Abstract.Connectable import Connectable

class Picus_Driver(Connectable):

    def __init__(self, _resource_manager: pyvisa.ResourceManager=None, _port: str=None, _connectionMethod=None) -> None:
        self.resource_manager = _resource_manager
        self.port = _port
        self.baud_rate = 115200
        self.data_bits = 8
        self.parity = "None"
        self.stop_bits = 1
        self.termination_character = "\n"
        self.timeout_ms = 5000        

        self.connectionType = _connectionMethod
        self.connection = None
        
#################################### HIGH LEVEL METHODS ##########################################



#################################### LOW LEVEL METHODS ###########################################

    def connect(self):
        if self.connectionType == "pyvisa":
            self.connection = self.resource_manager.open_resource(self.port)
            self.connection.read_termination = self.termination_character
            self.connection.write_termination = self.termination_character
            self.connection.timeout = self.timeout_ms
            print("Successfully connected to Picus laser via pyvisa using port: " + self.port)

        elif self.connectionType == "serial":
            self.connection = Serial(port=self.port, timeout = self.timeout_ms)
            print("Successfully connected to Picus laser via serial using port: " + self.port)    

        else:
            print("No connection method defined")

    def disconnect(self):
        # both the pyvisa and serial libraries have "close" command
        self.connection.close()

    def is_connected(self) -> bool:
        try:
            return bool(self.getRuntimeAmplifier())
        except:
            return False
        
    def getRuntimeAmplifier(self) -> str:
        command = "Measure:Runtime:Amplifier?"
        response = self._query(command)
        return response

    def getEnabledState(self) -> bool:
        command = "Laser:Enable?"
        response = self._query(command)
        return bool(int(response))
    
    def getWavelength(self) -> float:
        command = "Laser:Wavelength?"
        response = self._query(command)
        return float(response)
    
    def setEnabledState(self, state: bool) -> str:
        command = "Laser:Enable " + str(int(state))
        response = self._query(command)
        if response != "ACK":
            print("The command '" + command + "' failed. Response was: " + response)
        return response

    def setWavelength(self, wavelength_nm: float) -> None:
        command = "Laser:Wavelength " + str(wavelength_nm)
        response = self._query(command)
        if response != "ACK":
            print("The command '" + command + "' failed. Response was: " + response)
        return response
        


#################################### PRIVATE METHODS ###########################################

    def _write(self, command: str) -> None:
        if self.connectionType == "pyvisa":
            self.connection.write(command)
            
        elif self.connectionType == "serial":
            command = command + self.termination_character
            self.connection.write(command.encode())
        else:
            print("No connection method defined")        

    def _read(self) -> str:
        response = None

        if self.connectionType == "pyvisa":
            response = self.connection.read()
            response = response.replace('\n', '').replace('\r', '')

        elif self.connectionType == "serial":
            response = self.connection.readline().decode()
            response = response.replace('\n', '').replace('\r', '')

        else:
            print("No connection method defined")

        return response
    
    def _query(self, command: str) -> str:
        self._write(command)
        response = self._read()
        print("Command: " + str(command) + ", reponse: " + str(response))
        return response