from encoder.datalog import PositionDataLog

datafile = 'dataLog.npz'

dl = PositionDataLog()
dl.load_from_file(datafile)

# (optional) Post-process and generate interactive plots from loaded data
# Loaded data:
#   dl.time
#   dl.position
# For example: filtering https://docs.scipy.org/doc/scipy/reference/signal.html#filtering

# plot result
output_prefix = 'result'
dl.plot(output_prefix=output_prefix)
