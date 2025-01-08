from photonicdrivers.Piezo_AttocubeAMC.Piezo_AttocubeAMC_Driver import Piezo_AttocubeAMC_Driver

# has to run on the attocube PC
ip = "192.168.1.1"

# (2046444.326, 2170676.425, 3159894.639)

piezo = Piezo_AttocubeAMC_Driver(ip,x_min_nm=2040000,x_max_nm=2050000)
piezo.connect()
# x,y,z = piezo.get_position()
# piezo.set_position(x_nm=x + 10*1000, move_x=True)
print(piezo.get_position())

print(piezo.get_device_type())
piezo.disconnect()

