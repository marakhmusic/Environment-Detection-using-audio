import pyaudio
import wave
import librosa
import madmom
import IPython.display as ipd
import numpy as np
import time
from pydub import AudioSegment
from ffmpy import FFmpeg
import time
from subprocess import PIPE, Popen, run


def find_bpm(audio_file):
    """Finds the bpm of the recorded audio file"""
    x, sr = librosa.load(audio_file,sr=None)
    x = np.pad(x, (0, abs((int(sr/10) - len(x)))), 'constant', constant_values=0)
    # approach 2 - dbn tracker
    proc = madmom.features.beats.DBNBeatTrackingProcessor(fps=100)
    act = madmom.features.beats.RNNBeatProcessor()(audio_file)
    custom_click, sr1 = librosa.load('vibration2_works.wav',sr=None)
    beat_times = proc(act)
    print("The length of x is", len(x))
    clicks = librosa.clicks(beat_times, sr=sr, length=len(x),click=custom_click)
    #clicks = librosa.clicks(beat_times, sr=sr, length=len(x))
    ipd.Audio(x + clicks, rate=sr)
    print(clicks)
    # sound(clicks)
    #librosa.output.write_wav('fast_tone.wav', x+clicks, sr)
    librosa.output.write_wav('fast_clicks.wav',clicks, sr)
    #tempo = librosa.beat.tempo(y=clicks, sr=sr,start_bpm=120, max_tempo=150.0 )
    tempo = librosa.beat.tempo(y=clicks, sr=sr, max_tempo=180)
    print("The tempo is", tempo)
    return tempo


def out_encoded_audio(bit_coding):
    # file_path = str(bit_coding) + '.wav'
    #bit_coding = "0111111001"
    """
    ff = ffmpy.FFmpeg(inputs={"clicks.wav": None}, outputs={"final_tone.wav": ["-y","-filter:a", "atempo=4"]})
    ff.run()
    ff = ffmpy.FFmpeg(inputs={"clicks.wav": None}, outputs={"final_tone2.wav": ["-y","-filter:a", "atempo=2"]})
    ff.run()
    """
    a, sr = librosa.load('fast_clicks.wav', sr=None)
    #print("SRA",sr)
    #b, sr = librosa.load('final_tone2.wav',sr=None)
    #print("SRB",sr)
    #print(sr/4)
    #print(len(b))
    #print("Hey yar", len(a))
    #a = np.pad(a, (0, abs((int(sr/4) - len(a)))), 'constant', constant_values=0)
    #b = np.pad(b, (0, abs((int(sr/2) - len(b)))), 'constant', constant_values=0)
    b = a[0:int(sr/20)]

    #c = np.pad(b, (0, int(sr / 4)), 'constant', constant_values=0)
    d = np.append(b,b)
    #print("Hey",len(c))
    print("Hi",len(d))
    print(type(a))
    print(a.shape)
    #sound1 = AudioSegment.from_wav('t    one.wav')
    #sound2 = AudioSegment.from_wav('click
    # s.wav')
    combined_sounds = np.array([])
    head_sound, sr = librosa.load('header_tone.wav', sr=None)
    header_sound = head_sound[0:100]
    print(len(header_sound))
    combined_sounds = np.append(combined_sounds,header_sound)
    for i in bit_coding:
        if int(i)==0:
            sound = d
            print(sound)
        elif int(i)==1:
            sound = a
        combined_sounds = np.append(combined_sounds,sound)
        print("The combined sounds are")
        print(type(combined_sounds),combined_sounds.dtype)
    print(combined_sounds.size)
    print(combined_sounds)
    print("The maximum value of the encoded file is at ", np.argmax(combined_sounds))
    #final_sound = np.asarray(combined_sounds)
    # out_file=f'/Users/mansoorkhan/ToneTag_Experiments/Python Projects/Environment_detection/App_Development/Flask_App/static/music/{bit_coding}.wav'
    out_file=f'./static/music/{bit_coding}.wav'
    sample_format ='f64le'
    output=True
    cmd = ['ffmpeg',
            '-y',                   # override if the file already exists
            '-f', sample_format,          # input format s16le
            #{}"-acodec", "pcm_s16le", # raw pcm data s16 little endian input
            "-acodec", "pcm_"+ sample_format, # raw pcm data s16 little endian input
            '-i', '-',              # pipe input
            '-ac', '1',             # mono
            out_file]              # out file name
    if output:
        print(f'cmd: {cmd}')

    process = run(cmd, input=combined_sounds.tobytes(), stdout=PIPE, stderr=PIPE)
    if output:
        print(f'process return code: {process.returncode}')
        print(process.stdout)

    return {
        'success' : True,
        'file_path' : out_file
    }
    #librosa.output.write_wav('/Users/mansoorkhan/ToneTag_Experiments/Python Projects/Environment_detection/App_Development/Flask_App/static/music/encodedaudio.wav', combined_sounds, sr)
    #ff = FFmpeg(inputs={'/Users/mansoorkhan/ToneTag_Experiments/Python Projects/Environment_detection/App_Development/Flask_App/static/music/encodedaudio.wav': None},outputs={'/Users/mansoorkhan/ToneTag_Experiments/Python Projects/Environment_detection/App_Development/Flask_App/static/music/encodedaudio3.wav':["-y"]})
    #ff.run()
    #write('/Users/mansoorkhan/ToneTag_Experiments/Python Projects/Environment_detection/App_Development/Flask_App/static/music/test.wav', 44100, combined_sounds)
    #combined_sounds.export("tone3.wav", format="wav")
    #check_temp, sr = librosa.load('fast_tone3.wav', sr=None)
    #print("Max", np.max(check_temp))

if __name__ == '__main__':
    start = time.time()
    #record_sound()
    find_bpm('/Users/mansoorkhan/ToneTag_Experiments/Python Projects/Environment_detection/Friday_Demo/fast_mansoor4.wav')
    #out_encoded_audio(bit_coding)
    out_encoded_audio("1011011100") #debug
    end = time.time()
    print("Total time to encode", end-start)
