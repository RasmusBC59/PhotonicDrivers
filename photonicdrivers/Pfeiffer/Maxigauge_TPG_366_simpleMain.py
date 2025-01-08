from photonicdrivers.Pfeiffer.Maxigauge_TPG_366_Driver import Maxigauge_TPG_366_Driver

IPAddress = '10.209.68.57'
Port = 8000

tpg = Maxigauge_TPG_366_Driver(IPAddress,Port)
tpg.connect()

tpg._write("ho")

print("Getting id:")
print(tpg.get_id())

print("Getting unit:")
print(tpg.get_unit())

print("getting pressure of channel:")
print(tpg.get_pressure(1)[0])

print("getting all pressures:")
print(tpg.get_all_pressures()[0])

tpg.disconnect()