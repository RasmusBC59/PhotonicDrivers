import socket
from photonicdrivers.Abstract.Connectable import Connectable

class Maxigauge_TPG_366_Driver(Connectable):
    def __init__(self,_ip_string: str,_port_number: int) -> None:
        self.ipAddress = _ip_string
        self.port = _port_number
        self.timeout = 2 # seconds
        
        self.server_address = (self.ipAddress, self.port)
        
        self.terminationChar = "\r\n"

    ##################### LOW LEVEL  METHODS ###########################
    
    def disconnect(self) -> None:
        self.sock.close()

    def connect(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(self.timeout) # sets the timeout of the receive command in seconds. 
        self.sock.connect(self.server_address) 

    def is_connected(self) -> bool:
        try:
            self.get_id()
            return True
        except:
            False

    def get_id(self) -> str:
        response_raw, command_acknowledged = self._query("AYT")

        if command_acknowledged:
            response_raw, dummy = response_raw.split(b'\r\n')
            return response_raw.decode('utf-8').strip()
        
        pass
    
    def get_unit(self) -> str:
        '''
        Function gets the unit in which pressures are measured
        '''
        response_raw, command_acknowledged = self._query("UNI")

        if command_acknowledged:
            response_raw, dummy = response_raw.split(b'\r\n')
            response = int(response_raw.decode('utf-8').strip())

            unit_mapping = {
                0: "mbar",
                1: "Torr",
                2: "Pascal",
                3: "Micron",
                4: "hPascal",  # default
                5: "Volt"
            }

        return unit_mapping.get(response, "Invalid unit ID")

    def get_pressure(self, channel_number:int) -> float | int:
        '''
        Gets the pressure of the chosen channel in the unit of the device
        '''
        command = "PR" + str(channel_number)
        response_raw, command_acknowledged = self._query(command)

        if command_acknowledged:
            response, dummy = response_raw.split(b'\r\n')
            data_status_raw, pressure_raw = response.split(b',')

            data_status = int(data_status_raw.decode('utf-8').strip())
            pressure = float(pressure_raw.decode('utf-8').strip())

            return pressure, data_status
        
        pass

    def get_all_pressures(self) -> tuple[float] | tuple[int]:
        '''
        Gets the pressure of all channels in the unit of the device
        '''
        response_raw, command_acknowledged = self._query("PRX")

        if command_acknowledged:
            response, dummy = response_raw.split(b'\r\n')
            response_array = response.split(b',')
            data_status_array = []
            pressure_array = []

            for i in range(len(response_array)):
                if i%2==0:
                    # index is even. Array element is a data status
                    status = int(response_array[i].decode('utf-8').strip())
                    data_status_array.append(status)
                else:
                    # index is odd. Array element is a pressure value
                    pressure = float(response_array[i].decode('utf-8').strip())
                    pressure_array.append(pressure)

            return pressure_array, data_status_array
        
        pass
    
    ##################### PRIVATE METHODS ###########################

    def _query(self,commandString:str, bytes_to_read:int=1024) -> str:
        
        # Sending command and checking if acknowledged:
        self._write(commandString)
        write_response = self._read().strip()

        ascii_ack = b'\x06'
        command_acknowledged = write_response==ascii_ack

        if command_acknowledged == False:
            print(f"Command '{commandString}' not acknowledged. ASCII reponse: {write_response}")
            return write_response, command_acknowledged

        # Getting response:
        ascii_enq = "\x05"
        write_response = self._write(ascii_enq)
        read_response = self._read(bytes_to_read).strip()
        # print(read_response)

        return read_response, command_acknowledged

    def _write(self, commandString: str) -> None:
        command = commandString + self.terminationChar
        self.sock.sendall(command.encode("utf-8"))

    def _read(self, bytesToReceive:int=1024) -> str:
        byteString = self.sock.recv(bytesToReceive)
        return byteString