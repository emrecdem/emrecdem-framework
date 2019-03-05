import os
import subprocess
def findwav(videofilename, emrecdemStudyDataFolder):
    audiofile_name1 = videofilename.replace('.csv','.wav').replace('_Cfront','').replace('_Cside','').replace('_C1','')
    print(audiofile_name1)
     # Set up find command
    findCMD = 'find ' + emrecdemStudyDataFolder + ' -name ' + audiofile_name1
    out = subprocess.Popen(findCMD,shell=True,stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    print(findCMD)
    # Get standard out and error
    (stdout, stderr) = out.communicate()
    # Save found files to list
    filelist = stdout.decode().split()
    print(filelist)
    audiofiles_fullPaths = filelist # probably the list has only one filename
    audio_file2 = audiofiles_fullPaths[0]

    if (os.path.isfile(audio_file2) ==  True):
        print("Audio file identified")
    else:
        print("Warning: Audio file NOT identified")
    return(audio_file2)
