import sounddevice as sd
import numpy as np
from scipy.io import wavfile
from scipy.signal import decimate
import os

# Define the callback function
def audio_callback(indata, frames, time, status):
    audio_buffer.append(indata.copy())

if __name__ == "__main__":

    # Create an output directory
    #output_dir = r"/media/dvd/DATA/repos/hands-free_cursor/docker_test/files/out" 
    output_dir = r"/app/files/out"

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
    output_filename = os.path.join(output_dir,"captured_audio.wav")
    wavfile.write(output_filename, int(sample_rate/3), audio_data)

    print(f"Audio saved to {output_filename}")

