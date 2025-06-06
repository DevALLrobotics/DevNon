import cv2
import torch
import time
import os
from ultralytics import YOLO

# Load the trained YOLOv8 model
model_path = '../trashPJ/model/bestv6.pt'
if not os.path.exists(model_path):
    print(f"Model path not found: {model_path}")
    exit(1)

model = YOLO(model_path)

# Define class labels
label_map = {
    1: "plastic",
    0: "paper",
}

# Open webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Unable to access the webcam.")
    exit(1)

# Set webcam properties
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Convert frame to RGB for YOLO model
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Start time for FPS calculation
    start_time = cv2.getTickCount()

    # Perform inference
    results = model(frame_rgb)

    # End time for FPS calculation
    end_time = cv2.getTickCount()
    time_elapsed = (end_time - start_time) / cv2.getTickFrequency()
    fps = 1 / time_elapsed

    # Extract predictions and draw bounding boxes
    for result in results:
        for bbox in result.boxes:
            x1, y1, x2, y2 = map(int, bbox.xyxy[0])
            confidence = float(bbox.conf[0])
            class_id = int(bbox.cls[0])

            # Get label text
            label = label_map.get(class_id, "Unknown")

            # Draw bounding box and label
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f'{label} {confidence:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display FPS
    cv2.putText(frame, f'FPS: {fps:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('YOLOv8 Real-Time Detection', frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
