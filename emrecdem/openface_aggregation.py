# Copyright 2019 Netherlands eScience Center
# Licensed under the Apache License, version 2.0. See LICENSE for details.

import codecs
import re
import datetime as dt
import pandas as pd
import numpy as np


def extract_fragment(time_series, start_time, end_time):
    """
    Extracts the frames within the specified time interval
    """
    filter_timerange = (time_series['timestamp'] >= start_time) & (time_series['timestamp'] < end_time)
    fragment = time_series[filter_timerange]
    fragment.reset_index(drop=True, inplace=True)
    return fragment


selected_columns = ["AU01_r", "AU01_c", "AU04_r", "AU04_c", "AU09_r", "AU09_c", "AU10_r", "AU10_c", "AU12_r", "AU12_c", "AU14_r", "AU14_c"]

def get_selected_columns(time_series):
    return [col for col in time_series if col in selected_columns]

def readable_column_name(x, suffix):
    return f'{x[0:4]}_pres_{suffix}' if x.endswith('c') else f'{x[0:4]}_int_{suffix}'

def aggregate_frames(time_series):
    columns = get_selected_columns(time_series)

    selected_features = time_series[columns]
    agg_mean = selected_features.aggregate(['mean'])
    agg_mean.rename(columns=lambda x: readable_column_name(x, 'mean'), inplace=True)
    
    agg_runs = aggregate_feature_runs(time_series, columns)
    #pd.concat([aggregated_features, aggregated_row], ignore_index=True)
    
    return agg_runs


def aggregate_feature_runs(time_series, columns):
    start_time = time_series['timestamp'][time_series.index[0]]
    end_time = time_series['timestamp'][time_series.index[-1]]
    fragment_duration = end_time - start_time
    
    data = {}
    for column_name in columns:
        threshold_value = 0.5 if column_name.endswith('c') else 2.5
        threshold_framecount = 50 # TODO: this assumes frame rate is 50 fps, which would make 1 second
        runs = extract_runs_for_feature(time_series, column_name, threshold_value, threshold_framecount)
        # print(column_name, len(runs))
        
        # duration
        duration = 0
        for run in runs:
            start_time = time_series.loc[run[0], 'timestamp']
            end_time = time_series.loc[run[1], 'timestamp']
            duration += end_time - start_time
        data[readable_column_name(column_name, 'dur')] = duration
        data[readable_column_name(column_name, 'dur_pmin')] = duration * 60 / fragment_duration

        # frequency
        frequency = len(runs)
        data[readable_column_name(column_name, 'freq')] = frequency
        data[readable_column_name(column_name, 'freq_pmin')] = frequency * 60 / fragment_duration
    
    return pd.DataFrame(data, index=[0])
    

def extract_runs_for_feature(df, feature, threshold_value, threshold_framecount):
    threshold_filter = df[feature] > threshold_value
    first_rows = df.index[threshold_filter & ~ threshold_filter.shift(1).fillna(False)]
    last_rows = df.index[threshold_filter & ~ threshold_filter.shift(-1).fillna(False)]
    runs = [(i, j) for i, j in zip(first_rows, last_rows) if j > i + threshold_framecount]
    return runs
