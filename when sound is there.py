from pydub import AudioSegment,silence
import subprocess

INPUT_FILE="3.mp4"
SAMPLE_RATE=44100
command = "ffmpeg -i "+INPUT_FILE+" -ab 160k -ac 2 -ar "+str(SAMPLE_RATE)+" -vn "+"audio.wav"
print(command)
subprocess.call(command, shell=True)

myaudio = intro = AudioSegment.from_wav("audio.wav")
silence = silence.detect_silence(myaudio, min_silence_len=1000, silence_thresh=-32)

silence = [[(start/1000),(stop/1000)] for start,stop in silence] #convert to sec\
file='myfile.txt'
file1 = open(file,"w")
for i in range(0,len(silence)):
    file1.write('file '+INPUT_FILE+'\n')
    file1.write('inpoint '+str(silence[i][0])+'\n')
    file1.write('outpoint '+str(silence[i][1])+'\n')
file1.close()


command = "ffmpeg -f concat -i "+file+" combined.mp4"
print(command)
subprocess.call(command, shell=True)

command = command = "ffmpeg -f concat -i "+file+" background.mp4 -filter_complex [0:v]scale=400:400[v1];[1:v][v1]overlay=0:0:shortest=1 -shortest -preset superfast output.mp4"
print(command)
subprocess.call(command, shell=True)
