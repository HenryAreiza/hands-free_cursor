"""
FacePosition class

Author: HenryAreiza
Date: 08/09/2023
"""

import os
import cv2
import pickle
import pyautogui
import numpy as np
import mediapipe as mp
from src.Cursor import Cursor

class FacePosition:
    """
    A class for controlling the cursor based on head movements.

    This class provides functionality for detecting a face using
    the MediaPipe library and controlling the cursor's movement accordingly.

    Attributes:
        cursor_location (numpy.ndarray): The current cursor location as a normalized coordinate (x, y).
        speed (int): Cursor movement speed
        movement (numpy.ndarray): Movement vectors for different gestures.
        screen_size (numpy.ndarray): The screen size in pixels.
        cursor_model: The machine learning model for gesture prediction.
        face_detection: The MediaPipe Face Detection component.
    """

    def __init__(self):
        """
        Initializes the FaceCursorController class.
        """
        self.cursor_location = np.array([0.5, 0.5])
        self.speed = 2
        self.movement = np.array([[0, 0], [0, -1], [-1, -1], [-1, 0],
                                  [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1]])
        self.screen_size = np.array(pyautogui.size())

        # Load the cursor movement model
        with open(os.path.join('models', 'cursor_movement_model.pkl'), 'rb') as f:
            self.cursor_model = pickle.load(f)

        # Initialize the MediaPipe Face Detection component
        self.face_detection = mp.solutions.face_detection.FaceDetection(min_detection_confidence=0.5)     

    def move_cursor(self, reference, keypoints):
        """
        Move the cursor based on head position.

        Args:
            reference (list): A list containing reference coordinates and size of the bounding box.
            keypoints (list): A list of keypoints representing face landmarks.
        """
        # Transform the lists into numpy arrays
        reference = np.array(reference)
        keypoints = np.array(keypoints)

        # Remove off-set from keypoints
        keypoints = (keypoints - reference[0]) / reference[1]

        # Recognize the head position
        move = self.cursor_model.predict(keypoints.reshape((1, -1)))[0]

        # Move the cursor
        move = self.movement[move] * 10 * self.speed / self.screen_size
        self.cursor_location += move
        self.cursor_location[self.cursor_location >= 1] = 0.999
        self.cursor_location[self.cursor_location <= 0] = 0.001


if __name__ == "__main__":
    """
    Run the cursor control test.
    """
    # Create an instance of the Cursor class
    cursor = Cursor()

    # Create an instance of the FacePosition class
    position_controller = FacePosition()

    # Open the video capture
    capture = cv2.VideoCapture(0)

    print("""
          ----- Test of the class 'FacePosition' started... -----
          Please control the cursor position by moving your head.
          Move the cursor to the top/left position of your screen
          to finish the test.\n
          """)

    while position_controller.cursor_location.sum() > 0.004:
        # Capture a frame from the camera
        _, frame = capture.read()

        # Convert the BGR image to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Perform face detection
        results = position_controller.face_detection.process(frame)

        # Read the reference and landmarks from the detected face
        if results.detections:
            for detection in results.detections:
                reference = [[detection.location_data.relative_bounding_box.xmin,
                              detection.location_data.relative_bounding_box.ymin],
                             [detection.location_data.relative_bounding_box.width,
                              detection.location_data.relative_bounding_box.height]]

                keypoints = []
                for key_point in detection.location_data.relative_keypoints:
                    keypoints.append([key_point.x, key_point.y])

                position_controller.move_cursor(reference, keypoints)
                cursor.move(*position_controller.cursor_location)
                break

    # Release the camera
    capture.release()