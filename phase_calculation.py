import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display

y, sr = librosa.load('kaunsifretsoriginal44100.wav', sr=None)
D = librosa.stft(y)
k = D.copy()
#magnitude, phase = librosa.magphase(D)
print(D[:,4].shape)
rotation_vector = -1
print('1', D[:,4])
count = 1

for j in range(D[:,4].shape[0]-1):
    current_complex = D[:, 4][count]
    prev_complex = D[:, 4][count-1]

    amp_factor = np.abs(current_complex) / np.abs(prev_complex)
    D[count] = np.multiply(amp_factor * prev_complex, rotation_vector)
    count += 1

print('2', D[:,4])
print(D[:,4]-k[:,4])
y_hat = librosa.istft(D)
librosa.output.write_wav('kaunsifretsphaseshift.wav', y_hat, sr)



"""

for row in range(D.shape[0]):
    for column in range(D.shape[1]):
        print(D[row,column])
"""





#print(D.shape)
#print(magnitude.shape)
#print(phase.shape)
#radian_angle = np.angle(phase)
"""
librosa.display.specshow(D, y_axis='linear')
librosa.display.specshow(radian_angle, y_axis='linear')
radian_angle[4] = radian_angle[4] + 3.14
print(radian_angle[4])
librosa.display.specshow(radian_angle, y_axis='linear')
plt.plot(radian_angle)
plt.show()
"""
"""
for _ in Yxx[start:end]:
        for j in range(config.MIN_FREQ, len(Yxx[0]))[first::2]:
            current_complex =  Yxx[counter][j]
            prev_complex  =  Yxx[counter-1][j]

            amp_factor = np.abs(current_complex)/np.abs(prev_complex)
            Yxx[counter][j] = np.multiply(amp_factor*prev_complex, rotation_vector)

        encoded_places[value].append(counter)
        counter += 1
"""