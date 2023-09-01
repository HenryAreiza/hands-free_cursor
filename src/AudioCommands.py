import os
import numpy as np
import sounddevice as sd
from scipy.signal import decimate
from transformers import pipeline

MODELS_PATH = os.path.join('models')

# Load the pipeline
pipe = pipeline("audio-classification", model=os.path.join(MODELS_PATH, 'audio_model'))

def classify_audio(audio_data):
    result = pipe(audio_data)[0]["label"]
    return result

# Define the callback function
audio_buffer = [None, None, False]
def audio_callback(indata, _, __, ___):
    audio_buffer[2] = True
    audio_buffer[0] = audio_buffer[1]
    audio_buffer[1] = indata.copy()
    audio_buffer[2] = False

def read_buffer(flag):
    while flag:
        sd.sleep(int(1))
    return np.concatenate(audio_buffer[:2], axis=0)

# Define audio InputStream
audio_stream = sd.InputStream(callback=audio_callback, channels=1,
                              samplerate=48000, blocksize=24000)

audio_stream.start()
sd.sleep(int(2000))
counter = 0
print('\nListening...')
while counter<20:
    sd.sleep(int(500))
    audio_data = read_buffer(audio_buffer[2])
    if audio_data.max() > 0.3:
        sd.sleep(int(500))
        audio_data = read_buffer(audio_buffer[2])
        audio_data = decimate(audio_data[:,0], 3)
        result = classify_audio(audio_data)
        print(f"{counter} - Command: {result}")
        sd.sleep(int(500))
        counter += 1

audio_stream.stop()
audio_stream.close()
print('\n')

