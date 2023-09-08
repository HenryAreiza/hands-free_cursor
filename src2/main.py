import os
import cv2
import pickle
import pyautogui
import numpy as np
import mediapipe as mp
from Cursor import Cursor


cursor_location = np.array([0.5, 0.5])
movement = np.array([[0, 0],   # center
                     [0, -1],  # up
                     [-1, -1], # left/up
                     [-1, 0],  # left
                     [-1, 1],  # left/down
                     [0, 1],   # down
                     [1, 1],   # right/down
                     [1, 0],   # right
                     [1, -1]])  # rigth/up
screen_size = np.array(pyautogui.size())
classes = {0:'center', 1:'up', 2:'left/up', 3:'left', 4:'left/down',
           5:'down', 6:'right/down', 7:'right', 8:'right/up'}

def move_cursor(reference, keypoints, cursor, model):
    global cursor_location, movement, screen_size, classes

    reference = np.array(reference)
    keypoints = np.array(keypoints)
    
    keypoints = (keypoints-reference[0]) / reference[1]

    move = model.predict(keypoints.T.reshape((1,-1)))[0]
    move = movement[move] * 20 / screen_size
    cursor_location += move
    cursor_location[cursor_location>=1] = 0.999
    cursor_location[cursor_location<=0] = 0.001

    cursor.move(*cursor_location)


if __name__ == "__main__":
    # Getting back the eyes model:
    with open(os.path.join('models', 'cursor_model.pkl'), 'rb') as f:
        cursor_model = pickle.load(f)

    # Initialize the MediaPipe Face Detection component
    face_detection = mp.solutions.face_detection
    # drawing = mp.solutions.drawing_utils

    # Create a face detection object
    face_detection = face_detection.FaceDetection(min_detection_confidence=0.5)

    # Create an instance of the Cursor class
    cursor = Cursor()

    # Open the video capture
    capture = cv2.VideoCapture(0)

    while True:
        # Capture a frame from the camera
        _, frame = capture.read()

        # Convert the BGR image to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Perform face detection
        results = face_detection.process(frame_rgb)

        # Draw face bounding boxes
        if results.detections:
            for detection in results.detections:                    
                reference = [[detection.location_data.relative_bounding_box.xmin,
                            detection.location_data.relative_bounding_box.ymin],
                            [detection.location_data.relative_bounding_box.width,
                            detection.location_data.relative_bounding_box.height]]
                
                keypoints = []
                for key_point in detection.location_data.relative_keypoints:
                    keypoints.append([key_point.x, key_point.y])

                # drawing.draw_detection(frame, detection)
                move_cursor(reference, keypoints, cursor, cursor_model)
                break

        # # Display the resulting frame
        # cv2.imshow('Face Detection', frame)

        # Exit the loop if 'q' is pressed
        if (cv2.waitKey(1) & 0xFF == ord('q')):
            break
    
    # Release the camera and close all OpenCV windows
    capture.release()
    cv2.destroyAllWindows()
