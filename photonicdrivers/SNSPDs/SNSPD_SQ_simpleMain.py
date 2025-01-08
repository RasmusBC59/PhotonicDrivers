from photonicdrivers.SNSPDs.SNSPD_SQ_Driver import SNSPD_SQ_Driver

ip_address = "10.209.67.158"
control_port = 12000 # The control port (default 12000)
counts_port = 12345 # The port emitting the photon Counts (default 12345)

snspd = SNSPD_SQ_Driver(ip_address, control_port, counts_port)
snspd.connect()
print(snspd.getNumberOfDetectors())
print(snspd.getMeasurementPeriod())
data = snspd.getCounts(1)
unixTime = data[0][0]
print(unixTime)
ch1Counts = data[0][1]
print(ch1Counts)

print(snspd.is_connected())

snspd.disconnect()
