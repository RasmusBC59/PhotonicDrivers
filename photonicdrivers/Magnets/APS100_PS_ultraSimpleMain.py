import serial
import time

COM_PORT = 'COM6'
BAUD_RATE = 9600


device = serial.Serial(COM_PORT, BAUD_RATE, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE, timeout=1)
# device = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
# device.write(b'*IDN?\n')
device.write(b'*IDN?;*ESE 12;*ESE?\r')

time.sleep(0.5)
# response = device.readline().decode('utf-8').strip()
# response = device.readline().decode('utf-8')
response = device.readline(1024)
print(response)
response = device.readline(1024)
print(response)
response = device.readline(1024)
print(response)

device.close()




# import pyvisa
# print("hello")
# # Open a VISA resource manager
# rm = pyvisa.ResourceManager()
# # List available VISA resources (instruments)
# # available_resources = rm.list_resources()
# # if not available_resources:
# #     print("No available VISA resources found.")
# # # Print the list of available resources
# # print("Available VISA resources:")
# # for idx, resource in enumerate(available_resources, start=1):
# #     print(f"{idx}. {resource}")



# # ASRL6::INSTR

# instrument = rm.open_resource("ASRL6::INSTR")

# # Send an IDN query using SCPI
# idn_query = "*IDN?"
# response = instrument.query(idn_query)
# print("Device Identification:", response)






# import serial.tools.list_ports
# # Get a list of all connected COM ports
# ports = serial.tools.list_ports.comports()
# # Print each available COM port
# if ports:
#     print("Connected COM ports:")
#     for port in ports:
#         print(f"{port.device}: {port.description}")
# else:
#     print("No COM ports found.")

