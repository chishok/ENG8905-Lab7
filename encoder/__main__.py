from control import ReadAndDisplayEncoder
from configuration import EncoderReadConfiguration
import argparse

parser = argparse.ArgumentParser(
    prog='encoder',
    description='Quadrature encoder with display data collection and plot'
)
parser.add_argument('--step-size',
                    type=float,
                    help='Data collection step size (rate) in seconds',
                    default=None)
parser.add_argument('--duration',
                    type=float,
                    help='Duration of data collection in seconds',
                    default=None)
parser.add_argument('--output',
                    type=str,
                    help='Output data file path and plot images prefix',
                    default=None)
parser.add_argument('--custom-decoder',
                    help='Use custom decoder',
                    action='store_true')
parser.add_argument('--user',
                    type=str,
                    help='Username',
                    default=None)
args = parser.parse_args()

config = EncoderReadConfiguration()
if args.step_size is not None:
    config.STEP_SIZE = args.step_size
if args.duration is not None:
    config.DURATION = args.duration
if args.output is not None:
    config.DATA_LOG_PREFIX = args.output
if args.custom_decoder:
    config.ENC_CUSTOM_DECODER = True
if args.user is not None:
    config.USER = args.user

controller = ReadAndDisplayEncoder(config)
controller.run_timed_loop()
controller.plot()
