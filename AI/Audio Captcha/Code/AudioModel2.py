import os
import librosa
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM

# Define the path to the audio data
audio_path = 'AudioCaptchas/'

# Define the number of classes
num_classes = 10

# Define the number of MFCCs to extract
num_mfcc = 13

# Define the maximum length of the audio samples
max_len = 128

# Define the function to load and extract MFCCs from an audio file
def load_audio(file_path):
    audio, _ = librosa.load(file_path)
    mfccs = librosa.feature.mfcc(y=audio, sr=44100, n_mfcc=num_mfcc)
    mfccs = np.pad(mfccs, ((0, 0), (0, max_len - len(mfccs[0]))), mode='constant')
    return mfccs

# Load the audio data and extract MFCCs for each file
X = []
y = []
for i, filename in enumerate(os.listdir(audio_path)):
    file_path = os.path.join(audio_path, filename)
    mfccs = load_audio(file_path)
    X.append(mfccs)
    y.append(i)

X = np.array(X)
y = to_categorical(np.array(y), num_classes=num_classes)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Define the LSTM model
model = Sequential()
model.add(LSTM(64, input_shape=(num_mfcc, max_len)))
model.add(Dense(num_classes, activation='softmax'))

# Compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))
