import time
from encoder.display import TextWithBorderDisplay
from encoder.quadrature import RotaryEncoder
from encoder.configuration import EncoderReadConfiguration
from encoder.datalog import PositionDataLog
import numpy as np


class ReadAndDisplayEncoder():
    def __init__(self, config: EncoderReadConfiguration):

        self.display: TextWithBorderDisplay = TextWithBorderDisplay(config)
        self.enc: RotaryEncoder = RotaryEncoder(config)
        self.datalog: PositionDataLog = PositionDataLog(config)

        self.step_size: float = config.STEP_SIZE
        self.display_step_size: float = config.DISPLAY_STEP_SIZE
        self.duration: float = config.DURATION
        self.output_prefix = config.DATA_LOG_PREFIX
        self.user = config.USER

        self.time: float = 0.0
        self.position: float = 0.0

    def run_timed_loop(self):

        # notify user
        print('Running for {} seconds ...'.format(self.duration))

        # Initialize loop
        stop_loop = False
        time_start = time.monotonic()
        capture_target = self.step_size
        display_target = 0
        time_elapsed = 0
        while not stop_loop:
            # Update elapsed time
            time_elapsed = time.monotonic() - time_start
            if time_elapsed >= capture_target:
                # set data point
                self.time = time_elapsed
                self.position = self.enc.read()
                # add to data logger
                self.datalog.add_point(self.time, self.position)
                # advance time
                capture_target += self.step_size
            if time_elapsed >= display_target:
                # display
                self.display.update('T: {:.1f}s A: {:.0f}'.format(self.time, self.position))
                # advance time
                display_target += self.display_step_size
            if time_elapsed >= self.duration:
                # End loop
                stop_loop = True
        self.display.update('Done')

        # notify user data file is being written
        datapath = self.output_prefix + '.npz'
        print('Saving data to "{}" ...'.format(datapath))
        self.datalog.save_to_file(datapath)
        print('Done')

    def plot(self):
        self.datalog.plot(self.output_prefix, user=self.user)
