from photonicdrivers.AttocubeAPI import AMC
from photonicdrivers.Abstract.Connectable import Connectable

from time import sleep
import numpy as np 

class Piezo_AttocubeAMC_Driver(Connectable):

    def __init__(self,ip_string: str, x_min_nm:int=300000, x_max_nm:int=4700000, y_min_nm:int=300000, y_max_nm:int=4700000, z_min_nm:int=300000, z_max_nm:int=4700000) -> None:
        self.ip_address = ip_string

        self.x_min = x_min_nm
        self.x_max = x_max_nm        
        self.y_min = y_min_nm
        self.y_max = y_max_nm        
        self.z_min = z_min_nm
        self.z_max = z_max_nm

        self.amc = AMC.Device(self.ip_address)

    def connect(self) -> None:
        self.amc.connect()

    def disconnect(self) -> None:
        self.amc.close()

    def is_connected(self) -> bool:
        try:
            return bool(self.get_device_type())
        except:
            return False
    
    def get_device_type(self):
        return self.amc.description.getDeviceType()
        

    def get_position(self) -> float | float | float:
        x, y, z, v1, v2, v3 = self.amc.control.getPositionsAndVoltages()
        return x, y, z
    
    def set_position(self, x_nm:int=0, y_nm:int=0, z_nm:int=0, move_x:bool=False, move_y:bool=False, move_z:bool=False, wait_while_moving:bool=True) -> None:
        '''
        Moves the piezo to the position specified by x_nm, y_nm,z_nm
        '''
        if self.__check_position_limits(x_nm,y_nm,z_nm,move_x,move_y,move_z):
            self.amc.control.MultiAxisPositioning(int(move_x), int(move_y), int(move_z), x_nm, y_nm, z_nm)
            if wait_while_moving:
                stages_moving = True
                while stages_moving:
                    sleep(0.1)
                    status = self.is_axis_moving
                    stages_moving = np.any(status)

        else:
            print("Requested piezo position was outside the limits. Did not execute the move command.")

    def set_position_relative(self, x_nm:int=0, y_nm:int=0, z_nm:int=0, move_x:bool=False, move_y:bool=False, move_z:bool=False, wait_while_moving:bool=True) -> None:
        '''
        Moves the piezo with an amount specified by x_nm, y_nm,z_nm relative to the current position
        '''
        x0, y0, z0 = self.get_position()
        x = x0 + x_nm
        y = y0 + y_nm
        z = z0 + z_nm

        self.set_position(int(x), int(y), int(z), move_x, move_y, move_z, wait_while_moving)

    def is_axis_moving(self) -> bool | bool | bool:
        x_moving, y_moving, z_moving = self.amc.control.getStatusMovingAllAxes()
        return bool(x_moving), bool(y_moving), bool(z_moving)

    
    ##################################### PRIVATE METHODS #####################################

    def __check_position_limits(self, x:int, y:int, z:int, move_x:bool, move_y:bool, move_z:bool) -> bool:
        if move_x:
            if x<self.x_min or x>self.x_max:
                print("Cannot move x to " + str(x) + " as it is outside the piezo limits of [" + str(self.x_min) + ", " + str(self.x_max) + "] nm." )
                return False
            
        if move_y:
            if y<self.y_min or y>self.y_max:
                print("Cannot move y to " + str(y) + " as it is outside the piezo limits of [" + str(self.y_min) + ", " + str(self.y_max) + "] nm." )
                return False

        if move_z:
            if z<self.z_min or z>self.z_max:
                print("Cannot move z to " + str(z) + " as it is outside the piezo limits of [" + str(self.z_min) + ", " + str(self.z_max) + "] nm." )
                return False
            
        return True