"""
Create Dataset Script

This script captures camera images for different head positions. It uses OpenCV and
mediapipe libraries to detect faces in real time. Captured images and relevant data are
saved in folders, and a JSON file contains information about the capture session.

Author: HenryAreiza
Date: 06/09/2023
"""

import os
import csv
import cv2
import json
import datetime
import pyautogui
import mediapipe as mp
from pynput.mouse import Listener, Button

class CreateDataset:
    """
    A class for creating the dataset used to train the FacePosition AI model.

    This class is responsible for capturing camera images for different head positions.
    It creates data folders, handles face detection, records image data, and saves captured
    images along with relevant information.

    Attributes:
        DATA_PATH (str): Path to the dataset folder.
        FOLDER_PATH (str): Path to the current capture session folder.
        IMGS_PATH (str): Path to the folder where captured images are saved.
        face_detection: An instance of the MediaPipe Face Detection component.
        drawing: An instance of MediaPipe's drawing utilities.
        faces_history (list): A list to store captured face images.
        location_history (list): A list to store face bounding box locations.
        keypoints_history (list): A list to store relative keypoints of the detected face.
        labels_history (list): A list to store labels for captured images.
        face_capture: The currently captured face image.
        location: The bounding box location of the detected face.
        keypoints: Relative keypoints of the detected face.
        im_width (int): Width of the camera frame.
        im_height (int): Height of the camera frame.
        im_depth (int): Depth of the camera frame.
        flag (bool): A flag indicating whether data capture is active.
        label (int): The label/index for the current capture session.
        counter (int): A counter to track the number of captured images.
        limit (int): The maximum number of images to capture for each label.
        labels (list): A list of label names corresponding to head positions.
    """
    
    def __init__(self):
        """
        Initializes the CreateDataset class.
        """
        # Create data folders
        self.DATA_PATH = os.path.join('data', 'subject_0')
        self.FOLDER_PATH = os.path.join(self.DATA_PATH,datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S"))
        self.IMGS_PATH = os.path.join(self.FOLDER_PATH,'images')
        os.mkdir(self.FOLDER_PATH)
        os.mkdir(self.IMGS_PATH)
        
        # Initialize the MediaPipe Face Detection component
        self.face_detection = mp.solutions.face_detection
        self.drawing = mp.solutions.drawing_utils

        # Initialize data lists
        self.faces_history = []
        self.location_history = []
        self.keypoints_history = []
        self.labels_history = []
        self.face_capture = None
        self.location = None
        self.keypoints = None
        self.im_width = 0
        self.im_height = 0
        self.im_depth = 0
        self.flag = False
        self.label = 0
        self.counter = 0
        self.limit = 10
        self.labels = ['center', 'up', 'left/up', 'left', 'left/down',
                       'down', 'right/down', 'right', 'right/up']

    def on_click(self, _, __, button, pressed):
        """
        Callback function for mouse click events.
        Records left click positions and associated eye images.

        Args:
            _: The x-coordinate of the mouse click (unused).
            __: The y-coordinate of the mouse click (unused).
            button: The button that was clicked.
            pressed: A boolean indicating whether the button was pressed or released.
        """
        if pressed:
            if button == Button.left:
                self.flag = True
                print(f"Taking data for {self.labels[self.label]} position...\n")

    def capture_camera_image(self):
        """
        Captures an image from the camera and returns it.

        Returns:
            numpy.ndarray: The captured camera image.
        """
        _, frame = self.capture.read()
        return frame

    def save_csv(self):
        """
        Saves the location history, keypoints history, and label into a CSV file.
        """
        header = ['file_name', 'ref_x', 'ref_y', 'ref_w', 'ref_h', 'kpt1_x', 'kpt1_y', 'kpt2_x', 'kpt2_y',
                  'kpt3_x', 'kpt3_y', 'kpt4_x', 'kpt4_y', 'kpt5_x', 'kpt5_y', 'kpt6_x', 'kpt6_y', 'label']
        data = []
        for location, keypoints, label in zip(self.location_history, self.keypoints_history, self.labels_history):
            name = [f'{label}-{self.counter}.jpg']
            data.append(name + location + keypoints + [label])
            self.counter += 1
            if self.counter >= self.limit:
                self.counter = 0
        with open(os.path.join(self.FOLDER_PATH, 'data_info.csv'), 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(header)
            csv_writer.writerows(data)

    def save_json(self):
        """
        Saves relevant data as JSON, including image count, date, and screen size.
        """
        screen_size = pyautogui.size()
        data_info = {
            'images': len(self.location_history),
            'date': self.FOLDER_PATH[-19:],
            'screen_width': screen_size.width,
            'screen_height': screen_size.height,
            'im_width': self.im_width,
            'im_height': self.im_height, 
            'im_depth': self.im_depth
        }
        with open(os.path.join(self.FOLDER_PATH, 'data_info.json'), 'w') as json_file:
            json.dump(data_info, json_file, indent=4)

    def save_image(self, image, prefix):
        """
        Saves the captured image to a file.

        Args:
            image (numpy.ndarray): The captured image.
            prefix (str): The filename prefix for the saved image.
        """
        file_name = f"{prefix}.jpg"
        cv2.imwrite(os.path.join(self.IMGS_PATH, file_name), image)

    def run(self):
        """
        Main loop for capturing and processing camera images.
        """
        # Start the mouse listener
        self.listener_thread = Listener(on_click=self.on_click)
        self.listener_thread.start()

        # Create a face detection object
        face_detection = self.face_detection.FaceDetection(min_detection_confidence=0.5)

        # Open the video capture
        self.capture = cv2.VideoCapture(0)

        print(f'\nClick to start {self.labels[self.label]} acquisition.')
        while True:
            # Read the current frame from the video capture
            frame = self.capture_camera_image()
            self.im_height, self.im_width, self.im_depth = frame.shape

            # Convert the BGR image to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Perform face detection
            results = face_detection.process(frame_rgb)

            # Read the reference and landmarks from the detected face
            if results.detections:
                for detection in results.detections:                    
                    self.location = [detection.location_data.relative_bounding_box.xmin,
                                     detection.location_data.relative_bounding_box.ymin,
                                     detection.location_data.relative_bounding_box.width,
                                     detection.location_data.relative_bounding_box.height]
                    
                    self.keypoints = []
                    for key_point in detection.location_data.relative_keypoints:
                        self.keypoints.append(key_point.x)
                        self.keypoints.append(key_point.y)
                    
                    x = int(self.location[0] * self.im_width)
                    y = int(self.location[1] * self.im_height)
                    w = int(self.location[2] * self.im_width)
                    h = int(self.location[3] * self.im_height)
                    self.face_capture = frame[y:y+h, x:x+w].copy()

                    self.drawing.draw_detection(frame, detection)
                    break

            # Save the reference and landmarks from the detected face
            if self.flag:
                self.faces_history.append(self.face_capture)
                self.location_history.append(self.location)
                self.keypoints_history.append(self.keypoints)
                self.labels_history.append(self.label)
                self.counter += 1
                if self.counter >= self.limit:
                    self.counter = 0
                    self.label += 1
                    self.flag = False
                    if self.label < 9:
                        print(f'Click to start {self.labels[self.label]} acquisition.')
                    else:
                        break
                        

            # Display the resulting frame
            cv2.imshow('Face Detection', frame)

            # Exit the loop if 'q' is pressed
            if (cv2.waitKey(1) & 0xFF == ord('q')):
                break

        self.listener_thread.stop()

        # Release the video capture and close the window
        self.capture.release()
        cv2.destroyAllWindows()

        self.save_csv()
        print('\nCSV file saved!')

        self.save_json()
        print('JSON file saved!')

        for i, image in enumerate(self.faces_history):
            self.save_image(image, f'{self.labels_history[i]}-{self.counter}')
            self.counter += 1
            if self.counter >= self.limit:
                self.counter = 0
        print('Images saved!\n')


if __name__ == "__main__":
    dataset = CreateDataset()
    dataset.run()
