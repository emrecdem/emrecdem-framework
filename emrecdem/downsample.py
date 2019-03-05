import datetime as dt
import pandas as pd
import numpy as np

def downsample(time_series,res = '0.2S'):
    # downsamples time_series pandas data frame
    # time_series: a pandas data.frame for which there is a column 'timestamps' with numeric timestamps
    # res: desired resolution in time after downsampling
    Nvalues = len(time_series.index)
    samplerate = 1/ ((time_series.timestamp[Nvalues-1] - time_series.timestamp[0]) / Nvalues)
    timestart = dt.datetime(1970, 1, 1, 0, 0, 0, 0) #dt.datetime.now()
    start = pd.Timestamp(timestart)
    end = pd.Timestamp(timestart + dt.timedelta(seconds=Nvalues/samplerate))
    t = np.linspace(start.value, end.value, Nvalues)
    t = pd.to_datetime(t)
    time_series['time'] = t
    time_series = time_series.resample(res,on='time').mean() # downsample to 0.2 second intervals
    time_series.index.name = 'time'
    time_series.reset_index(inplace=True)
    return time_series
