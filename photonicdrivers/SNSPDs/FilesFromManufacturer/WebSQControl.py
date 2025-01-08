#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
The MIT License (MIT)

Copyright (c) 2020 Single Quantum B. V. and Andreas Fognini

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import socket
import json
import threading
import time
import re
import ast
import sys
import numpy as np
from datetime import datetime

# Next part (Start -> End) based on: http://www.theorangeduck.com/page/synchronized-python 2016-June-1st
# Which is released under BSD3 license
# Start


def synchronized_method(method, *args, **kws):
    outer_lock = threading.Lock()
    lock_name = "__" + method.__name__ + "_lock" + "__"

    def sync_method(self, *args, **kws):
        with outer_lock:
            if not hasattr(self, lock_name):
                setattr(self, lock_name, threading.Lock())
            lock = getattr(self, lock_name)
            with lock:
                return method(self, *args, **kws)
    sync_method.__name__ = method.__name__
    sync_method.__doc__ = method.__doc__
    sync_method.__module__ = method.__module__
    return sync_method


def _synchronized_method(method):
    return decorate(method, _synchronized_method) # type: ignore


def synchronized_with_attr(lock_name):
    def decorator(method):
        def synced_method(self, *args, **kws):
            lock = getattr(self, lock_name)
            with lock:
                return method(self, *args, **kws)
        synced_method.__name__ = method.__name__
        synced_method.__doc__ = method.__doc__
        synced_method.__module__ = method.__module__
        return synced_method
    return decorator
# End


class SQTalk(threading.Thread):
    def __init__(self, TCP_IP_ADR='localhost', TCP_IP_PORT=12000, error_callback=None, TIME_OUT=0.1):
        threading.Thread.__init__(self)
        self.TCP_IP_ADR = TCP_IP_ADR
        self.TCP_IP_PORT = TCP_IP_PORT

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(TIME_OUT)
        self.socket.connect((self.TCP_IP_ADR, self.TCP_IP_PORT))
        self.BUFFER = 10000000
        self.shutdown = False
        self.labelProps = dict()

        self.error_callback = error_callback

        self.lock = threading.Lock()

    @synchronized_method
    def close(self):
        # Print("Closing Socket")
        self.socket.close()
        self.shutdown = True

    @synchronized_method
    def send(self, msg):
        if sys.version_info.major == 3:
            self.socket.send(bytes(msg, "utf-8"))
        if sys.version_info.major == 2:
            self.socket.send(msg)

    def sub_jsons(self, msg):
        """Return sub json strings.
        {}{} will be returned as [{},{}]
        """
        i = 0
        result = []
        split_msg = msg.split('}{')
        for s in range(len(split_msg)):
            if i == 0 and len(split_msg) == 1:
                result.append(split_msg[s])
            elif i == 0 and len(split_msg) > 1:
                result.append(split_msg[s] + "}")
            elif i == len(split_msg) - 1 and len(split_msg) > 1:
                result.append("{" + split_msg[s])
            else:
                result.append("{" + split_msg[s] + "}")
            i += 1
        return result

    @synchronized_method
    def add_labelProps(self, data):
        if "label" in data.keys():
            # After get labelProps, queries also bounds, units etc...
            if isinstance(data["value"], (dict)):
                self.labelProps[data["label"]] = data["value"]
            # General label communication, for example from broadcasts
            else:
                try:
                    self.labelProps[data["label"]
                                    ]["value"] = data["value"]
                except Exception:
                    None

    @synchronized_method
    def check_error(self, data):
        if "label" in data.keys():
            if "Error" in data["label"]:
                self.error_callback(data["value"])

    @synchronized_method
    def get_label(self, label):
        timeout = 10
        dt = .1
        i = 0
        while True:
            if i * dt > timeout:
                raise IOError("Could not acquire label")
            try:
                return self.labelProps[label]
            except Exception:
                self.send(json.dumps({"request": "labelProps", "value": "None"}))
                time.sleep(dt)
            i += 1

    @synchronized_method
    def get_all_labels(self, label):
        return self.labelProps

    def run(self):
        self.send(json.dumps({"request": "labelProps", "value": "None"}))
        rcv_msg = []

        while self.shutdown is False:
            try:
                rcv = ""+rcv_msg[1]
            except:
                rcv = ""
            data = {}
            r = ""
            while ("\x17" not in rcv) and (self.shutdown == False):
                try:
                    if sys.version_info.major == 3:
                        r = str(self.socket.recv(self.BUFFER), 'utf-8')
                    elif sys.version_info.major == 2:
                        r = self.socket.recv(self.BUFFER)
                except Exception as e:
                    None
                rcv = rcv + r

            rcv_msg = rcv.split("\x17")

            for rcv_line in rcv_msg:
                rcv_split = self.sub_jsons(rcv_line)
                for msg in rcv_split:
                    try:
                        data = json.loads(msg)
                    except Exception:
                        None

                    with self.lock:
                        self.add_labelProps(data)
                        self.check_error(data)


class SQCounts(threading.Thread):
    def __init__(self, TCP_IP_ADR='localhost', TCP_IP_PORT=12345, CNTS_BUFFER=100, TIME_OUT=10):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.rlock = threading.RLock()
        self.TCP_IP_ADR = TCP_IP_ADR
        self.TCP_IP_PORT = TCP_IP_PORT

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(TIME_OUT)
        self.socket.connect((self.TCP_IP_ADR, self.TCP_IP_PORT))
        # self.socket.settimeout(.1)
        self.BUFFER = 1000000
        self.shutdown = False

        self.cnts = []
        self.CNTS_BUFFER = CNTS_BUFFER
        self.n = 0

    @synchronized_method
    def close(self):
        #print("Closing Socket")
        self.socket.close()
        self.shutdown = True

    @synchronized_method
    def get_n(self, n):
        n0 = self.n
        while self.n < n0 + n:
            time.sleep(0.001)
        cnts = self.cnts
        return cnts[-n:]

    def run(self):
        data = []
        while self.shutdown == False:
            if sys.version_info.major == 3:
                try:
                    data_raw = str(self.socket.recv(self.BUFFER), 'utf-8')
                except:
                    data_raw = ""
                    None  # Happens while closing
            elif sys.version_info.major == 2:
                data_raw = self.socket.recv(self.BUFFER)

            data_newline = data_raw.split('\n')

            v = []
            for d in data_newline[0].split(','):
                try:
                    v.append(float(d))
                except:
                    None

            with self.lock:
                self.cnts.append(v)
                # Keep Size of self.cnts
                l = len(self.cnts)
                if l > self.CNTS_BUFFER:
                    self.cnts = self.cnts[l-self.CNTS_BUFFER:]
                self.n += 1


class WebSQControl(object):
    """

    Python control class for the SNSNPD atlas driver.
    It implements many functions that can be found in the SNSPD manual.

    :param TCP_IP_ADR: name of the computer. Defaults to 'localhost'
    :type TCP_IP_ADR: string
    :param TCP_IP_PORT: port number to use. Defaults to 12000
    :type TCP_IP_PORT: int
    :param TIME_OUT: Time out time in seconds. Defaults to 0.1 s
    :type TIME_OUT: float

    """
    def __init__(self, TCP_IP_ADR='localhost', CONTROL_PORT=12000, COUNTS_PORT=12345):
        self.TCP_IP_ADR = TCP_IP_ADR
        self.CONTROL_PORT = CONTROL_PORT
        self.COUNTS_PORT = COUNTS_PORT
        self._number_of_detectors = None
        self.connected = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self, TIME_OUT=10):
        if not self.connected:
            self.talk = SQTalk(TCP_IP_ADR=self.TCP_IP_ADR,  TCP_IP_PORT=self.CONTROL_PORT,
                               error_callback=self.error, TIME_OUT=TIME_OUT)
            # Daemonic Thread close when main progam is closed
            self.talk.daemon = True
            self.talk.start()

            self.cnts = SQCounts(TCP_IP_ADR=self.TCP_IP_ADR,
                                 TCP_IP_PORT=self.COUNTS_PORT, TIME_OUT=TIME_OUT)
            # Daemonic Thread close when main progam is closed
            self.cnts.daemon = True
            self.cnts.start()

            self.connected = True

        self.get_number_of_detectors()

    def close(self):
        if self.connected:
            self.connected = False
            self.talk.close()
            self.talk.join()

    def error(self, error_msg):
        """Called in case of an error"""
        print("ERROR DETECTED")
        print(error_msg)

    def acquire_cnts(self, n):
        """
        Acquire n-times count measurements. It retrives the counts for each channel n times.

        :param n: number of count measurements
        :type n: int

        :return counts: Acquired counts for each channel with timestamp in first column.
        :rtype counts: numpy array of length (Nchannels + 1, n)

        """
        return self.cnts.get_n(n)

    def set_measurement_periode(self, t_in_ms):
        """
        Sets the integration time in ms, also called measurement period.

        NOTE: the minimum value can be 10 ms

        :param t_in_ms: integration time to set (in ms)
        :type t_in_ms: int

        """
        msg = json.dumps(
            dict(
                command="SetMeasurementPeriod",
                label="InptMeasurementPeriod",
                value=t_in_ms))
        self.talk.send(msg)

    def get_number_of_detectors(self):
        """ Reads the number of detectors present in the Atlas driver. """

        self._number_of_detectors = self.talk.get_label("NumberOfDetectors")["value"]
        return self._number_of_detectors

    def get_measurement_periode(self):
        """
        Gets measurement period (integration time) in ms.

        :return dt: integration time in ms
        :rtype dt: float

        """
        self._dt = self.talk.get_label("InptMeasurementPeriod")["value"]
        return self._dt

    def get_bias_current(self):
        """
        Gets the bias current used to bias the SNSPDS. It returns a vector of dimension Nchannels.

        """
        return self.talk.get_label("BiasCurrent")["value"]

    def get_trigger_level(self):
        """
        Gets the current trigger level for the counters for each channel. It returns a vector of dimension Nchannels.

        """
        return self.talk.get_label("TriggerLevel")["value"]

    def get_bias_voltage(self):
        """
        Gets the bias voltage for the counters for each channel. It returns a vector of dimension Nchannels.

        """
        msg = json.dumps(dict(request="BiasVoltage"))
        self.talk.send(msg)
        return self.talk.get_label("BiasVoltage")["value"]

    def set_bias_current(self, current_in_uA):
        """
        Sets the bias current used to bias the SNSPDS in uA.

        :param current_in_uA: array of currents to set in uA
        :type current_in_uA: array of Nchannel floats

        """
        array = current_in_uA
        msg = json.dumps(dict(command="SetAllBiasCurrents",
                              label="BiasCurrent", value=array))
        self.talk.send(msg)

    def set_trigger_level(self, trigger_level_mV):
        """
        Sets the current trigger level for the counters for each channel.

        :param trigger_level_mV: array of trigger levels to set (in mV)
        :type trigger_level_mV: array of Nchannel floats

        """
        array = trigger_level_mV
        msg = json.dumps(dict(command="SetAllTriggerLevels",
                              label="TriggerLevel", value=array))
        self.talk.send(msg)

    def enable_detectors(self, state=True):
        """ Enables the bias current to the SNSPDs

         :param state: state for the enable.
         :type state: boolean
         """
        msg = json.dumps(dict(command="DetectorEnable", label='DetectorEnable', value=state))
        self.talk.send(msg)

    def get_enable_detectors(self):
        """
        Gets the status of the SNSPDs. True means the detectors are enabled, i.e.
        they are biased and can detect photons.


        """
        return self.talk.get_label("DetectorEnable")["value"]

    def auto_bias_calibration(self, state=True, DarkCounts=[100, 100, 100, 100]):
        """        
        Starts an automatic bias current search. The bias current will be set to match the dark counts self.
        For this function to work properly the detectors should not be exposed to light.
        This function is blocking.
        Returns the found bias currents.

        :param state: boolean to see if the command is running
        :param DarkCounts: measured dark counts for each detector. It defaults to [100, 100, 100, 100]
        """
        msg = json.dumps(dict(command="DarkCountsAutoIV", value=DarkCounts))
        self.talk.send(msg)
        msg = json.dumps(dict(command="AutoCaliBiasCurrents", value=state))
        self.talk.send(msg)
        time.sleep(1)
        while self.talk.get_label("StartAutoIV")["value"] == True:
            time.sleep(.1)
        return self.talk.get_label("BiasCurrentAutoIV")["value"]

    def ic_scan_history(self):
        """ Gets the IC history.
            It returns the last detector characterization measurement.
            It returns a matrix where the first column contains the current and the rest the counts for each detector.

        :returns: M: matrix where the first column is the current and the rest are the counts for each detector.
        """
        # IC
        msg = json.dumps(dict(request="IVHistory"))
        self.talk.send(msg)
        ic = self.talk.get_label("ic_scan_history")["value"]

        I = []
        C = []
        for ind in range(len(ic)):
            I.append(ic[ind]['biasCurrent'])
            c = []
            for n in range(self._number_of_detectors):
                c.append(ic[ind]['y{}'.format(n + 1)])
            C.append(c)
        out = np.zeros((len(I), self._number_of_detectors + 1))
        out[:, 0] = I
        out[:, 1:] = C
        return out

    def iv_scan_history(self):
        """ Gets the IV history.
            It returns the last IV scan characterization measurement.
            It returns a matrix where the first column contains the current and the rest the voltage for each detector.

        :returns: M: matrix where the first column is the current and the rest are the voltage for each detector.
        """
        # IV
        msg = json.dumps(dict(request="IVHistory"))
        self.talk.send(msg)
        iv = self.talk.get_label("iv_scan_history")["value"]

        I = []
        V = []
        for ind in range(len(iv)):
            I.append(iv[ind]['biasCurrent'])
            v = []
            for n in range(self._number_of_detectors):
                v.append(iv[ind]['v{}'.format(n + 1)])
            V.append(v)
        out = np.zeros((len(I), self._number_of_detectors + 1))
        out[:, 0] = I
        out[:, 1:] = V
        return out

    def iv_scan_run(self, state=True):
        """
        Controls the IV scan. When the state is set to true, you start the scan and with False you stop it.

        The output data is retrieved with the iv_history method.

        :param state: set the state to true to run the IV and to False to stop it.
        :type state: bool

        """

        if not self.iv_scan_state() and state is True:
            # start scan
            self.talk.send(json.dumps(dict(command="IVScanEnable", label = "IVScanEnable", value=state)))
            self.iv_scan_state()
        elif self.iv_scan_state() and state is False:
            # stop scan
            self.talk.send(json.dumps(dict(command="IVScanEnable", label="IVScanEnable", value=state)))
            self.iv_scan_state()

    def iv_scan_setup(self, start=0, stop=30, step=0.5):
        """ Sets up the settings for an IV scan to record the IV curves and
        the I vs Counts curves. The counts counted in the current integration time.
        In order to actually start the measurement you need to use the iv_scan_run method.
        In order to read the output of these curves you need to use the iv_history method.
        Note that this method does not freeze the driver.

        :param start: starting bias current value for the IV curve in uA (-90.9 < I < 90.9)
        :type start: float
        :param stop: stopping bias current value for the IV curve in uA (-90.9 < I < 90.9)
        :type start: float
        :param step: bias current steps used for the IV scan
        :type step: float

        """
        print('Websq is setting up the IV scan: start = {}, stop = {}, step = {}'.format(start, stop, step))
        # set start
        msg = json.dumps(dict(label="IVScanStart", value=start))
        self.talk.send(msg)

        # set stop
        msg = json.dumps(dict(label="IVScanEnd", value=stop))
        self.talk.send(msg)

        # step
        msg = json.dumps(dict(label="IVScanIncrement", value=step))
        self.talk.send(msg)

        # reset counts
        # self.talk.send(json.dumps(dict(command="RecordCountsReset")))

    def iv_scan_state(self):
        """Gets the state of the IV Scan. It is true if the scan is running and false if it is not running.

        """
        return self.talk.get_label("IVScanEnable")["value"]

    def get_temperature_stage_1(self):
        """ Gets the cryo temperature of the first stage (warmer, ~40k)"""
        t, T, T2, _, _, _ = self.get_cryo_temperature()
        print(T)
        # print('Cryo temp stage 2: time = {}, T = {}.Length={}'.format(t[-1], T2[-1], len(T2)))
        return t, T2

    def get_temperature_stage_2(self):
        """ Gets the cryo temperature of the second stage (coldest, ~2.5K)"""
        t, T, T2, _, _, _ = self.get_cryo_temperature()
        # print('Cryo temp stage 2: time = {}, T = {}.Length={}'.format(t[-1],T[-1], len(T)))
        return t, T

    def get_board_temperature(self):
        """ Gets the boards temperature"""
        t, _, _, _, T1, T2 = self.get_cryo_temperature()
        return t, T1, T2

    def get_cryo_temperature(self):
        """
        Gets the history of the temperature (last 200 values) for all the available temperatures

        :returns t: time (epoc), T


        """
        msg = json.dumps(dict(request="TemperatureHistory"))
        self.talk.send(msg)
        time.sleep(1)
        D = self.talk.get_label("temperature_long_memory")#["value"]
        #print('All dictionary \n {}'.format(D))
        # get data
        T = D['T'] # cold, 2nd stage (~2.5K)
        T2 = D['T2'] # warm, 1st stage (~40K)
        # get time
        Time = D['x']
        # transform the time stamps into epoc
        t = []
        for tt in Time:
            t.append(int((datetime.strptime(tt, "%d-%b-%y %H:%M:%S.%f") - datetime(1970,1,1)).total_seconds()))

        # more info that comes with it.
        v_av =D['V_avrg']
        board_T1 = D['BoardTemp1']
        board_T2 = D['BoardTemp2']

        return t, T, T2, v_av, board_T1, board_T2


if __name__ == "__main__":
    driver_number = 1
    with WebSQControl(TCP_IP_ADR="192.168.1.{}".format(driver_number)) as websq:
        websq.connect()
        websq.set_measurement_periode(10)       # sets the integration time to 10ms
        websq.enable_detectors(True)            # starts the measurement

        print("Automatically finding bias current, avoid Light exposure")
        found_bias_current = websq.auto_bias_calibration(
            DarkCounts=[100, 100, 100, 100])
        print("Bias current: " + str(found_bias_current))

        N_times = 10
        Nmeasurements = 3
        i = 1
        while i < N_times:
            websq.set_bias_current(current_in_uA=[12.0, 8.0, 3.0, 8.0])
            websq.set_trigger_level(trigger_level_mV=[23.0, 24.0, 25.0, 26.0])
            print("{} Measurements: {}".format(Nmeasurements, websq.acquire_cnts(Nmeasurements)))
            print('Measurement period = Integration time = {} ms'.format(websq.get_measurement_periode()))
            print('Bias current = {} uA'.format(websq.get_bias_current()))
            print('Trigger level = {} mV'.format(websq.get_trigger_level()))
            print("Bias Voltage: {} mV".format(websq.get_bias_voltage()))
            i+=1

