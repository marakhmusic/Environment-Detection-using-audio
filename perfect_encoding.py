import pyaudio
import wave
import librosa
import madmom
import IPython.display as ipd
import numpy as np
import time
from pydub import AudioSegment
import ffmpy
import time

def record_sound():
    FORMAT = pyaudio.paInt16    #16 bit encoding
    CHANNELS = 1        #mono
    RATE = 44100        #sampling rate
    CHUNK = 1024        #chunks of samples for purpose of processing
    RECORD_SECONDS = 0.1  #length of audio to be recorded
    WAVE_OUTPUT_FILENAME = "fast_mansoor45.wav"

    audio = pyaudio.PyAudio()

    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("recording...")
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("finished recording")
    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

#/Users/mansoorkhan/ToneTag_Experiments/Python Projects/Environment_detection

def find_bpm(audio_file):
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
    librosa.output.write_wav('fast_tone.wav', x+clicks, sr)
    librosa.output.write_wav('fast_clicks.wav',clicks, sr)
    #tempo = librosa.beat.tempo(y=clicks, sr=sr,start_bpm=120, max_tempo=150.0 )
    tempo = librosa.beat.tempo(y=clicks, sr=sr, max_tempo=180)
    print("The tempo is", tempo)
    return tempo
"""
def assign_binaries(tempo):
    bit_coding = "211101112"
    encoded_seq=[]
    for i in bit_coding:
        if int(i)==0:
            coded_seq = tempo*2
        elif int(i)==1:
            coded_seq=tempo
        encoded_seq.append(coded_seq)
    print(encoded_seq)
    return encoded_seq
"""

def out_encoded_audio():
    bit_coding = "0100111001"
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
    for i in bit_coding:
        if int(i)==0:
            sound = d
            print(sound)
        elif int(i)==1:
            sound = a
        combined_sounds = np.append(combined_sounds,sound)
        print(type(combined_sounds))
    print(combined_sounds.size)
    print(combined_sounds)
    #final_sound = np.asarray(combined_sounds)
    librosa.output.write_wav('fast_tone3.wav', combined_sounds, sr)

    #combined_sounds.export("tone3.wav", format="wav")

if __name__ == '__main__':
    start = time.time()
    record_sound()
    find_bpm('/Users/mansoorkhan/ToneTag_Experiments/Python Projects/Environment_detection/Friday_Demo/fast_mansoor4.wav')
    out_encoded_audio()
    end = time.time()
    print("Total time to encode", end-start)