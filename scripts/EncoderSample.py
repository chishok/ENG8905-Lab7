from Encoder.encoder import Encoder
import time

# Step size to print feedback in timed loop
step_size = 0.1
# Duration of timed loop
timeout = 10.0

# encoder pins
pin_a = 6
pin_b = 13

# create encoder
enc = Encoder(6, 13)

# initialize loop
stop_loop = False
time_start = time.monotonic()
time_target = 0
time_elapsed = 0
while not stop_loop:
    # update elapsed time
    time_elapsed = time.monotonic() - time_start
    if time_elapsed >= time_target:
        # print out reading
        print('Count: {:}'.format(enc.read()))
        time_target += step_size
    if time_elapsed >= timeout:
        # pend loop
        stop_loop = True
print('Done')
