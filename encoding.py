import librosa


#import the audio file to be analyzed
audio, sr = librosa.load('lunar.wav', sr=None)

pitches, magnitude = librosa.piptrack(y=audio, sr=sr)
print(pitches)
print(magnitude)
print(sum(pitches))
print(sum(magnitude))
