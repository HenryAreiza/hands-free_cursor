"""
FacePosition class

Author: HenryAreiza
Date: 08/09/2023
"""

import os
import cv2
import pickle
import numpy as np
import mediapipe as mp

class FacePosition:
    """
    A class for controlling the cursor based on head movements.

    This class provides functionality for detecting a face using
    the MediaPipe library and controlling the cursor's movement accordingly.

    Attributes:
        movement (list): List of classes corresponding to the predicted movement.
        images (list): List of images associated to each class
        cursor_model: The machine learning model for gesture prediction.
        face_detection: The MediaPipe Face Detection component.
    """

    def __init__(self):
        """
        Initializes the FaceCursorController class.
        """
        self.movement = ['Center', 'Up', 'Right/Up', 'Right', 'Right/Down', 'Down', 'Left/Down', 'Left', 'Left/Up']
        self.images = [cv2.imread(os.path.join('media', str(i)+'.png')) for i in range(9)]

        # Load the cursor movement model
        with open('cursor_movement_model.pkl', 'rb') as f:
            self.cursor_model = pickle.load(f)

        # Initialize the MediaPipe Face Detection component
        self.face_detection = mp.solutions.face_detection.FaceDetection(min_detection_confidence=0.5)     

    def predict(self, frame):
        """
        Move the cursor based on head position.

        Args:
            reference (list): A list containing reference coordinates and size of the bounding box.
            keypoints (list): A list of keypoints representing face landmarks.

        Returns:
            result (list): The predicted class image and label.
        """
        # Perform face detection
        results = self.face_detection.process(frame)

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
                break

            # Transform the lists into numpy arrays
            reference = np.array(reference)
            keypoints = np.array(keypoints)

            # Remove off-set from keypoints
            keypoints = (keypoints - reference[0]) / reference[1]

            # Recognize the head position
            prediction = self.cursor_model.predict(keypoints.reshape((1, -1)))[0]

            return [self.images[prediction], self.movement[prediction]]
        
        else:
            return [self.images[0], self.movement[0]]

