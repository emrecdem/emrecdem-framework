import datetime as dt
import pandas as pd
import numpy as np

def OpenFace(openface_features, PID, EXP):
    """
    Tidy up OpenFace features in pandas data.frame to be stored in sqlite
    database:
    - Participant and experiment identifiers are added as columns
    - Underscores in column names are removed, because sqlite does not like
        underscores in column names.
    - Only column names with 'AU' in the column name are considered relevant
      features and kept, the rest is removed.

    Parameters
    ----------
    video_features : pandas.core.frame.DataFrame
        Data frame with columns participant_id (str), experiment_id (str),
        timestamp (datetime64), and columns for the OpenFace derived
        video features:
        AU01r (float64), AU02r (float64), AU01c (float64), AU02c (float64)
    PID : str
        Participant identifier
    EXP : str
        Experiment identifier.

    Returns
    -------
    video_features : pandas.core.frame.DataFrame
        New data frame

    """

    # tidy up data frame:
    filter_col = [col for col in openface_features if col.startswith('AU')]
    filter_col.insert(0,'time')
    filter_col.insert(0,'participant_id')
    filter_col.insert(0,'experiment_id')
    openface_features['participant_id'] = PID
    openface_features['experiment_id'] = EXP
    openface_features = openface_features[filter_col]
    openface_features.columns = openface_features.columns.str.replace('_', '')
    openface_features = openface_features.rename(columns = {'experimentid':'experiment_id'})
    openface_features = openface_features.rename(columns = {'participantid':'participant_id'})
    return openface_features

def Librosa(librosa_features, PID, EXP):
    """
    Tidy up Librosa features in pandas data.frame to be stored in sqlite
    database:
    - Participant and experiment identifiers are added as columns
    - Underscores in column names are removed, because sqlite does not like
        underscores in column names.
    - Column zrc is renamed as zcrate
    - Only column names 'participant_id','experiment_id','time','pitch',
      'rmse', 'zcrate are kept.

    Parameters
    ----------
    audio_features : pandas.core.frame.DataFrame
        Data frame with columns participant_id (str), experiment_id (str),
        timestamp (datetime64),  and columns for the librosa derived
        audio features:
        pitch (float64), rmse (float32), zcrate (float64)
    PID : str
        Participant identifier
    EXP : str
        Experiment identifier.

    Returns
    -------
    audio_features : pandas.core.frame.DataFrame
        New data frame.

    """
    librosa_features['participant_id'] = PID
    librosa_features['experiment_id'] = EXP
    librosa_features = librosa_features.rename(columns={'zrc': 'zcrate'})
    librosa_features.drop(['timestamp'], axis = 1, inplace = True, errors = 'ignore')
    librosa_features = librosa_features[['participant_id','experiment_id','time','pitch','rmse','zcrate']]
    return librosa_features

def downsample(time_series,res = '0.2S'):
    """
    Downsamples time_series pandas data frame

    Parameters
    ----------
    time_series: pandas.core.frame.DataFrame
        A pandas data.frame for which there is a column 'timestamps'
        with numeric timestamps.

    res: str
        Desired resolution in time after downsampling used by 'resample'
        function.

    Returns
    -------
    time_series: pandas.core.frame.DataFrame
        New resampled data frame.
    """

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
