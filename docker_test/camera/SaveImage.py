import cv2
import time
import os

def main():
    # Open the camera (0 represents the default camera)
    cap = cv2.VideoCapture(0)

    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Create an output directory
    output_dir = "/app/files/out"
    os.makedirs(output_dir, exist_ok=True)

    # Camera warmup
    ret, frame = cap.read()
    time.sleep(0.1)
    
    try:
        # Capture and save 5 images
        for i in range(5):
            # Capture a frame from the camera
            ret, frame = cap.read()

            if not ret:
                print("Error: Failed to capture frame.")
                break

            # Save the captured image
            image_filename = os.path.join(output_dir, f"image_{i}.jpg")
            cv2.imwrite(image_filename, frame)

            print(f"Saved image {i + 1}")

            # Wait for 1 second before capturing the next image
            time.sleep(0.1)

    finally:
        # Release the camera
        cap.release()

if __name__ == "__main__":
    main()

