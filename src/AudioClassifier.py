"""
AudioClassifier class

Author: HenryAreiza
Date: 08/09/2023
"""

import os
import numpy as np
import sounddevice as sd
from scipy.signal import decimate
from transformers import pipeline

class AudioClassifier:
    """
    A class for classifying audio commands using a pre-trained model.

    This class provides functionality for classifying audio commands based on
    a pre-trained audio classification model.

    Attributes:
        verbose (boolean): Print (or not) detected commands
        vocab (list): Vocabulary of valid commands
        sensitivity (float): Microphone sensitivity (0.0 to 1.0)
        state (list): Last detected command and flag for 'new detected command'
        audio_buffer (list): A list to store audio buffer and flag for data availability.
        MODEL_PATH (str): Path to the pretrained AI model directory.
        pipe: The Hugging Face Transformers pipeline for audio classification.
        audio_stream: The sounddevice audio input stream.
    """

    def __init__(self, sensitivity=0.7, verbose=False):
        """
        Initializes the AudioClassifier class.
        """
        self.verbose = verbose
        self.vocab = ["left", "right", "up", "down", "go", "follow",
                      "on", "off", "one", "two", "three", "stop"]
        self.sensitivity = sensitivity
        self.state = ['', True]
        self.audio_buffer = [None, None, False]

        # Load the audio classification pipeline
        self.MODEL_PATH = os.path.join('models', 'speech_commands_model')
        if os.path.isdir(self.MODEL_PATH):
            self.pipe = pipeline("audio-classification", model=self.MODEL_PATH)
        else:
            self.pipe = pipeline("audio-classification", model="0xb1/wav2vec2-base-finetuned-speech_commands-v0.02")
            self.pipe.save_pretrained(self.MODEL_PATH)

        # Initialize the audio input stream
        self.audio_stream = sd.InputStream(callback=self.audio_callback, channels=1,
                                           samplerate=48000, blocksize=24000)

    def classify_audio(self, audio_data):
        """
        Classify audio data into a command label.

        Args:
            audio_data (numpy.ndarray): Input audio data.

        Returns:
            result (str): The classified command label.
        """
        result = self.pipe(audio_data)[0]["label"]
        return result

    def audio_callback(self, indata, _, __, ___):
        """
        Callback function to handle incoming audio data.

        Args:
            indata (numpy.ndarray): Input audio data.
        """
        self.audio_buffer[2] = True
        self.audio_buffer[0] = self.audio_buffer[1]
        self.audio_buffer[1] = indata.copy()
        self.audio_buffer[2] = False

    def read_buffer(self):
        """
        Read audio data from the buffer.

        Returns:
            numpy.ndarray: Concatenated audio data from the buffer.
        """
        while self.audio_buffer[2]:
            sd.sleep(1)
        return np.concatenate(self.audio_buffer[:2], axis=0)

    def run(self):
        """
        Start the audio classification process.
        """
        self.audio_stream.start()
        sd.sleep(int(2000))

        while self.state[0] != 'stop':
            sd.sleep(int(500))
            audio_data = self.read_buffer()
            if audio_data.max() > (1-self.sensitivity):
                sd.sleep(int(500))
                audio_data = self.read_buffer()
                audio_data = decimate(audio_data[:, 0], 3)
                result = self.classify_audio(audio_data)
                if result in self.vocab:
                    self.state = [result, True]
                else:
                    self.state = ['unknown', True]
                if self.verbose:
                    print(f"Detected Command: {self.state[0]}")
                sd.sleep(int(500))

        self.audio_stream.stop()
        self.audio_stream.close()


if __name__ == "__main__":
    """
    Run the audio commands test.
    """

    # Create an instance of the AudioClassifier class
    audio_classifier = AudioClassifier(verbose=True)

    print(f"""
          ---- Test of the class 'AudioClassifier' ----
          Please say any of the next speech commands:\n
          {audio_classifier.vocab[:6]}
          {audio_classifier.vocab[6:]}\n
          use the 'STOP' command to finish the test.\n
          """)
    
    # Run speech commands classifier
    audio_classifier.run()
