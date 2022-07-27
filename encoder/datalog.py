import numpy as np
from encoder.configuration import EncoderReadConfiguration
from encoder.plot import plot_encoder_data, plot_timing, plt


class PositionDataLog():
    def __init__(self, config: EncoderReadConfiguration = None, max_size: int = None):

        self.step_size: float = 0.0
        self.max_size: int = 0
        self.time: np.ndarray = np.array([])
        self.position: np.ndarray = np.array([])
        self.index: int = 0

        if config is not None:
            self.step_size = config.STEP_SIZE
            self.max_size = int(np.ceil(config.DURATION / config.STEP_SIZE))
            if max_size is not None:
                self.max_size = max_size
            self.time: np.ndarray = np.zeros((self.max_size,))
            self.position: np.ndarray = np.zeros((self.max_size,))

    def add_point(self, time: float, position: float):

        if self.index < self.max_size:
            self.time[self.index] = time
            self.position[self.index] = position
            self.index += 1

    def save_to_file(self, filepath: str):

        with open(filepath, 'wb') as fp:
            data = {
                'step_size': self.step_size,
                'time': self.time[:self.index],
                'position': self.position[:self.index]
            }
            np.savez(fp, **data)

    def load_from_file(self, filepath: str):
        # load dictionary
        data = np.load(filepath, allow_pickle=True)
        # save to object
        self.step_size = float(data['step_size'])
        if self.max_size < data['time'].size:
            # adjust new max size
            self.max_size = data['time'].size
            # copy data
            self.index = data['time'].size
            self.time = data['time']
            self.position = data['position']
        else:
            # keep max size, copy data
            self.index = data['time'].size
            self.time[:self.index] = data['time']
            self.position[:self.index] = data['position']

    def plot(self, output_prefix: str, user: str = None, show: bool = False):
        enc_plot_output = output_prefix + '_position.png'
        timing_plot_output = output_prefix + '_timing.png'
        print('Writing plots ...\n  {}\n  {}'.format(enc_plot_output, timing_plot_output))
        plot_encoder_data(self.time[:self.index], self.position[:self.index], output=enc_plot_output, username=user)
        plot_timing(self.time[:self.index], self.step_size, output=timing_plot_output, username=user)
        if show:
            plt.show()
        print('Done')
