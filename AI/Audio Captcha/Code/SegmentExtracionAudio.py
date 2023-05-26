import librosa
import soundfile as sf
import numpy as np


# Load the audio file
audio_file_path = 'AudioCaptchas/00249.wav'
audio_samples, sample_rate = librosa.load(audio_file_path, sr=None)

# Set the amplitude threshold
amplitude_threshold = 0.35  # Adjust this value as needed

# Initialize variables
segments = []
start_time = None

# Iterate through the audio samples and detect segments
for i, sample in enumerate(audio_samples):
    time = i / sample_rate
    if sample > amplitude_threshold and start_time is None:
        start_time = time - 0.03
    elif sample <= amplitude_threshold and start_time is not None:
        sample_threshold = np.where(audio_samples[i:i+5])
        if np.any(sample_threshold):
            continue
        else:
            segments.append((start_time, time + 0.03))
            start_time = None

print(len(segments))

# Extract the segments and concatenate them into a single audio array
extracted_audio = np.concatenate([audio_samples[int(start * sample_rate):int(end * sample_rate)] for start, end in segments])

# Calculate the duration of the extracted audio in seconds
extracted_duration = len(extracted_audio) / sample_rate

# Save the extracted audio as a single file
output_file_path = 'output_audio.wav'
sf.write(output_file_path, extracted_audio, sample_rate)
print(f'Total duration: {extracted_duration:.2f} seconds')

print(f'Saved extracted audio to: {output_file_path}')

print(f'sample_rate: {sample_rate}')
