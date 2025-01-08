
import struct
import socket
import signal
import datetime


class CryomechCompressor_Driver:
    def __init__(self, _ip_address, _port=502, _timeout=10):
        self.ip_address = _ip_address
        self.port = _port
        self.timeout = _timeout


 ##################### HIGH LEVEL SOURCE METHODS ###########################
 
    def get_data_lst(self):
        """
        Returns list of specified values (coolant in/out temp, oil/helium temp, low/high pressure, delta pressure average, motor current)
        """
        self.comm.sendall(self._buildRegistersQuery())
        data = self.comm.recv(1024)
        data_readout_failed, brd = self._breakdownReplyData(data)
        if data_readout_failed:
            return None
        else:
            return data_readout_failed, brd['Coolant In Temp'],brd['Coolant Out Temp'],brd['Oil Temp'],brd['Helium Temp'], brd['Low Pressure'], brd['High Pressure'], brd['Delta Pressure Average'], brd['Motor Current']


  ##################### LOW LEVEL SOURCE METHODS ###########################

    def connect(self):
        self.comm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.comm.connect((self.ip_address, self.port))
        self.comm.settimeout(self.timeout)

    def disconnect(self):
        self.comm.close()

    def get_operating_state(self) -> str:
        return self._get_data('Operating State') 

    def get_compressor_state(self) -> str:
        return self._get_data('Compressor State') 

    def get_warning_state(self) -> str:
        return self._get_data('Warning State') 

    def get_alarm_state(self) -> str:
        return self._get_data('Alarm State') 

    def get_coolant_in_temp(self) -> float: #in C
        return self._get_data('Coolant In Temp') 
    
    def get_coolant_out_temp(self) -> float: #in C
        return self._get_data('Coolant In Temp')
    
    def get_oil_temp(self) -> float: #in C
        return self._get_data('Oil Temp')
    
    def get_helium_temp(self) -> float: #in C
        return self._get_data('Helium Temp')
    
    def get_low_pressure(self) -> float: #in psi
        return self._get_data('Low Pressure')

    def get_low_pressure_average(self) -> float: #in psi
        return self._get_data('Low Pressure Average')

    def get_high_pressure(self) -> float: #in psi
        return self._get_data('High Pressure')

    def get_high_pressure_average(self) -> float: #in psi
        return self._get_data('Low Pressure Average')

    def get_delta_pressure_average(self) -> float: #in psi
        return self._get_data('Delta Pressure Average')
    
    def get_motor_current(self) -> float:
        return self._get_data('Motor Current')
    
    def get_hours_of_opperation(self) -> float:
        return self._get_data('Hours of Opperation')


    ##################### PRIVATE METHODS ###########################


    def _get_data(self,specific_data):
        """
        Gets the raw data from the compressor and returns it in a usable format.
        """
        self.comm.sendall(self._buildRegistersQuery())
        data = self.comm.recv(1024)
        data_readout_failed, brd = self._breakdownReplyData(data)

        if data_readout_failed:
            return None
        else:
            return brd[specific_data]


    def _buildRegistersQuery(self):
        # ModBusTCP query code
        query = bytes(
            [
                0x09,
                0x99,  # Message ID (arbitrary)
                0x00,
                0x00,  # Protocol Identifier
                0x00,
                0x06,  # Message size to follow (bytes)
                0x01,  # Unit Identifier
                0x04,  # Read Analog Input Register
                0x00,
                0x01,  # Starting Register
                0x00,
                0x35,  # Number of 2 byte registers to read
            ]
        )
        return query

    def _breakdownReplyData(self, rawdata):
        """
        Take in raw ptc data, and return a dictionary.
        The dictionary keys are the data labels,
        the dictionary values are the data in floats or ints.
        """

        # Associations between keys and their location in rawData
        # Original data as transmitted is high byte first, low word first
        # We rearrange to do high byte first, high word first which is "big endian"
        keyloc = {
            "Operating State": [9, 10],
            "Compressor State": [11, 12],
            "Warning State": [15, 16, 13, 14],
            "Alarm State": [19, 20, 17, 18],
            "Coolant In Temp": [23, 24, 21, 22],
            "Coolant Out Temp": [27, 28, 25, 26],
            "Oil Temp": [31, 32, 29, 30],
            "Helium Temp": [35, 36, 33, 34],
            "Low Pressure": [39, 40, 37, 38],
            "Low Pressure Average": [43, 44, 41, 42],
            "High Pressure": [47, 48, 45, 46],
            "High Pressure Average": [51, 52, 49, 50],
            "Delta Pressure Average": [55, 56, 53, 54],
            "Motor Current": [59, 60, 57, 58],
            "Hours of Opperation": [63, 64, 61, 62],
            "Pressure Unit": [65, 66],
            "Temperature Unit": [67, 68],
            "Serial Number": [69, 70],
            "Model": [71, 72],
            "Software Revision": [73, 74],
        }
        statuscodes = dict()
        statuscodes["Operating State"] = {
            0: "Idling - ready to start",
            2: "Starting",
            3: "Running",
            5: "Stopping",
            6: "Error Lockout",
            7: "Error",
            8: "Helium Cool Down",
            9: "Power Related Error",
            15: "Recovered from Error",
        }
        statuscodes["Compressor State"] = {0: "Off", 1: "On"}
        statuscodes["Warning State"] = {
            -0: "No warnings",
            -1: "Coolant In Temp High",
            -2: "Coolant In Temp Low",
            -4: "Cooling Out Temp High",
            -8: "Cooling Out Temp Low",
            -16: "Oil Temp High",
            -32: "Oil Temp Low",
            -64: "Helium Temp High",
            -128: "Helium Temp Low",
            -256: "Low Pressure Low",
            -512: "Low Pressure High",
            -1024: "High Pressure High",
            -2048: "High Pressure Low",
            -4096: "Delta Pressure High",
            -8192: "Delta Pressure Low",
            -16384: "Motor Current Low",
            -32768: "Three Phase Error",
            -65536: "Power Supply Error",
            -131072: "Static Pressure High",
            -262144: "Static Pressure Low",
            -524288: "Cold Head Motor Stall",
            -1048576: "Coolant In Sensor Problem",
            -2097152: "Coolant Out Sensor Problem",
            -4194304: "Helium Sensor Problem",
            -8388608: "Oil Sensor Problem",
            -16777216: "High Pressure Sensor Problem",
            -33554432: "Low Pressure Sensor Problem",
            -67108864: "Motor Current Sensor Problem",
            -134217728: "Motor Current High",
            -268435456: "Inverter Error",
            -536870912: "Driver Communication Loss",
            -1073741824: "Inverter Communication Loss",
        }
        statuscodes["Alarm State"] = statuscodes["Warning State"]
        statuscodes["Pressure Unit"] = {0: "psi", 1: "bar", 2: "kPa"}
        statuscodes["Temperature Unit"] = {0: "F", 1: "C", 2: "K"}
        statuscodes["Model Major"] = {1: "8", 2: "9", 3: "10", 4: "11", 5: "28"}
        statuscodes["Model Minor"] = {
            1: "A1",
            2: "01",
            3: "02",
            4: "03",
            5: "H3",
            6: "I3",
            7: "04",
            8: "H4",
            9: "05",
            10: "H5",
            11: "I6",
            12: "06",
            13: "07",
            14: "H7",
            15: "I7",
            16: "08",
            17: "09",
            18: "9C",
            19: "10",
            20: "1I",
            21: "11",
            22: "12",
            23: "13",
            24: "14",
        }

        # Iterate through all keys and return the data in a usable format.
        # If there is an error in the string format, print the
        # error to logs, return an empty dictionary, and flag the data as bad
        data = {}
        data["datetime"] = datetime.datetime.now().isoformat()
        try:
            for key in keyloc.keys():
                locs = keyloc[key]
                wkrBytes = bytes([rawdata[loc] for loc in locs])

                # four different data formats to unpack
                # Big endian unsigned integer 16 bits
                if key in [
                    "Operating State",
                    "Compressor State",
                    "Pressure Unit",
                    "Temperature Unit",
                    "Serial Number",
                ]:
                    state = struct.unpack(">H", wkrBytes)[0]
                    try:
                        data[key] = statuscodes[key][state]
                    except:
                        data[key] = state
                # 32bit signed integer which is actually stored as a 32bit IEEE float (silly)
                elif key in ["Warning State", "Alarm State"]:
                    state = int(struct.unpack(">f", wkrBytes)[0])
                    try:
                        data[key] = ""
                        for status in statuscodes[key].keys():
                            if abs(state) & abs(status):
                                data[key] += statuscodes[key][status] + ":"
                        if not data[key]:
                            data[key] = statuscodes[key][-0.0]
                        data[key] = data[key].rstrip(":")
                    except:
                        data[key] = state
                # 2 x 8-bit lookup tables
                elif key in ["Model"]:
                    model_major = struct.unpack(">B", bytes([rawdata[locs[0]]]))[0]
                    model_minor = struct.unpack(">B", bytes([rawdata[locs[1]]]))[0]
                    try:
                        data[key] = (
                            statuscodes["Model Major"][model_major]
                            + statuscodes["Model Minor"][model_minor]
                        )
                    except:
                        data[key] = str(model_major) + "_" + str(model_minor)
                elif key in ["Software Revision"]:
                    version_major = struct.unpack(">B", bytes([rawdata[locs[0]]]))[0]
                    version_minor = struct.unpack(">B", bytes([rawdata[locs[1]]]))[0]
                    data[key] = str(version_major) + "." + str(version_minor)
                # 32 bit Big endian IEEE floating point
                else:
                    data[key] = struct.unpack(">f", wkrBytes)[0]

            data_readout_failed = False

        except:
            data_readout_failed = True
            print(
                "Compressor output could not be converted to numbers."
                "Skipping this data block. Bad output string is {}".format(rawdata)
            )

        return data_readout_failed, data

