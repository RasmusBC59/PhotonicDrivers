from photonicdrivers.Lakeshore335.Lakeshore335_Driver import Lakeshore335_Driver

com_port = "COM5"
baud_rate = 57600
lakeshore = Lakeshore335_Driver(com_port,baud_rate)
lakeshore.connect()

print(lakeshore.get_id())

temperatures = lakeshore.get_all_kelvin()
print(temperatures)