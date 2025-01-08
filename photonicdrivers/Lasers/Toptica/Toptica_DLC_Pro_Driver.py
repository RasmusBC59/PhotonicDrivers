import toptica.lasersdk.dlcpro.v3_0_1 as toptica
from photonicdrivers.Abstract.Connectable import Connectable

class Toptica_DLC_PRO_Driver(Connectable):
    """
    A driver class for controlling a Toptica CTL950 laser via the Toptica DLC pro laser controller.

    Attributes:
        ip_address (str): The IP address of the Toptica CTL laser.
        laser_controller: The DLC pro laser controller object from the Toptica SDK.
    """

    def __init__(self, ip_address='10.209.67.103'):
        """
        Initializes the laser controller by establishing a network connection to the specified IP address.

        Args:
            ip_address (str): The IP address of the Toptica CTL laser. Default is '10.209.67.103'.
        """
        self.ip_address = ip_address
        self.laser_controller = toptica.DLCpro(toptica.NetworkConnection(self.ip_address))

    def connect(self):
        """
        Opens the connection to the laser controller.
        """
        self.laser_controller.open()

    def disconnect(self):
        """
        Closes the connection to the laser controller.
        """
        self.laser_controller.close()

    def is_connected(self):
        try:
            return self.laser_controller.serial_number.get() is not None
        except ConnectionError:
            return False
        except Exception:
            return False

    ###### SHALLOW SCAN ######

    def set_scan_enabled(self, enable_bool):
        """
        Enables or disables the shallow scan operation on the laser.

        Args:
            enable_bool (bool): True to enable the scan, False to disable it.
        """
        self.laser_controller.laser1.scan.enabled.set(enable_bool)

    def get_scan_enabled(self):
        """
        Retrieves the current status of the shallow scan operation.

        Returns:
            bool: The current status of the shallow scan (enabled or disabled).
        """
        return self.laser_controller.laser1.scan.enabled.get()

    def set_scan_amplitude(self, scan_amplitude):
        """
        Sets the amplitude for the shallow scan.

        Args:
            scan_amplitude (float): The amplitude of the shallow scan.
        """
        self.laser_controller.laser1.scan.amplitude.set(scan_amplitude)

    def get_scan_amplitude(self):
        """
        Retrieves the current amplitude of the shallow scan.

        Returns:
            float: The current amplitude of the shallow scan.
        """
        return self.laser_controller.laser1.scan.amplitude.get()

    def set_scan_offset(self, offset):
        """
        Sets the offset for the shallow scan.

        Args:
            offset (float): The offset value for the shallow scan.
        """
        self.laser_controller.laser1.scan.offset.set(offset)

    def get_scan_offset(self):
        """
        Retrieves the current offset of the shallow scan.

        Returns:
            float: The current offset of the shallow scan.
        """
        return self.laser_controller.laser1.scan.offset.get()

    def set_scan_start(self, start):
        """
        Sets the start position for the shallow scan.

        Args:
            start (float): The start position of the shallow scan.
        """
        self.laser_controller.laser1.scan.start.set(start)

    def get_scan_start(self):
        """
        Retrieves the current start position of the shallow scan.

        Returns:
            float: The current start position of the shallow scan.
        """
        return self.laser_controller.laser1.scan.start.get()

    def set_scan_end(self, end):
        """
        Sets the end position for the shallow scan.

        Args:
            end (float): The end position of the shallow scan.
        """
        self.laser_controller.laser1.scan.end.set(end)

    def get_scan_end(self):
        """
        Retrieves the current end position of the shallow scan.

        Returns:
            float: The current end position of the shallow scan.
        """
        return self.laser_controller.laser1.scan.end.get()

    def set_scan_frequency(self, frequency):
        """
        Sets the frequency for the shallow scan.

        Args:
            frequency (float): The frequency of the shallow scan.
        """
        self.laser_controller.laser1.scan.frequency.set(frequency)

    def get_scan_frequency(self):
        """
        Retrieves the current frequency of the shallow scan.

        Returns:
            float: The current frequency of the shallow scan.
        """
        return self.laser_controller.laser1.scan.frequency.get()

    def set_scan_hold(self, hold):
        """
        Sets the hold time for the shallow scan.

        Args:
            hold (float): The hold time for the shallow scan.
        """
        self.laser_controller.laser1.scan.hold.set(hold)

    def get_scan_hold(self):
        """
        Retrieves the current hold time of the shallow scan.

        Returns:
            float: The current hold time of the shallow scan.
        """
        return self.laser_controller.laser1.scan.hold.get()

    def set_scan_output_channel(self, output_channel):
        """
        Sets the output channel for the shallow scan.

        Args:
            output_channel (str): The output channel for the shallow scan.
        """
        self.laser_controller.laser1.scan.output_channel.set(output_channel)

    def get_scan_output_channel(self):
        """
        Retrieves the current output channel of the shallow scan.

        Returns:
            str: The current output channel of the shallow scan.
        """
        return self.laser_controller.laser1.scan.output_channel.get()

    def set_scan_phase_shift(self, phase_shift):
        """
        Sets the phase shift for the shallow scan.

        Args:
            phase_shift (float): The phase shift for the shallow scan.
        """
        self.laser_controller.laser1.scan.phase_shift.set(phase_shift)

    def get_scan_phase_shift(self):
        """
        Retrieves the current phase shift of the shallow scan.

        Returns:
            float: The current phase shift of the shallow scan.
        """
        return self.laser_controller.laser1.scan.phase_shift.get()

    def set_scan_signal_type(self, signal_type):
        """
        Sets the signal type for the shallow scan.

        Args:
            signal_type (str): The signal type for the shallow scan.
        """
        self.laser_controller.laser1.scan.signal_type.set(signal_type)

    def get_scan_signal_type(self):
        """
        Retrieves the current signal type of the shallow scan.

        Returns:
            str: The current signal type of the shallow scan.
        """
        return self.laser_controller.laser1.scan.signal_type.get()

    def get_scan_unit(self):
        """
        Retrieves the current unit of the shallow scan.

        Returns:
            str: The current unit of the shallow scan.
        """
        return self.laser_controller.laser1.scan.unit.get()

    ###### WIDE SCAN ######

    def set_wide_scan_continuous_mode(self, enable_bool):
        """
        Enables or disables the continuous mode for the wide scan.

        Args:
            enable_bool (bool): True to enable continuous mode, False to disable it.
        """
        self.laser_controller.laser1.wide_scan.continuous_mode.set(enable_bool)

    def get_wide_scan_continuous_mode(self):
        """
        Retrieves the current status of the wide scan continuous mode.

        Returns:
            bool: The current status of the wide scan continuous mode (enabled or disabled).
        """
        return self.laser_controller.laser1.wide_scan.continuous_mode.get()

    def set_wide_scan_offset(self, offset):
        """
        Sets the offset for the wide scan.

        Args:
            offset (float): The offset value for the wide scan.
        """
        self.laser_controller.laser1.wide_scan.offset.set(offset)

    def get_wide_scan_offset(self):
        """
        Retrieves the current offset of the wide scan.

        Returns:
            float: The current offset of the wide scan.
        """
        return self.laser_controller.laser1.wide_scan.offset.get()

    def set_wide_scan_amplitude(self, amplitude):
        """
        Sets the amplitude for the wide scan.

        Args:
            amplitude (float): The amplitude of the wide scan.
        """
        self.laser_controller.laser1.wide_scan.amplitude.set(amplitude)

    def get_wide_scan_amplitude(self):
        """
        Retrieves the current amplitude of the wide scan.

        Returns:
            float: The current amplitude of the wide scan.
        """
        return self.laser_controller.laser1.wide_scan.amplitude.get()

    def set_wide_scan_begin(self, start_wavelength):
        """
        Sets the start wavelength for the wide scan.

        Args:
            start_wavelength (float): The start wavelength of the wide scan.
        """
        self.laser_controller.laser1.wide_scan.scan_begin.set(start_wavelength)

    def get_wide_scan_begin(self):
        """
        Retrieves the current start wavelength of the wide scan.

        Returns:
            float: The current start wavelength of the wide scan.
        """
        return self.laser_controller.laser1.wide_scan.scan_begin.get()

    def set_wide_scan_end(self, end_wavelength):
        """
        Sets the end wavelength for the wide scan.

        Args:
            end_wavelength (float): The end wavelength of the wide scan.
        """
        self.laser_controller.laser1.wide_scan.scan_end.set(end_wavelength)

    def get_wide_scan_end(self):
        """
        Retrieves the current end wavelength of the wide scan.

        Returns:
            float: The current end wavelength of the wide scan.
        """
        return self.laser_controller.laser1.wide_scan.scan_end.get()

    def set_wide_scan_output_channel(self, output_channel):
        """
        Sets the output channel for the wide scan.

        Args:
            output_channel (str): The output channel for the wide scan.
        """
        self.laser_controller.laser1.wide_scan.output_channel.set(output_channel)

    def get_wide_scan_output_channel(self):
        """
        Retrieves the current output channel of the wide scan.

        Returns:
            str: The current output channel of the wide scan.
        """
        return self.laser_controller.laser1.wide_scan.output_channel.get()

    def set_wide_scan_duration(self, duration):
        """
        Sets the duration for the wide scan.

        Args:
            duration (float): The duration of the wide scan.
        """
        self.laser_controller.laser1.wide_scan.duration.set(duration)

    def get_wide_scan_duration(self):
        """
        Retrieves the current duration of the wide scan.

        Returns:
            float: The current duration of the wide scan.
        """
        return self.laser_controller.laser1.wide_scan.duration.get()

    def get_wide_scan_remaining_time(self):
        """
        Retrieves the remaining time for the wide scan.

        Returns:
            float: The remaining time of the wide scan.
        """
        return self.laser_controller.laser1.wide_scan.remaining_time.get()

    #### CONNECTION ####

    def set_diode(self, enable_bool):
        """
        Enables or disables the diode.

        Args:
            enable_bool (bool): True to enable the diode, False to disable it.
        """
        self.laser_controller.laser1.dl.cc.enabled.set(enable_bool)

    def get_wavelength(self):
        """
        Retrieves the current wavelength of the laser.

        Returns:
            float: The current wavelength of the laser in nanometers (nm).
        """
        return self.laser_controller.laser1.ctl.wavelength_act.get()

    def set_wavelength(self, wavelength_nm: float):
        """
        Sets the wavelength of the laser.

        Args:
            wavelength_nm (float): The desired wavelength of the laser in nanometers (nm).
        """
        self.laser_controller.laser1.ctl.wavelength_set.set(wavelength_nm)

    def get_power(self):
        """
        Retrieves the current power of the laser.

        Returns:
            float: The current power of the laser in milliwatts (mW).
        """
        return self.laser_controller.laser1.ctl.power.power_act.get()

    def set_power(self, power_mW: float):
        """
        Sets the power of the laser.

        Args:
            power_mW (float): The desired power of the laser in milliwatts (mW).
        """
        self.laser_controller.laser1.power_stabilization.setpoint.set(power_mW)

    def get_emission_status(self) -> bool:
        """
        Retrieves the emission status of the laser.

        Returns:
            bool: True if the laser is on, False if the laser is off.
        """
        return self.laser_controller.emission.get()

    def get_power_stabilization(self) -> bool:
        """
        Retrieves the power stabilization status of the laser.

        Returns:
            bool: True if power stabilization is enabled, False otherwise.
        """
        return self.laser_controller.laser1.power_stabilization.enabled.get()

    def set_power_stabilization(self, power_stabilization: bool):
        """
        Enables or disables the power stabilization of the laser.

        Args:
            power_stabilization (bool): True to enable power stabilization, False to disable it.
        """
        self.laser_controller.laser1.power_stabilization.enabled.set(power_stabilization)

    def play_welcome(self):
        """
        Plays a welcome sound from the laser controller.
        """
        self.laser_controller.buzzer.play_welcome()

    def get_power_stabilization_parameters(self):
        """
        Retrieves the parameters for power stabilization.

        Returns:
            tuple: A tuple containing the gain, P, I, and D parameters for power stabilization.
        """
        gain = self.laser_controller.laser1.power_stabilization.gain.all.get()
        p = self.laser_controller.laser1.power_stabilization.gain.p.get()
        i = self.laser_controller.laser1.power_stabilization.gain.i.get()
        d = self.laser_controller.laser1.power_stabilization.gain.d.get()
        return gain, p, i, d

    def set_power_stabilization_parameters(self, p, i, d=0, gain=1):
        """
        Sets the parameters for power stabilization.

        Args:
            p (float): Proportional gain.
            i (float): Integral gain.
            d (float, optional): Derivative gain. Default is 0.
            gain (float, optional): Overall gain. Default is 1.
        """
        self.laser_controller.laser1.power_stabilization.gain.all.set(gain)
        self.laser_controller.laser1.power_stabilization.gain.p.set(p)
        self.laser_controller.laser1.power_stabilization.gain.i.set(i)
        self.laser_controller.laser1.power_stabilization.gain.d.set(d)
