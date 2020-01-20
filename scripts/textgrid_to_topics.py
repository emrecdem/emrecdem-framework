import codecs
import re

"""
Extracts the topics from a PRAAT TextGrid file and outputs the topic labels and start + end times
"""

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


def format_duration(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return '{:02d}:{:02d}:{:07.4f}'.format(int(hours), int(minutes), seconds)


path = "/Users/peter/repos/esc/data/Deniece/P1/getranscribeerd_P1_S2_LSB_HM1_Mparticipant_talkspurt.TextGrid"
fragments = get_fragments_from_textgrid(path)
for fragment in fragments:
    (start_time, end_time, topic) = fragment
    print(topic, format_duration(start_time), format_duration(end_time))
