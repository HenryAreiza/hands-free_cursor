"""
AudioClassifier class

Author: HenryAreiza
Date: 08/09/2023
"""

from scipy.io import wavfile
from scipy.signal import decimate
from transformers import pipeline

class AudioClassifier:
    """
    A class for classifying audio commands using a pre-trained model.

    This class provides functionality for classifying audio commands based on
    a pre-trained audio classification model.

    Attributes:
        vocab (list): Vocabulary of valid commands
        pipe: The Hugging Face Transformers pipeline for audio classification.
    """

    def __init__(self):
        """
        Initializes the AudioClassifier class.
        """
        self.vocab = ["left", "right", "up", "down", "go", "follow",
                      "on", "off", "one", "two", "three", "stop"]

        # Load the audio classification pipeline
        self.pipe = pipeline("audio-classification", model="0xb1/wav2vec2-base-finetuned-speech_commands-v0.02")

    def predict(self, audio_path):
        """
        Classify audio data into a command label.

        Args:
            audio_data (numpy.ndarray): Input audio data.

        Returns:
            result (str): The classified command label.
        """
        _, audio = wavfile.read(audio_path)
        audio = decimate(audio, 3)
        result = self.pipe(audio)[0]["label"]

        if result not in self.vocab:
            result = 'unknown'

        return result

   

