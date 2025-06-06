import cv2
import os
from datetime import datetime
import time

def create_folder(folder_name):
    """ Create folder if it doesn't exist """
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def capture_images(folder_name):
    # Open the webcam (0 for the primary camera)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam")
        return

    print("Hold 'c' to capture images every 0.5 seconds. Press 'q' to quit.")

    capturing = False
    last_capture_time = 0
    interval = 0.5  # Interval in seconds

    while True:
        # Read frame-by-frame
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read frame")
            break

        # Display the frame
        cv2.imshow("Hold 'c' to Capture | Press 'q' to Quit", frame)

        # Wait for user input
        key = cv2.waitKey(1)

        # Check if 'c' is held down
        if key == ord('c'):
            capturing = True
        else:
            capturing = False

        # Capture images every 0.5 seconds while holding 'c'
        if capturing and (time.time() - last_capture_time) >= interval:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S%f")
            file_name = os.path.join(folder_name, f"img_{timestamp}.jpg")
            cv2.imwrite(file_name, frame)
            print(f"Saved: {file_name}")
            last_capture_time = time.time()

        # Press 'q' to quit
        elif key == ord('q'):
            break

    # Release the webcam and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    folder_name = "captured_images"
    create_folder(folder_name)
    capture_images(folder_name)
