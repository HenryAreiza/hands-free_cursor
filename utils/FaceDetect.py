import cv2
import mediapipe as mp

# Initialize the MediaPipe Face Detection component
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# Initialize the webcam capture
cap = cv2.VideoCapture(0)

# Create a face detection object
with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            continue

        # Convert the BGR image to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Perform face detection
        results = face_detection.process(frame_rgb)

        # Draw face bounding boxes
        if results.detections:
            for detection in results.detections:
                mp_drawing.draw_detection(frame, detection)
                location = [detection.location_data.relative_bounding_box.xmin,
                            detection.location_data.relative_bounding_box.ymin,
                            detection.location_data.relative_bounding_box.width,
                            detection.location_data.relative_bounding_box.height]
                keypoints = []
                for key_point in detection.location_data.relative_keypoints:
                    keypoints.append(key_point.x)
                    keypoints.append(key_point.y)

        # Display the frame with detected faces
        cv2.imshow('Face Detection', frame)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
