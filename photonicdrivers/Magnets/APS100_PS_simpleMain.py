from photonicdrivers.Magnets.APS100_PS_Driver import APS100_PS_Driver
from time import sleep

# COM6 is PS Y, COM4 is XZ

com_port = 'COM6'
ps = APS100_PS_Driver(com_port)
ps.connect()



print("getting ID:")
print(ps.get_id())
print(ps.set_control_remote())

# print("getting channel:")
# print(ps.get_channel())

# print(ps.get_current())
print(ps.set_unit("kG"))
print(ps.get_unit())

ps.set_upper_limit(1, "kG")
print(ps.get_upper_limit())
# print(ps.ramp_up(wait_while_ramping=False))

# sleep(5)
print(ps.get_sweep_mode())
print(ps.get_field())
print(ps.get_current())
print(ps.get_unit())
# ps.ramp_to_zero(wait_while_ramping=False)

# print("setting mode:")
# print(ps.set_control_remote())


# ps.send_custom_command("SWEEP ZERO")

# print("getting mode:")
# print(ps.get_mode())
# sleep(1)
# print(ps.get_current())

ps.disconnect()