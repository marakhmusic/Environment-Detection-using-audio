import pyaudio
import wave
import librosa
import madmom
import IPython.display as ipd
import numpy as np

from pydub import AudioSegment
import ffmpy


def record_sound():
    FORMAT = pyaudio.paInt16    #16 bit encoding
    CHANNELS = 2        #stereo
    RATE = 44100        #sampling rate
    CHUNK = 1024        #chunks of samples for purpose of processing
    RECORD_SECONDS = 4  #length of audio to be recorded
    WAVE_OUTPUT_FILENAME = "mansoor2.wav"

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
"""
def assign_binaries(tempo):
    bit_coding = "10111"
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
    bit_coding = "1000"
    ff = ffmpy.FFmpeg(inputs={"clicks.wav": None}, outputs={"final_tone.wav": ["-y","-filter:a", "atempo=2"]})
    ff.run()
    a, sr = librosa.load('final_tone.wav', sr=None)
    b, sr = librosa.load('clicks.wav',sr=None)
    print(type(a))
    print(a.shape)
    #sound1 = AudioSegment.from_wav('tone.wav')
    #sound2 = AudioSegment.from_wav('clicks.wav')
    combined_sounds = np.array([])
    for i in bit_coding:
        if int(i)==0:
            sound = a
            print(sound)
        elif int(i)==1:
            sound = b
        combined_sounds = np.append(combined_sounds,sound)
        print(type(combined_sounds))
    print(combined_sounds.size)
    print(combined_sounds)
    #final_sound = np.asarray(combined_sounds)
    librosa.output.write_wav('tone3.wav', combined_sounds, sr)

    #combined_sounds.export("tone3.wav", format="wav")

if __name__ == '__main__':
    record_sound()
    find_bpm('/Users/mansoorkhan/ToneTag_Experiments/Python Projects/Environment_detection/Friday_Demo/demo.wav')
    out_encoded_audio()