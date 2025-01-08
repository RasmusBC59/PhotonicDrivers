import serial
import time

from instruments.Abstract.Connectable import Connectable


class APS100_PS_Driver(Connectable):
    def __init__(self, com_port:str) -> None:
        print("Initialising APS100 Ps Driver. Make sure to set it to REMOTE mode to control it.")
        
        self.port = com_port
        self.baud_rate = 9600
        self.timeout = 1

        self.termination_char = '\r'

    def connect(self) -> None:
        self.connection = serial.Serial(port=self.port, baudrate=self.baud_rate, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE, timeout=self.timeout)
        self.unit = self.get_unit()
    
    def disconnect(self) -> None:
        self.connection.close()

    def is_connected(self) -> bool:
        try:
            self.get_id()
            return True
        except:
            return False

    def get_id(self) -> None:
        return self.__query("*IDN?;*ESE 12;*ESE?")

    def get_channel(self) -> str:
        '''
        Returns which output channel is currently controlled (1 or 2)
        '''
        return self.__query("CHAN?")
    
    def set_channel(self, channel_number:int) -> str:
        '''
        Sets which output channel is currently controlled (1 or 2)
        '''
        return self.__query(f"CHAN {channel_number}")
       
    def set_control_remote(self) -> str:
        return self.__query("REMOTE")
    
    def set_control_local(self) -> str:
        return self.__query("LOCAL")
    
    def get_control_mode(self) -> str:
        return "There is no way of asking the PS whether it is in LOCAL or REMOTE mode. Look at the front panel"

    def get_unit(self) -> str:
        return self.__query("UNITS?")
    
    def set_unit(self, unit:str) -> str:
        '''
        Unit options are A or kG.
        Both G and kG will set the unit to kG.
        '''
        # The PS will also accept T and G as an input, but it will set the unit to kG
        if unit == "A" or unit == "kG":
            try:
                response = self.__query(f"UNITS {unit}")
                self.unit = self.get_unit()
                return response
            except:
                warning_str = "Set unit failed"
                print(warning_str)
                return warning_str
        else:
            print(f"Trying to set unit to {unit}, but it must be kG or A.")

    def get_lower_limit(self) -> str:
        return self.__query("LLIM?")

    def set_lower_limit(self, limit:float, unit:str):
        '''
        unit: should be A or kG
        '''
        ps_unit = self.get_unit()
        if  ps_unit != unit:
            warning_str = f"Trying to set the lower limit to {limit} {unit}, but the power supply unit is {ps_unit}. Ignoring command."
            print(warning_str)
            return warning_str
        return self.__query(f"LLIM {limit}")
    
    def get_upper_limit(self) -> str:
        return self.__query("ULIM?")

    def set_upper_limit(self, limit:float, unit:str):
        '''
        unit: should be A or kG
        '''
        ps_unit = self.get_unit()
        if  ps_unit != unit:
            warning_str = f"Trying to set the upper limit to {limit} {unit}, but the power supply unit is {ps_unit}. Ignoring command."
            print(warning_str)
            return warning_str
        return self.__query(f"ULIM {limit}")
    
    def ramp_up(self, wait_while_ramping:bool=True) -> str:
        return self.__ramp("SWEEP UP", wait_while_ramping)
    
    def ramp_down(self, wait_while_ramping:bool=True) -> None:
        return self.__ramp("SWEEP DOWN", wait_while_ramping)
    
    def ramp_to_zero(self, wait_while_ramping:bool=True) -> None:
        return self.__ramp("SWEEP ZERO", wait_while_ramping)
    
    def get_sweep_mode(self) -> str:
        '''
        Returns: "Sweeping up", "Standby", "Pause", "Sweeping to zero", "Sweeping down"
        '''
        return self.__query("SWEEP?")
    
    def __ramp(self, command:str, wait_while_ramping:bool) -> str:
        response = self.__query(command)
        status = "unknown"
        if wait_while_ramping: print("Check if with the current ramp rates, the PS never really reaches the target field") # Can be remoed later is ramp rates are made less cautious
        while status != "Standby" and wait_while_ramping == True:
            time.sleep(0.2)
            status = self.get_sweep_mode()
            print(status)
        return response

    # Attocube says the IMAG command should be avoided, as it ignores ramp rate limits.
    # def set_current(self, current_A:float, channel:int=None) -> None:
    #     # if channel != None:
    #     #     self.set_channel(str(channel))
    #     return self.__query(f"IMAG {current_A}")
    
    def get_current(self, channel:int=None) -> float:
        '''
        Returns the current in A
        '''
        if channel != None:
            self.set_channel(str(channel))        
        
        if self.unit != "A":
            print("Changing unit to A")
            self.set_unit("A")
            print(self.get_unit())
        
        response = self.__query("IMAG?")
        current = response.rstrip('A')
        return float(current)
    
    # Attocube says the IMAG command should be avoided, as it ignores ramp rate limits.
    # def set_field(self, field_T:float, channel:int=None) -> None:
    #     if channel != None:
    #         self.set_channel(str(channel))
    #     field_kG = field_T*10
    #     return self.__query(f"IMAG {field_kG} G")

    def get_field(self, channel:int=None) -> float:
        '''
        Returns the field in kG. This number is derived from the current used a factor determined at the factory
        '''
        if channel != None:
            print("Changing unit to kG")
            self.set_channel(str(channel))

        if self.unit != "kG":
            self.set_unit("kG")
        
        response = self.__query("IMAG?")
        field_kG = float(response.rstrip('kG'))
        return field_kG
    
    def send_custom_command(self, command:str) -> str:
        return(self.__query(command))

    ################################ PRIVATE METTHODS ################################

    def __query(self, command_str:str) -> str:
        command = f'{command_str}{self.termination_char}'        
        self.connection.write(command.encode('utf-8'))

        # a small wait is required for the device to send back a response. 0.1 s is too little
        time.sleep(0.2)

        # The power supply first returns the command that was sent to it:
        reflected_command = self.connection.readline()
        # The power supply then returns its response (if nay)
        response_raw = self.connection.readline()
        response = response_raw.decode('utf-8').strip()

        return response
