"""
Hands-free Cursor Application

Authors: HenryAreiza, deividbotina-alv
Date: 08/09/2023

This Python script represents a comprehensive application for controlling the computer's cursor and performing
various mouse actions using voice commands and head position. It integrates three major components:
audio classification, face detection for cursor positioning, and mouse action execution.

Components:
1. Audio Classifier:
   - Utilizes a pre-trained audio classification model to recognize voice commands.
   - Runs in a separate thread to continuously listen for and classify audio input.
   - Provides real-time feedback on recognized commands and their execution status.

2. Face Position Controller:
   - Utilizes the MediaPipe library for real-time face detection.
   - Tracks the position of a user's face in the webcam feed.
   - Calculates the reference and facial landmarks to control cursor movement.

3. Cursor Controller:
   - Provides a set of mouse actions, including left-click, right-click, scrolling, double-clicking, and more.
   - Controls the cursor's position and interacts with the computer's graphical interface.

Main Functionality:
- The application continuously listens for voice commands and tracks the user's face.
- When a voice command is recognized, the corresponding mouse action is triggered.
- The cursor's movement is controlled based on facial landmarks and gesture recognition.

Voice Commands and Corresponding Actions:
- "left": Performs a left mouse click.
- "right": Performs a right mouse click.
- "up" or "down": Scrolls the mouse wheel up or down, respectively.
- "go": Performs a double left mouse click.
- "follow": Initiates sustained left mouse click (release by repeating the command).
- "on": Activates the functionality for cursor's movement controlled by head position.
- "off": Deactivates the functionality for cursor's movement controlled by head position.
- "one", "two", "three": Adjusts the cursor speed (and scroll step) to slow, medium, or fast, respectively.
- "stop": Exits the program and terminates the application.

Usage:
- Run the script to start the application.
- Use the listed voice commands to control the cursor and perform mouse actions.
- Move your head intuitively to move the cursor on the screen.
- The program provides real-time feedback on executed commands and actions.
- Exit the program by issuing a "stop" command or closing the application window.

Note:
- Ensure that the required dependencies and AI models are installed for proper functionality.
- This application is designed to provide hands-free control and enhance accessibility for users with motor disabilities.
"""

from AudioClassifier import AudioClassifier
from FacePosition import FacePosition
from Cursor import Cursor, mouse_action
import threading
import argparse
import cv2

if __name__ == "__main__":
    """
    Main function for the Hands-free Cursor Application.

    This function serves as the entry point for the application. It orchestrates the integration
    of audio classification, face detection, cursor control, and mouse actions. The application listens
    for voice commands, tracks the user's face, and performs mouse actions accordingly.

    Input Parameters:
        --verbose (int): Interpreted as bool, it enables verbose mode (1 (true)/ 0 (false))
        --mic_sens (float): Microphone sensitivity (0.0 to 1.0)
    """

    # Define main file arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', type=int, default=1, help="Enable verbose mode (1 (true)/ 0 (false))")
    parser.add_argument('--mic_sens', type=float, default=0.7, help="Microphone sensitivity (0.0 to 1.0)")
    args = parser.parse_args()

    # Create an instance of the AudioClassifier class
    audio_classifier = AudioClassifier(sensitivity=args.mic_sens)

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
    
    if args.verbose:
        print("""\n
          ********************************************************************
                         Hands-free Cursor application started...             
          ********************************************************************    
          Please control the cursor position by moving your head.
          Please say any of the next speech commands:
            - "left": left mouse click.
            - "right": right mouse click.
            - "up" or "down": Scrolls the mouse wheel.
            - "go": double left mouse click.
            - "follow": sustained left click (release by repeating the command).
            - "on": Activates the cursor's movement functionality.
            - "off": Deactivates the cursor's movement functionality.
            - "one", "two", "three": Adjusts the cursor speed.
            - "stop": Exits the program and terminates the application.
          use the 'STOP' command to close the application.\n
          """)

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
        
        # Check for new voice commands
        if audio_classifier.state[1]:
            move_active = mouse_action(cursor, position_controller, audio_classifier.state[0],
                                       move_active, verbose=args.verbose)
            audio_classifier.state[1] = False

    # Wait for the audio thread to finish
    audio_thread.join()

    # Release the camera
    capture.release()
