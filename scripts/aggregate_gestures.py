import pandas as pd
import numpy as np
import re

"""
Aggregates gesture annotations by topic from an Elan-exported TSV file. Topics and gestures
should be available as annotations. Gestures that occur between the start and end time of
each topic are counted by value. I.e. for every gesture value, an output column is created
with the count of that value within a topic.
"""

input_path = "/Users/peter/repos/esc/data/Deniece/P18_S2_LSB_HM1_DSN_v2.tsv"
output_path = "/Users/peter/repos/esc/data/Deniece/P18_S2_LSB_HM1_DSN_v2_output.tsv"

# Column names to match
BEGIN_TIME = 'Begin Time - ss.msec'
END_TIME = 'End Time - ss.msec'
GESTURES_COLUMN_STRING = 'gestures'

# Read csv
df = pd.read_csv(input_path, sep='\t')

# Fix weird number format (1.101.761 => 1101.761) and convert to float
df[BEGIN_TIME] = df[BEGIN_TIME].map(lambda s: float(re.sub(r'\.(?=.*?\.)', '', s)))
df[END_TIME] = df[END_TIME].map(lambda s: float(re.sub(r'\.(?=.*?\.)', '', s)))

# Extract rows containing topic
topics_filter = ~pd.isnull(df['Topic'])
topics = df[topics_filter]

# Aggregates columns corresponding to the topic
def process_topic(topic):
    # Filter by begin and end time
    fragment_filter = (df[BEGIN_TIME] >= topic[BEGIN_TIME]) & (df[END_TIME] < topic[END_TIME])
    fragment = df[fragment_filter]
    
    # Aggregate columns containing 'gestures'
    gesture_columns = list(filter(lambda c: GESTURES_COLUMN_STRING in c.lower(), fragment.columns))
    for column in gesture_columns:
        for value in [1, 2]:
            gestures_filter = fragment[column] == value
            count = gestures_filter.sum()
            topic[column + '_' + str(value)] = count
    
    return topic

# For each topic, aggregate the gesture columns
processed_series = []
for index, topic in topics.iterrows():
    processed_topic = process_topic(topic)
    processed_series.append(processed_topic)

# Create a DataFrame from the array of processed Series
cols = processed_series[0].to_dict().keys()
output = pd.DataFrame(processed_series, columns=cols)

# Write to csv
output.to_csv(output_path, sep='\t')
