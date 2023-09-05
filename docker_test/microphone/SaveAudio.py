import sounddevice as sd
import numpy as np
from scipy.io import wavfile
from scipy.signal import decimate
import os
import argparse

audio_buffer = []

# Define the callback function
def audio_callback(indata, frames, time, status):
    audio_buffer.append(indata.copy())

def list_audio_devices():
    print("Available audio devices:")
    audio_devices = sd.query_devices()
    for i, device_info in enumerate(audio_devices):
        print(f"{i}: {device_info['name']}")

def record_audio(device, sample_rate):

    print('Recording...')
    # Start recording using InputStream with the specified device and sample rate
    audio_stream = sd.InputStream(
        device=device,
        callback=audio_callback,
        channels=1,
        samplerate=sample_rate,
        blocksize=int(sample_rate/2)
    )
    audio_stream.start()  # Initialize audio acquisition
    sd.sleep(5000)  # Sleep for 5 seconds (duration)
    audio_stream.stop()  # Stop the audio acquisition
    audio_stream.close()  # Close audio communication

    # Convert the audio buffer to a single numpy array
    audio_data = np.concatenate(audio_buffer, axis=0)
    audio_data = decimate(audio_data[:, 0], 3)

    # Save the audio data to a WAV file
    # output_dir = r"/media/dvd/DATA/repos/hands-free_cursor/docker_test/files/out" 
    output_dir = r"/app/files/out"
    output_filename = os.path.join(output_dir, "captured_audio.wav")
    wavfile.write(output_filename, int(sample_rate / 3), audio_data)

    print(f"Audio saved to {output_filename}")

if __name__ == "__main__":

    print("================================================================")
    print("                          SaveAudio                             ")
    print("================================================================")

    parser = argparse.ArgumentParser(description="Record audio from a specified audio device.")
    parser.add_argument("--device", type=int, default=0, help="Index of the audio device to use (default: 0)")
    parser.add_argument("--sample_rate", type=int, default=48000, help="Sample rate in Hz (default: 48000)")
    args = parser.parse_args()

    for arg in vars(args):
        print(f"{arg}: {getattr(args, arg)}")
    print("================================================================")

    # Show available audio devices
    list_audio_devices()

    # Call the record_audio function with the specified arguments
    record_audio(args.device, args.sample_rate)

