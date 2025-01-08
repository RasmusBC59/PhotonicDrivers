# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 10:03:04 2024

@author: Sven
"""
import numpy as np #scientific data manipulation
import matplotlib.pyplot as plt #basic plotting
import time, io
from serial import Serial
import scipy.io as sio #matlab save

def sys_status(ausgabe):
    """
    SYS_STATUS queries a set of system parameters to characterize the current 
    system state. 

    Parameters
    ----------
    ausgabe : int
        Set ausgabe to 1 to generate command line output, otherwise the output
        is suppressed.

    Returns
    -------
    status : array of float64
        Contains the queried system parameters ordered according to status_cmd.
    status_cmd : array of str1280
        Contains the query commands or the name of the command set.

    """
    
    # can be either a valid query command or a set of commands with the following
    # notation: [Name, cmd1, cmd2, cmd3, ...]
    # only the result of the last command will be stored and output
    status_queries = [
        "Measure:Runtime:Oscillator?\n",
        "Monitor:ModeLock:State?\n",
        "Develop:Enable:Oscillator?\n",
        "Develop:Oscillator:Enable?\n",
        "Develop:Oscillator:Wavfilter?\n",
        "Develop:Oscillator:Current?\n",
        "Monitor:Current:Oscillator?\n",
        "Monitor:DiodePower:Oscillator?\n",
        "Develop:Oscillator:Reprate?\n",
        "Measure:Wavelength:Stokes?\n",
        "Develop:System:Modelock:Position?\n",
        "Develop:Preamp:Enable?\n",
        "Develop:Preamp:Current?\n",
        "Monitor:Current:Preamp?\n",
        "Monitor:DiodePower:Preamp?\n",
        "Develop:Enable:Amplifiers?\n",
        "Develop:Stokes:Enable?\n",
        "Develop:Stokes:Current?\n",
        "Monitor:Current:Stokes?\n",
        "Develop:Pump:Enable?\n",
        "Develop:Pump:Current?\n",
        "Monitor:Current:Pump?\n",
        "Measure:Wavelength:Pump?\n",
        "Measure:Power:Pump?\n",
        "Laser:Wavenumber?\n",
        "Measure:Wavenumber?\n",
        "Monitor:Temperature:Laserhead?\n",
        "Monitor:Temperature:Diode:Oscillator?\n",
        "Monitor:Temperature:Diode:Preamp?\n",
        "Monitor:Temperature:Diode:Mainamp?\n",
        "Monitor:Seed:Pump?\n",
        "Monitor:Seed:Stokes?\n",
        "Monitor:Seed:PD3?\n",
        "Laser:Finetune?\n",
        "Service:Oscillator:Power?\n",
        "Service:Temperature:Laserhead:OsciSink?\n",
        "Service:Temperature:Laserhead:PumpSink?\n",
        "Monitor:Temperature:Diode:Heatsink?\n",
        "Service:Current:TEC:Mainamp?\n",
        "Service:Temperature:Driver:BasePlate?\n",
        "Service:Temperature:Laserhead:Oscillator?\n",
        "Service:Current:TEC:Laserhead:Oscillator?\n",
        "Service:Temperature:Laserhead:Pump?\n",
        "Service:Current:TEC:Laserhead:Pump?\n",
        "Laser:Delay?\n",
        "Develop:Delay:Bits?\n",
        "Laser:Settings:Autodelay:Enable?\n",
        "Laser:Settings:Autodelay:Offset?\n",
        "Laser:Modulation:Enable?\n",
        "Develop:System:Modelock:LastMoved?\n",
        "Laser:Filter?\n",
        "Develop:Filter:Bits?\n"]
    status = np.zeros(len(status_queries))
    
    # query all parameters 
    for i in range(len(status_queries)):
        try:
            if status_queries[i] == "":
                status[i] = 0
            else:
                new_query = status_queries[i]
                laser.write(new_query)
                ans = laser.readline()
                status[i] = ans
        except ValueError as e:
            if ausgabe == 1:
                print(f"Error bei '{status_queries[i].strip()}'({new_query.strip()})! Status: {ans}")
                print(e)
        except ser.SerialTimoutException:
            print(f"Timout for command: {status_queries[i][-1]}")

    if ausgabe == 1:
        print(f"Oscillator Runtime = {status[0]:.1f}, ModeLock Status {int(status[1])}")
        print(f"Modelock Position {int(status[10])}, LastMoved {int(status[49])/60:.1f}")
        print(f"HL Enable: Oscillator {int(status[2])}     - Amplifiers {int(status[15])}    - MOD {int(status[48])}")
        print(f"LL Enable: Osc {int(status[3])} - PreAmp {int(status[11])} - Stokes {int(status[16])} - FOPO {int(status[19])}")
        print(f"Set Wavfilter = {int(status[4])} - Set Wavenumber = {int(status[24])}")
        print(f"Set OutFilter = {int(status[50])} nm - Bits = {int(status[51])}")
        print(f"Meas. Wavelength Osc = {status[9]}, FOPO = {status[22]} -> Wavenumber = {status[25]}")
        print(f"RepRate Position {int(status[8])} with finetune {int(status[33])} % ")
        print(f"Delay Position {(status[44])}mm = {int(status[45])}bits, AutoTune Status {int(status[46])} with Offset {(status[47])}")
        print(f"Power ... FOPO = {status[23]}, Osc = {status[33]}")
        print( '               Curr Set  -  Meas:Curr?   -   Meas:PumpPower?')
        print(f"Oscillator ...  {int(status[5]):<5}   ...   {status[6]:<7}   ...   {status[7]}")
        print(f"PreAmp     ...  {int(status[12]):<5}   ...   {status[13]:<7}   ...   {status[14]}")
        print(f"Stokes     ...  {status[17]:<5}   ...   {status[18]:<7}")
        print(f"FOPO       ...  {status[20]:<5}   ...   {status[21]:<7}")
        print(f"Diode Temp ... Osc {np.round(status[27],1)}°C - PreAmp {np.round(status[28],1)}°C - MainAmp {np.round(status[29],1)}°C")
        print(f"Main TEC   ... Sink Temp. {np.round(status[37],1)}°C - Base Temp. {np.round(status[39],1)}°C - Current {np.round(status[38],2)} A")
        print(f"LH         ... Temp. {np.round(status[26],1)}°C - AUX1 Temp. {np.round(status[35],1)}°C - AUX2 Temp. {np.round(status[36],1)}°C")
        print(f"LH Ch1     ... Temp. {np.round(status[40],1)}°C - Current {np.round(status[41],2)} A")
        print(f"LH Ch2     ... Temp. {np.round(status[42],1)}°C - Current {np.round(status[43],2)} A")
        print(f"PD         ... M0 {status[30]} - M1 {status[31]} - M2 {status[32]}")
    
    return (status, status_queries)

#%% Connect Laser
ser = Serial(port = 'COM27', timeout = 7)
laser = io.TextIOWrapper(io.BufferedRWPair(ser, ser,1),newline = "\n",encoding = "utf-8")
laser._CHUNK_SIZE = 1

#%% MEAS - Power Scan FOPO + STOKES (therm. Pow.)
wavstart = 880
wavend = 950

wavfilter=np.linspace(wavstart,wavend,num = 101,dtype = 'int')
[temp,laserparameter] = sys_status(0)
laserstatus = np.zeros((len(temp),len(wavfilter)))
time0 = time.time()
plt.figure(figsize=[12,8])
for i in range(len(wavfilter)):
    print(f"Current wavfilter: {wavfilter[i]}, Elapsed Time: {time.time()-time0}s")
    laser.write(f"Laser:wavelength {wavfilter[i]}\n")
    laser.readline()
    time.sleep(1.0)
    [laserstatus[:,i],temp] = sys_status(0)
    plt.pause(0.05)
    if i>0:
        plt.clf()
        plt.subplot(2, 2, 1)
        plt.plot(wavfilter[0:i],laserstatus[1,0:i],label = 'ML Status')
        plt.plot(wavfilter[0:i],laserstatus[2,0:i],label = 'Oscillator')
        plt.plot(wavfilter[0:i],laserstatus[15,0:i],label = 'Amplifier')
        plt.ylabel('Status'),plt.grid(1),plt.ylim((-0.1,1.1)),plt.legend()
        plt.subplot(2, 2, 2)
        plt.plot(wavfilter[0:i],laserstatus[22,0:i])
        plt.ylabel('Wavelength in nm'),plt.grid(1)
        plt.subplot(2, 2, 3)
        plt.plot(wavfilter[0:i],laserstatus[27,0:i],label = 'Oscillator Diode')
        plt.plot(wavfilter[0:i],laserstatus[28,0:i],label = 'PreAmp Diode')
        plt.plot(wavfilter[0:i],laserstatus[29,0:i],label = 'MainAmp Diode')
        plt.xlabel('Wavelength Set in nm'),plt.ylabel('Temperature in C'),plt.grid(1),plt.legend()
        plt.subplot(2, 2, 4)
        plt.plot(wavfilter[0:i],laserstatus[23,0:i])
        plt.xlabel('Wavelength Set in nm'),plt.ylabel('Power Pump in a.u.'),plt.grid(1)
        plt.tight_layout()
        plt.pause(0.05)

print(f"Total time: {(time.time()-time0)/60} minutes")

# save data
variables = (('wavfilter','laserstatus','laserparameter'))
datapath = './'
sio.savemat(datapath+"power_scan.mat",dict( (name,eval(name)) for name in variables))


#%% PLOT - Power Scan
plt.figure(1,figsize=[12,8])
plt.clf()
plt.subplot(2, 2, 1)
plt.plot(wavfilter,laserstatus[1,:],label = 'ML Status')
plt.plot(wavfilter,laserstatus[2,:],label = 'Oscillator')
plt.plot(wavfilter,laserstatus[15,:],label = 'Amplifier')
plt.ylabel('Status'),plt.grid(1),plt.ylim((-0.1,1.1)),plt.legend()
plt.subplot(2, 2, 2)
plt.plot(wavfilter,laserstatus[22,:])
plt.ylabel('Wavelength in nm'),plt.grid(1)
plt.subplot(2, 2, 3)
plt.plot(wavfilter,laserstatus[27,:],label = 'Oscillator Diode')
plt.plot(wavfilter,laserstatus[28,:],label = 'PreAmp Diode')
plt.plot(wavfilter,laserstatus[29,:],label = 'MainAmp Diode')
plt.xlabel('Wavelength Set in nm'),plt.ylabel('Temperature in C'),plt.grid(1),plt.legend()
plt.subplot(2, 2, 4)
plt.plot(wavfilter,laserstatus[23,:])
plt.xlabel('Wavelength Set in nm'),plt.ylabel('Power Pump in a.u.'),plt.grid(1)
plt.tight_layout()

