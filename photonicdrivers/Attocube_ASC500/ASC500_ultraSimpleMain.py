from photonicdrivers.Attocube_ASC500.FilesFromAttocubeGit.lib import ASC500
from photonicdrivers.Attocube_ASC500.FilesFromAttocubeGit.lib.asc500_scanner import ASC500Scanner

import os
import time

# has to run on the attocube PC

binPath = "C:\\gitRepositories\\NQCP-Phot-Git-Drivers\\photonicdrivers\\Attocube_ASC500\\FilesFromAttocubeGit\\Installer\\ASC500CL-V2.7.13\\"
dllPath = "C:\\gitRepositories\\NQCP-Phot-Git-Drivers\\photonicdrivers\\Attocube_ASC500\\FilesFromAttocubeGit\\64bit_lib\\ASC500CL-LIB-WIN64-V2.7.13\\daisybase\\lib\\"
dll_loc = dllPath + 'daisybase.dll'

# print(os.path.isfile(dll_loc))

# asc500 = ASC500(binPath, dllPath)
asc500 = ASC500(binPath, dllPath)

print("Starting Server: ")
asc500.base.startServer()

print("Send Profile: ")
asc500.base.sendProfile(binPath + 'afm.ngp')

print("Set Data Enable: ")
asc500.data.setDataEnable(1)

# print("Getting Scanner State: ")
# print(asc500.scanner.getScannerState())

# print("Getting Scanner absolute coor system: ")
# print(asc500.scanner.getScannerAbsolutCoordSystem())


# print("Getting Scanner Position: ")
# print(asc500.scanner.getPositionsXYZRel())

time.sleep(3)

print("start scanner: ")
# print(asc500.scanner.startScanner())
asc500.scanner.startScanner()

print("Setting Scanner Position: ")
new_position_m = [-10.0e-6, 0.0] # array is in pm, which is then convereted to m
asc500.scanner.setPositionsXYRel(new_position_m)
time.sleep(0.5)

print("stop scanner: ")
print(asc500.scanner.stopScanner())

print("Getting Scanner State: ")
print(asc500.scanner.getScannerState())

print("Getting Scanner Position: ")
print(asc500.scanner.getPositionsXYZRel())

print("Disabling outputs") # SHOULD PERHAPS ALSO BE ENABLED??
print(asc500.base.setOutputs(0))

print("closing scanner: ")
asc500.scanner.closeScanner()

print("Stopping Server: ")
asc500.base.stopServer()