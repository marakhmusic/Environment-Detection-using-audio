import pyaudio
import wave
import librosa
import madmom
import IPython.display as ipd
import numpy as np
from tkinter import *
import tkinter as tk
import tkinter.font

from pydub import AudioSegment
import ffmpy


def record_sound():
    FORMAT = pyaudio.paInt16    #16 bit encoding
    CHANNELS = 2        #stereo
    RATE = 44100        #sampling rate
    CHUNK = 1024        #chunks of samples for purpose of processing
    RECORD_SECONDS = 10  #length of audio to be recorded
    WAVE_OUTPUT_FILENAME = "mansoor3.wav"

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
    # approach 2 - dbn tracker
    proc = madmom.features.beats.DBNBeatTrackingProcessor(fps=100)
    act = madmom.features.beats.RNNBeatProcessor()(audio_file)
    custom_click, sr1 = librosa.load('vibration2.wav',sr=None)
    beat_times = proc(act)
    print(len(x))
    clicks = librosa.clicks(beat_times, sr=sr, length=len(x),click=custom_click )
    ipd.Audio(x + clicks, rate=sr)
    print(clicks)
    # sound(clicks)
    librosa.output.write_wav('tone.wav', x+clicks, sr)
    librosa.output.write_wav('clicks.wav',clicks, sr)
    tempo, beats = librosa.beat.beat_track(y=clicks, sr=sr)
    print(tempo)
    return tempo

def assign_binaries(tempo_array,tempo):
    binary_array = []
    #assign_number = []
    for calc in tempo_array:
        if tempo-30 <= calc <= tempo+30:
            assign_number = 1
        elif tempo*2-30 <= calc <= tempo*2+30:
            assign_number = 0
        else:
            assign_number = 1
        binary_array.append(assign_number)
    print(binary_array)
    arr = []
    count = 0
    temp = 0
    for bin in binary_array:
        if bin==1:
            count+=1
            if count==2:
                temp = 1
                arr.append(temp)
                count=0
        elif bin==0:
            count+=1
            if count==1:
                temp=0
                count=0
                arr.append(temp)

    print("The decoded output is ", arr)
    return arr

def in_decoded_audio(audio):
    audio, sr = librosa.load(audio,sr=None)
    start = 0
    end = 2*sr
    print(sr)
    duration = round(len(audio)/sr)

    tempo_array = []
    #audio_samples = np.pad(audio, (0, (sr*duration - len(audio))), 'constant')
    audio_samples = np.pad(audio, (0, abs((sr * duration - len(audio)))), 'constant', constant_values=0)
    print(len(audio))
    print(len(audio_samples))
    print(duration)
    print(round(duration/2))
    for i in range(round(duration/2)):
        temp_audio = audio_samples[start:end]
        print(len(temp_audio))
        temp_tempo, beats = librosa.beat.beat_track(y=temp_audio,sr=sr)
        tempo_array.append(temp_tempo)
        if end == len(audio_samples):
            break
        start += 2*sr
        end += 2*sr

    return tempo_array

if __name__ == '__main__':
    root = Tk()
    photo = PhotoImage(file="condenser.png")
    helv36 = tkinter.font.Font(family='Helvetica', size=36, weight=tkinter.font.BOLD)
    label_1 = Label(root, text="Enter the recording duration", font=helv36, image=photo)
    #nos = Entry(root)
    tk_button = Button(root, text="Start Recording now", font=helv36, fg="red", bg="black",
                       command=record_sound)
    label_1.grid(row=0)
    tk_button.grid(row=1)
    root.mainloop()
    #record_sound()
    tempo = find_bpm('/Users/mansoorkhan/ToneTag_Experiments/Python Projects/Environment_detection/Friday_Demo/demo.wav')
    print(tempo)
    tempo_array = in_decoded_audio('mansoor3.wav')
    #tempo_array = in_decoded_audio('tone3.wav')
    print(tempo_array)
    arr = assign_binaries(tempo_array,tempo)
    root = Tk()
    helv36 = tkinter.font.Font(family='Helvetica', size=288, weight=tkinter.font.BOLD)
    label_2 = Label(root, text=arr, font=helv36)
    label_2.pack()
    root.mainloop()