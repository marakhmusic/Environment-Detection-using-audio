'''
    Purpose: Manipulation of audio in phase domain
    Author: Mansoor Rahimat Khan
    Organization: Naffa Innovations Pvt Ltd
'''


from scipy.fftpack import fft, ifft
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from scipy.io import wavfile
import numpy as np

#using scipy to read the audio wavefile
# sr, audio_data = wavfile.read('sineandsong.wav')
# sr, audio_data = wavfile.read('puresine_587point33hz.wav')
# sr, audio_data = wavfile.read('mergedfilenew.wav')
sr, audio_data = wavfile.read('mergedfile1.wav')
# sr, audio_data = wavfile.read('mergedfile2.wav')
# sr, audio_data = wavfile.read('mergedfile.wav')
#sr, audio_data = wavfile.read('recording.wav')

#converting stereo file into mono
if len(audio_data.shape)>1:
    audio_data = audio_data.sum(axis=1)/2

#calculate the fft of the audio file to get frequency information
audio_data_fft = fft(audio_data)

# Number of samplepoints
N = len(audio_data_fft)
print(N//2)
plt.plot(np.abs(audio_data_fft[0:N//2]))
plt.show()

print(sr)
print(audio_data.shape)
print(audio_data_fft)
