'''
    Purpose: Manipulation of audio in phase domain
    Author: Mansoor Rahimat Khan
    Organization: Naffa Innovations Pvt Ltd
'''

import numpy as np
import librosa
audio, sr = librosa.load('./songs/lunar.wav')
print(audio)
chromagram = librosa.feature.chroma_stft(y=audio, sr=sr)
print(audio.shape)
print(chromagram.shape)
