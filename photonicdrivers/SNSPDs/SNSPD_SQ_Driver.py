from photonicdrivers.SNSPDs.FilesFromManufacturer.WebSQControl import WebSQControl
from photonicdrivers.Abstract.Connectable import Connectable

class SNSPD_SQ_Driver(Connectable):
    def __init__(self,_ip_string: str, _control_port: int=12000, _counts_port: int=12345) -> None:
        self.ipAddress = _ip_string
        self.controlPort = _control_port
        self.countsPort = _counts_port

        self.websq = WebSQControl(TCP_IP_ADR=self.ipAddress, CONTROL_PORT=self.controlPort, COUNTS_PORT=self.countsPort)

    def connect(self):        
        self.websq.connect()

    def disconnect(self):        
        self.websq.close()

    def is_connected(self):    
        try:    
            return self.websq.connected
        except: 
            return False

    def getNumberOfDetectors(self) -> int:
        return self.websq.get_number_of_detectors()
    
    def getTemperatures(self) -> float:
        # This function returns all kind of temperatures. See the WebSQControl.py script from the manufacturer
        # Each return type is an array of the last 200 measurements
        time, T, T_40K, v_av, board_T1, board_T2 = self.websq.get_cryo_temperature()

        # We are only interested in the latest
        latestTemp = T[199]
        return latestTemp
    
    def getCounts(self, numberOfMeasurements: int):
        data = self.websq.acquire_cnts(numberOfMeasurements)
        print(data)
        return data
    
    def setMeasurementPeriod(self, integrationtime_ms:int) -> None:
        self.websq.set_measurement_periode(integrationtime_ms)

    def getMeasurementPeriod(self) -> float:
        return self.websq.get_measurement_periode()



        
    



# http://10.209.67.158

# Parses arguments, type -h for help message
# parser = argparse.ArgumentParser(
#     add_help=True,
#     description='Example program.')
# parser.add_argument('-N', dest='N', type=int, default=10,
#                     help='The amount of measurements done.')
# parser.add_argument(
#     '--ipAddress',
#     '-ip',
#     dest='tcp_ip_address',
#     type=str,
#     default='10.209.67.158',
#     help='The TCP IP address of the detector')
# args = parser.parse_args()

# # Number of measurements (default 10)
# N = 10

# # TCP IP Address of your system (default 192.168.1.1)
# tcp_ip_address = "10.209.67.158"

# # The control port (default 12000)
# control_port = 12000
# # The port emitting the photon Counts (default 12345)
# counts_port = 12345

# print(tcp_ip_address)
# print(control_port)
# print(counts_port)
# websq = WebSQControl(TCP_IP_ADR=tcp_ip_address, CONTROL_PORT=control_port, COUNTS_PORT=counts_port)
# # Alternatively, you can use the with clause
# # with WebSQControl(TCP_IP_ADR=tcp_ip_address, CONTROL_PORT=control_port, COUNTS_PORT=counts_port) as websq:


# websq.connect()
# # print("Automatically finding bias current, avoid Light exposure")
# # found_bias_current = websq.auto_bias_calibration(
# #     DarkCounts=[100, 100, 100, 100])
# # print("Bias current: " + str(found_bias_current))

# # Acquire number of detectors in the system
# number_of_detectors = websq.get_number_of_detectors()
# print("Your system has " + str(number_of_detectors) + ' detectors\n')
# t, T, T2, v_av, board_T1, board_T2 = websq.get_cryo_temperature()

# print("Temperature of stage 1: " + str(T[199]))


# print("Set integration time to 20 ms\n")
# websq.set_measurement_periode(20)   # Time in ms

# print("Enable detectors\n")
# websq.enable_detectors(True)


# # Random generator
# def rand():
#     return random.randrange(0, 10000) / 1000.0


# # Set the bias current and trigger level with random numbers
# curr = []
# trig = []
# for n in range(number_of_detectors):
#     curr.append(rand())
#     trig.append(rand())

# print("Set bias currents to: " + str(curr))
# websq.set_bias_current(current_in_uA=curr)

# print("Set trigger levels to: " + str(trig))
# websq.set_trigger_level(trigger_level_mV=trig)
# print("\n")


# Acquire N counts measurements
# Returns an array filled with N numpy arrays each
# containing as first element a time stamp and then the detector
# counts ascending order

# print("Acquire " + str(N) + " counts measurements")
# print("============================\n")
# # Get the counts
# counts = websq.acquire_cnts(N)

# # Print the counts nicely
# header = "Timestamp\t\t"
# for n in range(number_of_detectors):
#     header += "Channel" + str(n + 1) + "\t"

# print(header)

# for row in counts:
#     line = ""
#     for element in row:
#         line += str(element) + '\t'
#     print(line)

# print('\n')

# print("Read back set values")
# print("====================\n")
# print("Measurement Periode (ms): \t"
#       + str(websq.get_measurement_periode()))
# print("Bias Currents in uA: \t\t" + str(websq.get_bias_current()))
# print("Trigger Levels in mV: \t\t" + str(websq.get_trigger_level()))


# Close connection
# websq.close() # not needed since the with closes the connection
