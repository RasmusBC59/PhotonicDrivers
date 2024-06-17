## Python sample script to communicate with RLS Picus laser
import datetime
import tkinter as tk

import h5py
import numpy as np
import pyvisa
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from photonicdrivers.Instruments.Implementations.Power_Meters import \
    Thorlabs_PM100U


def add_dict_to_h5(dict, group):
    for key, element in dict.items():
        group.attrs[key] = element


instrument_list = []

resource_manager = pyvisa.ResourceManager()
print(resource_manager.list_resources())

input_power_meter = Thorlabs_PM100U(resource_manager, 'USB0::0x1313::0x8078::P0045344::0::INSTR',
                                    "C:/Users/NQCPQP/PycharmProjects/LabController/Code/Settings/Thorlabs_PM100U/Thorlabs_PM100U_Settings_1.txt")
input_power_meter.connect()
instrument_list.append(input_power_meter)

output_power_meter = Thorlabs_PM100U(resource_manager, 'USB0::0x1313::0x8078::P0041989::0::INSTR',
                                     "C:/Users/NQCPQP/PycharmProjects/LabController/Code/Settings/Thorlabs_PM100U/Thorlabs_PM100U_Settings_2.txt")
output_power_meter.connect()

instrument_list.append(output_power_meter)

wavelength_list_loop = range(910, 980, 10)

toptica_laser = Toptica_CTL950(IP_address='10.209.67.103',
                               settings_path="C:/Users/NQCPQP/PycharmProjects/LabController/Code/Settings"
                                             "/Toptica_CTL950/Toptica_CTL950_Settings.txt")
toptica_laser.connect()
toptica_laser.enable_emission()

toptica_laser.set_power_stabilization(True)
toptica_laser.print_emission_status()

instrument_list.append(toptica_laser)

output_power_list = []
input_power_list = []
wavelength_list = []

beginning_time = datetime.datetime.now()

# Create a Tkinter window
root = tk.Tk()
root.title("Matplotlib Plot in Tkinter")

# Create an empty plot
fig, ax = plt.subplots()
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_title('Matplotlib Plot in Tkinter')

# Set up the axes limits
ax.set_xlim(910, 980)
#ax.set_ylim(0, 20)


# Initialize an empty line object
line, = plt.plot([], [], 'bo-')

canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

for wavelength in wavelength_list_loop:
    toptica_laser.set_wavelength(wavelength)
    plt.pause(0.1)
    output_power_list.append(output_power_meter.get_detector_power())
    input_power_list.append(input_power_meter.get_detector_power())
    wavelength_list.append(wavelength)

    line.set_xdata(wavelength_list)
    line.set_ydata(output_power_list)

    # Update y-axis limits to match the min and max of y-data
    ax.set_ylim(np.min(output_power_list) - 1, np.max(output_power_list) + 1)

    canvas.draw()
    plt.pause(1)

root.mainloop()

chip_id = "photonicdev5324"
setup_id = "room_temp_KK4_v1.00.00"
device_id = "11"
filename = beginning_time.strftime("%Y-%m-%d_%H-%M-%S") + "_setup_id_" + setup_id + "_subject_id_" + chip_id + "_device_id_" + device_id

with h5py.File("N:/SCI-NBI-NQCP/Phot/rawData/transmission/" + filename + ".hdf5", 'w') as f:
    # Create a group and add metadata
    meta_data_group = f.create_group('meta_data')
    meta_data_group.attrs['author'] = "Magnus_Linnet_Madsen"
    meta_data_group.attrs['time_stamp'] = beginning_time.strftime("%Y-%m-%d_%H-%M-%S")
    meta_data_group.attrs['setup_id'] = setup_id
    meta_data_group.attrs['chip_id'] = chip_id
    meta_data_group.attrs['device_id'] = device_id

    # Create a dataset and add metadata
    data_group = f.create_group('data')

    data_input_power = data_group.create_dataset('input_power', data=input_power_list)
    data_input_power.attrs['units'] = "W"

    data_output_power = data_group.create_dataset('output_power', data=output_power_list)
    data_output_power.attrs['units'] = "W"

    data_wavelength = data_group.create_dataset('wavelength', data=wavelength_list)
    data_wavelength.attrs['units'] = "nm"

for instrument in instrument_list:
    instrument.disconnect()