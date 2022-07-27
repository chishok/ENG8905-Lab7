import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import time

# global plot style
mpl.rcParams['lines.linewidth'] = 0.8


def get_timestamp():
    """Get formatted time string

    Returns:
        str: Formatted time string
    """
    return time.strftime('%Y-%m-%d_%Hh%Mm%Ss', time.gmtime(time.time()))


def plot_timing(time_seconds: np.ndarray, step_size_sec: float,
                output: str = None, username: str = None, width=7, height=7, dpi=200):

    timevec = (time_seconds * 1e6).astype(int)
    step_size = int(step_size_sec * 1e6)
    jitter = timevec[1:] - timevec[:-1]

    min_jitter = np.min(jitter) - step_size
    max_jitter = np.max(jitter) - step_size
    stdev_jitter = np.std(jitter)
    mean_jitter = np.average(jitter)

    num_points = timevec.size
    duration = num_points * step_size
    abstime_desired = np.linspace(step_size, duration, num=num_points)
    abstime_actual = timevec
    abstime_error = abstime_actual - abstime_desired

    # plot
    fig, axs = plt.subplots(2, 1)
    ax0 = axs[0]
    ax1 = axs[1]

    ax0.plot(time_seconds[1:], jitter)
    ax0.set_title('Jitter')
    ax0.set_ylabel('Jitter (us)')
    ax0.set_xlabel('Time (s)')
    ax0.grid(True)

    ax1.plot(time_seconds, abstime_error)
    ax1.set_title('Absolute Error (Latency)')
    ax1.set_ylabel('Latency (us)')
    ax1.set_xlabel('Time (s)')
    ax1.grid(True)

    # show timestamp
    topstr = get_timestamp()
    ax0.text(0.5, 0.97, topstr, transform=ax0.transAxes, fontsize=8,
             verticalalignment='top', horizontalalignment='center')

    # info
    infostr = []
    infostr.extend(['Step size (us)', '{}'.format(step_size)])
    infostr.extend(['', 'Min (us)'])
    infostr.append('{} + {}'.format(min_jitter, step_size))
    infostr.extend(['', 'Max (us)'])
    infostr.append('{} + {}'.format(max_jitter, step_size))
    infostr.extend(['', 'Mean, Stdev (us)'])
    infostr.append('{:.2f}, {:.2f}'.format(mean_jitter, stdev_jitter))
    if username is not None:
        infostr.extend(['', 'User:', '{}'.format(username)])
    # place info text
    infostr = '\n'.join(infostr)
    ax0.text(1.03, 0.97, infostr, transform=ax0.transAxes, fontsize=8,
             verticalalignment='top')

    # resize figure
    fig.set_size_inches(width, height)
    fig.tight_layout()

    # save
    if output is not None:
        fig.savefig(output, bbox_inches='tight', dpi=dpi)


def plot_encoder_data(timevec: np.ndarray, position: np.ndarray,
                      output: str = None, username: str = None, width=7, height=4, dpi=200):
    # plot
    fig, ax = plt.subplots(1, 1)

    ax.plot(timevec, position)
    ax.set_title('Encoder Position vs Time')
    ax.set_ylabel('Position (deg)')
    ax.set_xlabel('Time (s)')
    ax.grid(True)

    # show timestamp
    topstr = get_timestamp()
    ax.text(0.5, 0.97, topstr, transform=ax.transAxes, fontsize=8,
            verticalalignment='top', horizontalalignment='center')

    # info
    if username is not None:
        infostr = ['User:', '{}'.format(username)]
        # place info text
        infostr = '\n'.join(infostr)
        ax.text(1.03, 0.97, infostr, transform=ax.transAxes, fontsize=8,
                verticalalignment='top')

    # resize figure
    fig.set_size_inches(width, height)
    fig.tight_layout()

    # save
    if output is not None:
        fig.savefig(output, bbox_inches='tight', dpi=dpi)
