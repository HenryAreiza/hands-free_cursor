import os
import cv2
import pickle
import threading
import pyautogui
import numpy as np
from Cursor import Cursor
from Preprocessor import Preprocessor


inputs = [None, None, True]
def move_cursor():
    # Getting back the eyes model:
    with open(os.path.join('models', 'eyes_model', 'model-20230906_084133.pkl'), 'rb') as f:
        eyes_model = pickle.load(f)
        # eyes_model.summary()

    # Create an instance of the Preprocessor class
    preprocessor = Preprocessor()

    # Create an instance of the Cursor class
    cursor = Cursor()

    predictions = np.zeros((5,2))

    print('\nCursor control started...\n')
    while inputs[2]:
        if inputs[0] is not None:
            eyes_capture, location, _ = inputs
            
            enhanced_eyes = cv2.resize(eyes_capture, (130, 50))
            enhanced_eyes = preprocessor.apply(enhanced_eyes, limit=2.0, grid=(8,8))
            enhanced_eyes = np.reshape(enhanced_eyes, (1, 50, 130, 3))
            enhanced_eyes = enhanced_eyes.astype(float) / 255
            
            location[[0,2]] /= im_width
            location[[1,3]] /= im_height
            location = np.reshape(location, (1, 4))
            
            prediction = eyes_model.predict([enhanced_eyes, location], verbose=0)
            prediction[prediction>=1] = 0.999
            prediction[prediction<=0] = 0.001

            predictions[:-1] = predictions[1:]
            predictions[-1] = prediction[0]
            cursor.move(*predictions.mean(axis=0))


if __name__ == "__main__":
    cursor_thread = threading.Thread(target=move_cursor)
    cursor_thread.start()

    # Load the pre-trained face detection model
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

    # Open the video capture
    capture = cv2.VideoCapture(0)
    # Initial capture a frame from the camera
    _, frame = capture.read()
    im_height, im_width, _ = frame.shape

    clahe = cv2.createCLAHE(clipLimit=5.0, tileGridSize=(8,8))
    min_size = int(min(list(pyautogui.size()))/7)

    while True:
        # Capture a frame from the camera
        _, frame = capture.read()

        # Convert the frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = clahe.apply(gray)

        # Perform face detection
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1,
                                              minNeighbors=5, minSize=(min_size, min_size))

        # Draw rectangles around the detected eyes
        eyes_capture = None
        for x, y, w, h in faces:
            x = int(x+w/5)
            w = int(3*w/5)
            y = int(y+h/4)
            h = int(h/4)
            eyes_capture = frame[y:y+h, x:x+w].copy()
            location = np.array([x, y, w, h], dtype=float)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            break

        # Display the resulting frame
        cv2.imshow('Eyes Detection', frame)

        if eyes_capture is not None:
            inputs = [eyes_capture, location, True]

        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    inputs = [None, None, False]
    cursor_thread.join()

    # Release the camera and close all OpenCV windows
    capture.release()
    cv2.destroyAllWindows()
