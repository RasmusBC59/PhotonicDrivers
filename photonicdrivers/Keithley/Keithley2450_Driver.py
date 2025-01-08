import socket
from photonicdrivers.Abstract.Connectable import Connectable

class Keithley2450_Driver(Connectable):

    def __init__(self, ip_address, port=5025):
        """
        Initialize the Keithley 2450 SourceMeter driver.

        :param ip_address: IP address of the Keithley 2450.
        :param port: Port number for SCPI communication (default is 5025).
        """
        self.ip_address = ip_address
        self.port = port
        self.socket = None

    def connect(self):
        """
        Establish a connection to the Keithley 2450.
        """
        if self.socket:
            print("Already connected.")
            return
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(10)  # Set a timeout for connection attempts

        try:
            self.socket.connect((self.ip_address, self.port))
            print(f"Connected to {self.ip_address}:{self.port}")
        except socket.timeout:
            print("Connection timed out.")
            self.socket = None
        except socket.error as e:
            print(f"Socket error: {e}")
            self.socket = None

    def disconnect(self):
        """
        Close the connection to the Keithley 2450.
        """
        if self.socket:
            self.socket.close()
            self.socket = None
            print("Connection closed.")

    def is_connected(self):
        try:
            self.identify()
            return True
        except: 
            return False

    def write(self, command):
        """
        Send an SCPI command to the Keithley 2450

        :param command: SCPI command to send.
        """
        if not self.socket:
            raise RuntimeError("Not connected to the device.")
        
        try:
            self.socket.sendall(command.encode('ascii') + b'\n')
        except socket.error as e:
            print(f"Socket error: {e}")
            return None

    def query(self, command):
        """
        Send an SCPI command to the Keithley 2450 and receive the response.

        :param command: SCPI command to send.
        :return: Response from the Keithley 2450.
        """
        if not self.socket:
            raise RuntimeError("Not connected to the device.")
        
        try:
            self.socket.sendall(command.encode('ascii') + b'\n')
            response = self.socket.recv(4096)  # Adjust buffer size if needed
            return response.decode('ascii').strip()
        except socket.error as e:
            print(f"Socket error: {e}")
            return None
    
    def read(self):
        """
        Receive a response from Keithley 2450

        :return: Response from the Keithley 2450.
        """
        if not self.socket:
            raise RuntimeError("Not connected to the device.")
        
        try:
            response = self.socket.recv(4096)  # Adjust buffer size if needed
            return response.decode('ascii').strip()
        except socket.error as e:
            print(f"Socket error: {e}")
            return None

    def identify(self):
        """
        Query the Keithley 2450 for its identification information.

        :return: Identification string.
        """
        return self.query("*IDN?")
    

    def measure_voltage(self):
        """
        Measure voltage in Volts
        """
        return self.query(":MEAS:VOLT?")

    def measure_current(self):
        """
        Measure current in Amps
        """
        return self.query(":MEAS:CURR?")
    
    def set_voltage(self,value):
        """
        Set output voltage in Volts
        """
        self.write(f":SOUR:VOLT:LEV:IMM:AMPL {str(value)}")

    def set_current(self,value):
        """
        Set output current in Amps
        """
        self.write(f":SOUR:CURR:LEV:IMM:AMPL {str(value)}")

    def set_output(self, value):
        """
        Start/stop output
        Value: 0 (off) or 1 (on)
        """
        self.write(f":OUTP:STAT {str(value)}")

    def set_voltage_output_range(self,value):
        """
        Set output voltage range in volts
        """
        self.write(f":SOUR:VOLT:RANG {str(value)}")
    
    def set_current_output_limit(self,value):
        """
        Set current limit in amps
        """
        self.write(f":SOUR:VOLT:ILIM {str(value)}")

    def set_voltage_measurement_range(self,value):
        """
        Set measurement voltage range in volts
        """
        self.write(f":SENS:VOLT:RANG {str(value)}")

    def set_current_measurement_range(self,value):
        """
        Set measurement current range in amps
        """
        self.write(f":SENS:CURR:RANG {str(value)}")

# Example usage:
if __name__ == "__main__":
    # Replace with the actual IP address of your Keithley 2450
    device = Keithley2450_Driver()

    try:
        device.connect()

        print("Identification:", device.identify())
    finally:
        device.disconnect()