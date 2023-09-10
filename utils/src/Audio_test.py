import sounddevice as sd
import numpy as np
from scipy.io import wavfile
from scipy.signal import decimate
import matplotlib.pyplot as plt

# Define the callback function
def audio_callback(indata, frames, time, status):
    audio_buffer.append(indata.copy())

# Initialize variables
sample_rate = 48000  # You can adjust this as needed
duration = 5  # Duration in seconds
audio_buffer = []

print('Recording...')
# Start recording using InputStream
audio_stream = sd.InputStream(callback=audio_callback, channels=1, samplerate=sample_rate, blocksize=24000)
audio_stream.start()                                                                   # Initialize audio acquisition
sd.sleep(int(duration * 1000))  # Sleep for the desired duration
audio_stream.stop()                                                                    # Stop the audio acquisition
audio_stream.close()                                                                   # Close audio communication

# Convert the audio buffer to a single numpy array
print([len(buffer) for buffer in audio_buffer])
audio_data = np.concatenate(audio_buffer, axis=0)
audio_data = decimate(audio_data[:,0], 3)

# Save the audio data to a WAV file
output_filename = "captured_audio.wav"
wavfile.write(output_filename, int(sample_rate/3), audio_data)

print(f"Audio saved to {output_filename}")

plt.figure()
plt.plot(audio_data)
plt.show()


#############################################

# import os
# import time
# from transformers import pipeline

# INPUT_PATH = os.path.join('..', 'data', 'audio_samples')
# MODELS_PATH = os.path.join('..', 'models')

# # Load the pipeline
# pipe = pipeline("audio-classification", model=os.path.join(MODELS_PATH, 'audio_model'))

# def predict(audio_path):
#     start_time = time.time()
#     result = pipe(audio_path)
#     end_time = time.time()
#     elapsed_time = end_time - start_time
#     return [pred[0]["label"] for pred in result], elapsed_time

# audio_files = [['backward16k.wav', 'happy16k.wav'], ['marvin16k.wav', 'seven16k.wav'], ['stop16k.wav', 'up16k.wav']]

# for audio_file in audio_files:
#     audio_path = [os.path.join(INPUT_PATH, audio) for audio in audio_file]
#     prediction, elapsed_time = predict(audio_path)
#     print(f"Prediction for {audio_file}: {prediction}")
#     print(f"Elapsed time: {elapsed_time:.6f} seconds\n")
