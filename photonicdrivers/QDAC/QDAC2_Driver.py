# import qdac2
# import common.connection as conn
# # from serial import Serial

# device = conn.find_qdac2_on_usb()
# qdac = qdac2.QDAC2(device)
# print(qdac.status())

import socket
from photonicdrivers.Abstract.Connectable import Connectable

class QDAC2_Driver(Connectable):
    def __init__(self,_ip_string: str,_port_number: int) -> None:
        self.ipAddress = _ip_string
        self.port = _port_number
        self.timeout = 2 # seconds
        
        self.server_address = (self.ipAddress, self.port)
        
        self.terminationChar = "\n"

    # High level methods are methods that consist of multiple low level methods
    # A low level method sends a single (or very few) command string

    ##################### HIGH LEVEL METHODS ###########################

    def printSystemInformation(self) -> None:
        print("IDN:")
        print(self.get_product_ID())
        print("MAC address:")
        print(self.get_MAC_address())
        print("IP address:")
        print(self.get_IP_address())
        print("Subnet mask:")
        print(self.get_subnet_mask())
        print("Gateway:")
        print(self.get_getway())
        print("Hostname:")
        print(self.get_host_name())
        print("DHCP [on/off]:")
        print(self.get_DHCP_status())

    ##################### LOW LEVEL SYSTEM METHODS ###########################

    def get_product_ID(self) -> str:
        try:
            response = self._query("*IDN?")
            return response
        except:
            return False
    
    def get_IP_address(self) -> str:
        response = self._query("syst:comm:lan:ipad?")
        return response
    
    def get_MAC_address(self) -> str:
        response = self._query("syst:comm:lan:mac?")
        return response
    
    def get_getway(self) -> str:
        response = self._query("syst:comm:lan:gat?")
        return response
    
    def get_subnet_mask(self) -> str:
        response = self._query("syst:comm:lan:smas?")
        return response
    
    def get_host_name(self) -> str:
        response = self._query("syst:comm:lan:host?")
        return response
    
    def get_DHCP_status(self) -> str:
        response = self._query("syst:comm:lan:dhcp?")
        return response
    
    def get_error_all(self) -> str:
        response = self._query("syst:err:all?")
        return response
    
    def get_error_count(self) -> str:
        response = self._query("syst:err:coun?")
        return response

    def restart_system(self) -> None:
        command = "syst:comm:lan:rest"
        self._write(command)        
        self._checkForErrors(command)

    def set_DCHP(self, DHCPStatusString: str) -> None:
        if DHCPStatusString == "ON" or DHCPStatusString == "OFF":
            command = "SYST:COMM:LAN:DHCP " + DHCPStatusString
            self._write(command)            
            self._checkForErrors(command)
            self.update_memory()
            self.restart_system()
        else:
            print("The DHCPStatusString provided is not valid. It must be either ON of OFF.")

    def set_IP_address(self) -> None:
        print("Setting the IP address must be done via USB communication, which has not been implemented yet.")

    def update_memory(self) -> None:
        command = "syst:comm:lan:upd"
        self._write(command)
        self._checkForErrors(command)

    ##################### LOW LEVEL SOURCE METHODS ###########################

    def get_voltage_range(self, chNumberString: str, chListNumberString: str) -> str:
        # Either chNumberString or chListNumberString must be empty - the command either changes a single channel OR a list of channels
        response = self._query("sour" + chNumberString + ":rang? " + chListNumberString) # return LOW for 2 V, HIGH for 10 V
        return response
    
    def get_voltage_mode(self, chNumberString: str) -> str:
        response = self._query("sour" + chNumberString + ":mode?") # returns FIXED, SWEEP, or LIST
        return response
    
    def get_voltage(self, chNumberString: str) -> str:
        response = self._query("sour" + chNumberString + ":volt?")
        return response
    
    def get_current(self, chNumberString: str) -> str:
        response = self._query("sour" + chNumberString + ":curr?")
        return response

    def set_voltage_range(self, chNumberString: str, rangeString: str) -> None:
        if rangeString == "HIGH" or rangeString == "LOW":
            command = "sour" + chNumberString + ":rang " + rangeString
            self._write(command) # returns LOW for 2 V, HIGH for 10 V
            self._checkForErrors(command)
        else:
            print("The rangeString must be either HIGH or LOW")

    def set_voltage_mode(self, chNumberString: str, modeString: str) -> None:
        if modeString == "FIX" or modeString == "SWE" or modeString == "LIST":
            command = "sour" + chNumberString + ":mode " + modeString
            self._write(command)
            self._checkForErrors(command)
        else:
            print("The modeString must be either FIX, SWE, or LIST")

    def set_voltage(self,chNumberString: str,voltageString: str) -> None:
        command = "sour" + chNumberString + ":volt " + voltageString
        self._write(command) # returns the current output voltage
        self._checkForErrors(command)

    ##################### CONNECTABLE ###########################
    
    def disconnect(self) -> None:
        self.sock.close()

    def connect(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(self.timeout) # sets the timeout of the receive command in seconds. 
        self.sock.connect(self.server_address) 

    def is_connected(self) -> bool:
        return bool(self.get_product_ID())

    def get_settings(self):
        channels_dict = {}
        # Loop over channels 1 through 10
        for channel in range(1, 11):
            # Convert channel number to string for usage in method calls
            channel_str = str(channel)
            
            # Collect settings for each channel
            channels_dict[str(channel_str)] = {
                "voltage": self.get_voltage(channel_str),
                "range": self.get_voltage_range(channel_str, ""),
                "mode": self.get_voltage_mode(channel_str)
            }
        settings = {"channels": channels_dict}
        return settings
    
    ##################### PRIVATE METHODS ###########################

    def _query(self,commandString: str) -> str:
        self._write(commandString)
        response = self._read()    

        # check is the system responded with an error:     
        self._checkForErrors(commandString)

        return response

    def _write(self, commandString: str) -> None:
        command = commandString + self.terminationChar
        self.sock.sendall(command.encode("utf-8"))
        # command = bytes(commandString + self.terminationChar, "utf-8")
        # self.sock.sendall(command)

    def _read(self, bytesToReceive: int = 1024) -> str:
        byteString = self.sock.recv(bytesToReceive)
        response = byteString.decode("utf-8")
        return response

    def _checkForErrors(self, commandString: str) -> None: 
        # To avoid recursion, the commands are typed in directly rather than calling the class methods
        self._write("syst:err:coun?")
        errorCount = self._read()
        try:
            if float(errorCount) > 0:            
                self._write("syst:err:all?")
                errors = self._read()
                print("The QDAC returned the error(s): " + errors + "when executing the command: " + commandString)
        except:
            pass     #if float(errorCount) > 0: 
                        #ValueError: could not convert string to float: '0\n0\n'