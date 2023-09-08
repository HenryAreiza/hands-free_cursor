"""
main file

Author: HenRick69
Date: 08/09/2023
"""

from AudioClassifier import AudioClassifier
from FacePosition import FacePosition
from Cursor import Cursor
import threading
import cv2

def mouse_action(cursor_obj, position_obj, action, state):  
    if action == "left":
        cursor_obj.left_click()
    elif action == "right":
        cursor_obj.right_click()
    elif action in ["up", "down"]:
        cursor_obj.scroll(position_obj.speed, action)
    elif action == "go":
        cursor_obj.double_left_click()
    elif action == "follow":
        cursor_obj.sustained_left_click()
    elif action == "on":
        return True
    elif action == "off":
        return False
    elif action == "one":
        position_obj.speed = 1
    elif action == "two":
        position_obj.speed = 2
    elif action == "three":
        position_obj.speed = 3
    elif action == "stop":
        print('\nProgram finished.\n')
    else:
        print('Unknown command.')       
    return state

if __name__ == "__main__":
    # Create an instance of the AudioClassifier class
    audio_classifier = AudioClassifier(verbose=True)

    # Run speech commands classifier in a parallel thread
    audio_thread = threading.Thread(target=audio_classifier.run)
    audio_thread.start()

     # Create an instance of the Cursor class
    cursor = Cursor()

    # Create an instance of the FacePosition class
    position_controller = FacePosition()  
    move_active = True

    # Open the video capture
    capture = cv2.VideoCapture(0)

    print('\nProgram started.\n')

    while audio_classifier.state[0] != 'stop':
        if move_active:
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
        
        if audio_classifier.state[1]:
            move_active = mouse_action(cursor, position_controller, audio_classifier.state[0], move_active)
            audio_classifier.state[1] = False

    # Wait for audio thread to finish
    audio_thread.join()

    # Release the camera
    capture.release()