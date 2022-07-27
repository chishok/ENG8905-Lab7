import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# data output path
filepath = 'sampledata.npz'
# sample figure dpi, size (inches), and filename
plot_dpi = 200
plot_width = 7
plot_height = 5
plot_output = 'plot_output.png'
# 200Hz sample rate (1/200) step size
step_size = 0.005
# 10 seconds
duration = 10.0
# number of data points
num_data_points = int(np.ceil(duration / step_size))

# initialize arrays
timevec = np.zeros((num_data_points,))
position = np.zeros((num_data_points,))
# copy data points to array
for idx in range(num_data_points):
    timevec[idx] = float(idx) * step_size
    position[idx] = 100.0 * np.sin(timevec[idx] * 2.0 * np.pi / duration) + 10.0 * np.random.normal()

# save data using a dictionary (dict) data structure
data = {
    'step_size': step_size,
    'time': timevec,
    'position': position
}
with open(filepath, 'wb') as fp:
    np.savez(fp, **data)

# load data from file
data = np.load(filepath, allow_pickle=True)
timevec = data['time']
position = data['position']

# filter 5th-order butterworth lowpass 10Hz cutoff
order = 5
# cutoff frequency
fc = 10.0
# nyquist frequency
fn = (0.5 / step_size)
# normalized cutoff frequency
wn = fc / fn
sos =  signal.butter(order, wn, btype='low', output='sos')
position_filtered = signal.sosfilt(sos, position)

# plot position vs time
fig, ax = plt.subplots(1, 1)
ax.plot(timevec, position, label='meas')
ax.plot(timevec, position_filtered, label='fc=10Hz')
ax.set_title('Position vs Time')
ax.set_ylabel('Position (deg)')
ax.set_xlabel('Time (s)')
ax.legend()
ax.grid(True)
# resize figure
fig.set_size_inches(plot_width, plot_height)
fig.tight_layout()
# save
fig.savefig(plot_output, dpi=plot_dpi)
# show
plt.show()
