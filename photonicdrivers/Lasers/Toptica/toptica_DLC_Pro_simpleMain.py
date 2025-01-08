from photonicdrivers.Lasers.Toptica.Toptica_DLC_Pro_Driver import Toptica_DLC_PRO_Driver 

laser = Toptica_DLC_PRO_Driver()
laser.connect()
laser.set_wavelength(940)
laser.set_diode(True)
laser.set_power_stabilization(True)
laser.set_power(1)
# laser.set_diode(False)
laser.disconnect()