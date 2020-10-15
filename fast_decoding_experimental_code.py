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
import time

from sys import byteorder
from array import array
from struct import pack

def record_sound():
    THRESHOLD = 11000
    FORMAT = pyaudio.paInt16    #16 bit encoding
    RATE = 44100        #sampling rate
    CHUNK = 2048        #chunks of samples for purpose of processing

    def is_silent(snd_data):
        "Returns 'True' if below the 'silent' threshold"
        return max(snd_data) < THRESHOLD


    def normalize(snd_data):
        "Average the volume out"
        MAXIMUM = 16384
        times = float(MAXIMUM)/max(abs(i) for i in snd_data)

        r = array('h')
        for i in snd_data:
            r.append(int(i*times))
        return r

    def trim(snd_data):
        "Trim the blank spots at the start and end"
        def _trim(snd_data):
            snd_started = False
            r = array('h')

            for i in snd_data:
                if not snd_started and abs(i)>THRESHOLD:
                    snd_started = True
                    r.append(i)

                elif snd_started:
                    r.append(i)
            return r

        # Trim to the left
        snd_data = _trim(snd_data)

        # Trim to the right
        snd_data.reverse()
        snd_data = _trim(snd_data)
        snd_data.reverse()
        return snd_data

    def add_silence(snd_data, seconds):
        "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
        r = array('h', [0 for i in range(int(seconds*RATE))])
        r.extend(snd_data)
        r.extend([0 for i in range(int(seconds*RATE))])
        return r

    def record():
        """
        Record a word or words from the microphone and
        return the data as an array of signed shorts.

        Normalizes the audio, trims silence from the
        start and end, and pads with 0.5 seconds of
        blank sound to make sure VLC et al can play
        it without getting chopped off.
        """
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT, channels=1, rate=RATE,
            input=True, output=True,
            frames_per_buffer=CHUNK)

        num_silent = 0
        snd_started = False

        r = array('h')

        while 1:
            # little endian, signed short
            snd_data = array('h', stream.read(CHUNK))
            if byteorder == 'big':
                snd_data.byteswap()
            r.extend(snd_data)

            silent = is_silent(snd_data)

            if silent and snd_started:
                num_silent += 1
            elif not silent and not snd_started:
                snd_started = True

            if snd_started and num_silent > 30:
                break

        sample_width = p.get_sample_size(FORMAT)
        stream.stop_stream()
        stream.close()
        p.terminate()

        r = normalize(r)
        r = trim(r)
        r = add_silence(r, 0)
        return sample_width, r
    def record_to_file(path):
        "Records from the microphone and outputs the resulting data to 'path'"
        sample_width, data = record()
        data = pack('<' + ('h'*len(data)), *data)

        wf = wave.open(path, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(sample_width)
        wf.setframerate(RATE)
        wf.writeframes(data)
        wf.close()

    print("please speak a word into the microphone")
    record_to_file('fast_mansoor3.wav')
    print("done - result written to fast_mansoor3.wav")#/Users/mansoorkhan/ToneTag_Experiments/Python Projects/Environment_detection

def find_bpm(audio_file):
    x, sr = librosa.load(audio_file,sr=None)
    # approach 2 - dbn tracker
    proc = madmom.features.beats.DBNBeatTrackingProcessor(fps=100)
    act = madmom.features.beats.RNNBeatProcessor()(audio_file)
    custom_click, sr1 = librosa.load('vibration2_works.wav',sr=None)
    beat_times = proc(act)
    print(len(x))
    clicks = librosa.clicks(beat_times, sr=sr, length=len(x),click=custom_click)
    #clicks = librosa.clicks(beat_times, sr=sr, length=len(x))
    ipd.Audio(x + clicks, rate=sr)
    print(clicks)
    # sound(clicks)
    tempo = librosa.beat.tempo(y=clicks, sr=sr, max_tempo=180)
    print("The tempo is", tempo)
    return tempo

def assign_binaries(tempo_array,tempo):
    binary_array = []
    assign_number = []
    for calc in tempo_array:
        if calc == tempo:
            assign_number = 1
        else:
            assign_number = 0
        binary_array.append(assign_number)
    print("The decoded sequence is",binary_array)
    """
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
    """
    return binary_array

def in_decoded_audio(audio):
    audio, sr = librosa.load(audio,sr=None)
    start = 0
    end = sr*0.1
    print(sr)
    duration = round(len(audio)/(sr*0.1))
    stop = duration * sr * 0.1
    print("oyr",duration)
    tempo_array = []
    #audio_samples = np.pad(audio, (0, (sr*duration - len(audio))), 'constant')
    #audio_samples = np.pad(audio, (0, abs((sr * duration - len(audio)))), 'constant', constant_values=0)
    print(len(audio))
    #print(len(audio_samples))
    print(duration)
    print(round(duration))
    while end != stop + (sr * 0.1):
        temp_audio = audio[int(start):int(end)]
        print(len(temp_audio))
        #temp_tempo, beats = librosa.beat.beat_track(y=temp_audio,sr=sr)
        temp_tempo = librosa.beat.tempo(y=temp_audio, sr=sr, max_tempo=180)
        tempo_array.append(temp_tempo)
        start += sr*0.1
        end += sr*0.1
        print(end)

    return tempo_array

if __name__ == '__main__':
    start = time.time()
    """
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
    """
    record_sound()
    tempo = find_bpm('/Users/mansoorkhan/ToneTag_Experiments/Python Projects/Environment_detection/Friday_Demo/fast_mansoor4.wav')
    print(tempo)
    tempo_array = in_decoded_audio('fast_mansoor3.wav')
    #tempo_array = in_decoded_audio('fast_tone3.wav')
    print(tempo_array)
    arr = assign_binaries(tempo_array,tempo)

    root = Tk()
    helv36 = tkinter.font.Font(family='Helvetica', size=144, weight=tkinter.font.BOLD)
    label_2 = Label(root, text=arr, font=helv36)
    label_2.pack()
    root.mainloop()

    end = time.time()
    print("Total time taken to decode",end-start)
