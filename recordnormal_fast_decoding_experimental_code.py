#import pyaudio
#import wave
import librosa
import madmom
import IPython.display as ipd
import numpy as np
from tkinter import *
import tkinter as tk
import tkinter.font
import sounddevice as sd
#from pydub import AudioSegment
#import ffmpy
import time



def record_sound():
    print("Recording.....")
    fs = 44100
    duration = 4  # seconds
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    print("Recording Finished")
    print(type(myrecording))
    processing_audio = myrecording[4410:len(myrecording)]
    #processed_audio = np.pad(processing_audio,(0, abs((int(duration*fs) - len(processing_audio)))), 'constant', constant_values=0)
    #print("Finally", len(processed_audio))
    librosa.output.write_wav('temporary_output.wav', processing_audio, sr=fs)



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
    threshold = 0.5
    print(audio[257])
    for sample in range(len(audio)):
        if audio[sample]>=threshold:
            print("This is the sample", sample)
            new_audio = audio[sample+4410:sample+4410+44100]
            break
    librosa.output.write_wav('temporary_output_new.wav', new_audio, sr=44100)


    #print("Max Value is", np.max(audio))
    start = 0
    end = sr*0.1
    print(sr)
    duration = round(len(new_audio)/(sr*0.1))
    stop = duration * sr * 0.1
    print("oyr",duration)
    tempo_array = []
    #audio_samples = np.pad(audio, (0, (sr*duration - len(audio))), 'constant')
    #audio_samples = np.pad(audio, (0, abs((sr * duration - len(audio)))), 'constant', constant_values=0)
    print("The new lenght is",len(new_audio))
    #print(len(audio_samples))
    print(duration)
    print(round(duration))
    while end != stop + (sr * 0.1):
        temp_audio = new_audio[int(start):int(end)]
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
    #record_sound()
    tempo = find_bpm('/Users/mansoorkhan/ToneTag_Experiments/Python Projects/Environment_detection/Friday_Demo/fast_mansoor4.wav')
    print(tempo)
    #tempo_array = in_decoded_audio('fast_mansoor3.wav')
    tempo_array = in_decoded_audio('temporary_output_test4.wav')
    print(tempo_array)
    arr = assign_binaries(tempo_array,tempo)

    root = Tk()
    helv36 = tkinter.font.Font(family='Helvetica', size=144, weight=tkinter.font.BOLD)
    label_2 = Label(root, text=arr, font=helv36)
    label_2.pack()
    root.mainloop()

    end = time.time()
    print("Total time taken to decode",end-start)
