"""
Create Dataset Script

This script captures camera images when a left mouse click is detected. It uses OpenCV and pynput
libraries to detect eyes and record click locations. Captured images and click data are saved in
folders, and a JSON file contains information about the capture session.

Author: HenRick69
Date: 29/08/2023
"""

import os
import csv
import cv2
import json
import datetime
import pyautogui
from pynput.mouse import Listener, Button

class CreateDataset:
    def __init__(self):
        # Create data folders
        self.DATA_PATH = os.path.join('data', 'deivid')
        self.FOLDER_PATH = os.path.join(self.DATA_PATH,datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S"))
        self.IMGS_PATH = os.path.join(self.FOLDER_PATH,'images')
        os.mkdir(self.FOLDER_PATH)
        os.mkdir(self.IMGS_PATH)

        # Load the pre-trained face detection model
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

        # Initialize data lists
        self.click_history = []
        self.eyes_history = []
        self.location_history = []
        self.eyes_capture = None
        self.location = None

    def on_click(self, x, y, button, pressed):
        """
        Callback function for mouse click events.
        Records left click positions and associated eye images.
        """
        if pressed:
            if button == Button.left:
                self.click_history.append([x, y])
                self.eyes_history.append(self.eyes_capture)
                self.location_history.append(self.location)
                print(f"Left click detected at ({x}, {y})")

    def capture_camera_image(self):
        """
        Captures an image from the camera and returns it.
        """
        _, frame = self.capture.read()
        return frame

    def save_csv(self):
        """
        Saves the click history, eye history, and location history into a CSV file.
        """
        header = ['file_name', 'im_width', 'im_height', 'im_depth', 'ref_x', 'ref_y', 'ref_w', 'ref_h', 'click_x', 'click_y']
        data = []
        for i, (click, image, location) in enumerate(zip(self.click_history, self.eyes_history, self.location_history)):
            name = [f'{i}.jpg']
            im_shape = list(image.shape)
            data.append(name + im_shape + location + click)
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
            'images': len(self.click_history),
            'date': self.FOLDER_PATH[-19:],
            'screen_width': screen_size.width,
            'screen_height': screen_size.height,
        }
        with open(os.path.join(self.FOLDER_PATH, 'data_info.json'), 'w') as json_file:
            json.dump(data_info, json_file, indent=4)

    def save_image(self, image, prefix):
        """
        Saves the captured eye image to a file.
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

        # Open the video capture
        self.capture = cv2.VideoCapture(0)
        min_size = int(min(list(pyautogui.size()))/4)

        while True:
            # Read the current frame from the video capture
            frame = self.capture_camera_image()

            # Convert the frame to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Histogram equalization
            clahe = cv2.createCLAHE(clipLimit=5.0, tileGridSize=(8,8))
            gray = clahe.apply(gray)

            # Perform face detection
            faces = self.eye_cascade.detectMultiScale(gray, scaleFactor=1.1,
                                                      minNeighbors=5, minSize=(min_size, min_size))

            # Draw rectangles around the detected eyes
            for x, y, w, h in faces:
                x = int(x+w/5)
                w = int(3*w/5)
                y = int(y+h/4)
                h = int(h/4)
                self.eyes_capture = frame[y:y+h, x:x+w].copy()
                self.location = [x, y, w, h]
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                break

            # Display the resulting frame
            cv2.imshow('Eyes Detection', frame)

            # Exit the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.listener_thread.stop()

        # Release the video capture and close the window
        self.capture.release()
        cv2.destroyAllWindows()

        self.save_csv()
        print('\nCSV file saved!')

        self.save_json()
        print('JSON file saved!')

        for i, image in enumerate(self.eyes_history):
            self.save_image(image, i)
        print('Images saved!\n')


if __name__ == "__main__":
    dataset = CreateDataset()
    dataset.run()
