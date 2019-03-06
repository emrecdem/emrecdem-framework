# Copyright 2019 Netherlands eScience Center
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import subprocess

def findwav(OpenFace_filename, datadirectory):
    """
    Recursively find .wav audio file in a folder that matches a given .csv
    OpenFace output filename. Here, we assume that the audio filename equals
    the OpenFace output filename minus the strings '_Cfront', '_Cside'
    and/or '_C1'. Further, with .csv replaced by .wav.

    Parameters
    ----------
    OpenFace_filename : str
        Name of the OpenFace file for which a matchin .wav audio file needs to
        be foundself.
    datadirectory: str
        Path to directory in which the .wav file is expected to be found.

    Returns
    -------
    audio_filename : str
        Name of the matching audiofile
    """

    expected_filename = OpenFace_filename.replace('.csv','.wav').replace('_Cfront','').replace('_Cside','').replace('_C1','')

    # Find file (inspired by code snippets as available on various forums)
    findCMD = 'find ' + datadirectory + ' -name ' + expected_filename
    out = subprocess.Popen(findCMD,shell=True,stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    (stdout, stderr) = out.communicate()     # Get standard out and error
    filelist = stdout.decode().split() # Save found files to list
    # probably the list has only one filename, but select first in case there
    # are two copies of the file
    audio_filename = filelist[0]

    if (os.path.isfile(audio_filename) ==  True):
        print("Mathing audio file identified")
    else:
        print("Warning: Matching audio file not identified")
    return(audio_filename)
