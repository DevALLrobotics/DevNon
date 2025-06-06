import cv2
import torch
import time
from ultralytics import YOLO

# Load the trained YOLOv8 model
model_path = '../trashPJ/model/best_2.pt'
model = YOLO(model_path)

# Open webcam
cap = cv2.VideoCapture(0)

# Set webcam properties
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Perform inference
    start_time = time.time()
    results = model(frame)
    end_time = time.time()

    # Extract predictions
    for result in results:
        for bbox in result.boxes:
            x1, y1, x2, y2 = bbox.xyxy[0].tolist()
            confidence = bbox.conf[0]
            label = bbox.cls[0]

            # Draw bounding box and label
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, f'{label} {confidence:.2f}', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Calculate FPS
    fps = 1 / (end_time - start_time)
    cv2.putText(frame, f'FPS: {fps:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('YOLOv8 Real-Time Detection', frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
