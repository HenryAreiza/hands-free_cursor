import cv2
import numpy as np

class Preprocessor:
    def __init__(self):
        pass

    @staticmethod
    def hist(image):
        """
        Compute the normalized histogram of a gray-scale image.
        Args:
            image (numpy.ndarray): Input gray-scale image.
        Returns:
            numpy.ndarray: Normalized histogram.
        """
        if len(image.shape) == 3:
            raise ValueError("Input image must be gray-scale (single channel).")

        # Calculate the histogram
        hist = cv2.calcHist([image], [0], None, [256], [0, 255])

        # Normalize the histogram
        hist /= hist.sum()

        return hist

    @staticmethod
    def hist2img(hist):
        """
        Transform a histogram into an image of size 100x255.
        Args:
            hist (numpy.ndarray): Input histogram.
        Returns:
            numpy.ndarray: Histogram image.
        """
        # Create an empty image
        hist_image = np.zeros((100, 255), dtype=np.uint8)

        # Calculate the maximum bin value
        max_bin_value = np.max(hist)
        if max_bin_value == 0:
            max_bin_value = 1

        # Scale and draw the histogram
        for i in range(255):
            h = int(hist[i] * 100 / max_bin_value)
            cv2.line(hist_image, (i, 100), (i, 100-h), 255)

        return hist_image
    
    @staticmethod
    def apply(image, kernel_size=None):
        """
        Apply a histogram equalization to the image.
        Args:
            image (numpy.ndarray): Input image.
            kernel_size (int): Size of the median filter kernel.
        Returns:
            numpy.ndarray: Processed image.
        """
        image_ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)

        # create a CLAHE object
        clahe = cv2.createCLAHE(clipLimit=5.0, tileGridSize=(8,8))
        image_ycrcb[:,:,0] = clahe.apply(image_ycrcb[:,:,0])
        image_ycrcb = cv2.cvtColor(image_ycrcb, cv2.COLOR_YCrCb2BGR)
        
        if kernel_size is not None:
            return cv2.medianBlur(image_ycrcb, kernel_size)
        else:
            return image_ycrcb


if __name__ == "__main__":
    # Create an instance of the Preprocessor class
    preprocessor = Preprocessor()

    # Open a connection to the first camera (typically the built-in webcam)
    cap = cv2.VideoCapture(0)

    while True:
        # Capture a frame from the camera
        ret, frame = cap.read()

        # Apply median filter to the gray-scale image
        enhanced_image = preprocessor.apply(frame, kernel_size=3)

        hist_image = np.zeros((100,255,3), dtype=np.uint8)
        hist_enhanced = np.zeros((100,255,3), dtype=np.uint8)
        for channel in range(3):
            # Compute and display the histogram
            histogram = preprocessor.hist(frame[:,:,channel])
            hist_image[:,:,channel] = preprocessor.hist2img(histogram)

            histogram = preprocessor.hist(enhanced_image[:,:,channel])
            hist_enhanced[:,:,channel] = preprocessor.hist2img(histogram)

        # Display the stacked images
        cv2.imshow("Original image", frame)
        cv2.imshow("Original histogram", hist_image)
        cv2.imshow("Enhanced image", enhanced_image)
        cv2.imshow("Enhanced histogram", hist_enhanced)

        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
