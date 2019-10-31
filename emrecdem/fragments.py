# Copyright 2019 Netherlands eScience Center
# Licensed under the Apache License, version 2.0. See LICENSE for details.

import codecs
import re
import datetime as dt
import pandas as pd
import numpy as np

def get_fragments_from_textgrid(filePath):
    """
    Extracts fragments from a PRAAT TextGrid file

    Parameters
    ----------
    filePath: the path of the TextGrid file

    Returns
    -------
    An array of tuples of the format (start_time, end_time, description)
    """

    # Read file
    content = ""
    with codecs.open(filePath, 'rb', encoding='utf-16') as file:
        content = file.read()

    # Match main fragment section (first 'item')
    r = re.compile(r"item \[1\](.*)item \[2\]", re.MULTILINE + re.S)
    match = r.search(content)
    fragment_section = match.groups()[0]

    # Match start / stop times and corresponding text
    r = re.compile(r"intervals \[.*?xmin = ([0-9.]*).*?xmax = ([0-9.]*).*?text = \"(.*?)\"", re.MULTILINE + re.S)
    match = r.findall(fragment_section)
    
    # Convert times to floats
    match = map(lambda t: (float(t[0]), float(t[1]), t[2]), match)

    # Filter out empty text
    filtered = list(filter(lambda x: x[2] != '', match))

    return filtered

def extract_fragments_openface(time_series, fragments, PID, EXP):
    """
    Extracts / aggregates features for the specified fragments within the time series data

    Parameters
    ----------
    time_series: pandas.core.frame.DataFrame
        A pandas data.frame for which there is a column 'timestamps'
        with numeric timestamps.
    fragments: an array of tuples of the format (start_time, end_time, description), where:
        start_time: the start_time of the data to include (float).
        end_time: the end_time of the data to include (float).
        description: label to add as extra column (string).
    PID: participant id to add as extra column.
    EXP: experiment id to add as extra column.

    Returns
    -------
    aggregated_features: pandas.core.frame.DataFrame
        Single-row DataFrame containing the aggregated values.
    """
    aggregated_features = pd.DataFrame()
    for fragment in fragments:
        (start_time, end_time, description) = fragment
        fragment_df = extract_fragment_features_openface(time_series, start_time, end_time, description, PID, EXP)
        aggregated_features = pd.concat([aggregated_features, fragment_df], ignore_index=True)
    return aggregated_features

def extract_fragment_features_openface(time_series, start_time, end_time, description, PID, EXP):
    """
    Extracts / aggregates features in a certain time period within the time series data

    Parameters
    ----------
    time_series: pandas.core.frame.DataFrame
        A pandas data.frame for which there is a column 'timestamps'
        with numeric timestamps.
    start_time: the start_time of the data to include.
    end_time: the end_time of the data to include.
    description: label to add as extra column.
    PID: participant id to add as extra column.
    EXP: experiment id to add as extra column.

    Returns
    -------
    agg_col: pandas.core.frame.DataFrame
        Single-row DataFrame containing the aggregated values.
    """
    filter_timerange = (time_series['timestamp'] >= start_time) & (time_series['timestamp'] < end_time)
    selected_features = time_series[filter_timerange]
    
    filter_col = [col for col in selected_features if col.startswith('AU')]
    selected_features = selected_features[filter_col]
    agg_col = selected_features.aggregate(['mean'])
    
    agg_col['participant_id'] = PID
    agg_col['experiment_id'] = EXP
    agg_col['start_time'] = start_time
    agg_col['end_time'] = end_time
    agg_col['description'] = description
    return agg_col

def extract_fragments_librosa(time_series, fragments, PID, EXP):
    """
    Extracts / aggregates features for the specified fragments within the time series data

    Parameters
    ----------
    time_series: pandas.core.frame.DataFrame
        A pandas data.frame for which there is a column 'timestamps'
        with numeric timestamps.
    fragments: an array of tuples of the format (start_time, end_time, description), where:
        start_time: the start_time of the data to include (float).
        end_time: the end_time of the data to include (float).
        description: label to add as extra column (string).
    PID: participant id to add as extra column.
    EXP: experiment id to add as extra column.

    Returns
    -------
    aggregated_features: pandas.core.frame.DataFrame
        Single-row DataFrame containing the aggregated values.
    """
    aggregated_features = pd.DataFrame()
    for fragment in fragments:
        (start_time, end_time, description) = fragment
        fragment_df = extract_fragment_features_librosa(time_series, start_time, end_time, description, PID, EXP)
        aggregated_features = pd.concat([aggregated_features, fragment_df], ignore_index=True)
    return aggregated_features

def extract_fragment_features_librosa(time_series, start_time, end_time, description, PID, EXP):
    """
    Extracts / aggregates features in a certain time period within the time series data

    Parameters
    ----------
    time_series: pandas.core.frame.DataFrame
        A pandas data.frame for which there is a column 'timestamps'
        with numeric timestamps.
    start_time: the start_time of the data to include.
    end_time: the end_time of the data to include.
    description: label to add as extra column.
    PID: participant id to add as extra column.
    EXP: experiment id to add as extra column.

    Returns
    -------
    agg_col: pandas.core.frame.DataFrame
        Single-row DataFrame containing the aggregated values.
    """
    filter_timerange = (time_series['timestamp'] >= start_time) & (time_series['timestamp'] < end_time)
    selected_features = time_series[filter_timerange]

    selected_features = selected_features.rename(columns={'zrc': 'zcrate'})
    selected_features = selected_features[['pitch','rmse','zcrate']]
    aggregated_features = selected_features.aggregate(['mean'])
    
    aggregated_features['participant_id'] = PID
    aggregated_features['experiment_id'] = EXP
    aggregated_features['start_time'] = start_time
    aggregated_features['end_time'] = end_time
    aggregated_features['description'] = description
    return aggregated_features
