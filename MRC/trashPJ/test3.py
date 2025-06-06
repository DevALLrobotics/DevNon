import cv2
import torch
import time
import os
import serial
from ultralytics import YOLO

# === กำหนดเส้นทางโมเดล YOLOv8 ===
model_path = '../MRC/model/bestv6.pt'
if not os.path.exists(model_path):
    print(f"Model path not found: {model_path}")
    exit(1)

model = YOLO(model_path)

# === กำหนด label ของคลาส ===
label_map = {
    1: "plastic",
    0: "paper",
}

# === เชื่อมต่อ Arduino ===
try:
    arduino = serial.Serial('COM24', 9600)  # <-- เปลี่ยนตามพอร์ตของคุณ
    time.sleep(2)  # รอให้ Arduino พร้อมทำงาน
except Exception as e:
    print(f"Failed to connect to Arduino: {e}")
    exit(1)

# === เปิดกล้อง ===
cap = cv2.VideoCapture(1)
if not cap.isOpened():
    print("Error: Unable to access the webcam.")
    exit(1)

# สำหรับการเช็คสถานะพลาสติก
plastic_detected = False

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    start_time = cv2.getTickCount()
    results = model(frame_rgb)
    end_time = cv2.getTickCount()
    time_elapsed = (end_time - start_time) / cv2.getTickFrequency()
    fps = 1 / time_elapsed

    detected_plastic = False

    for result in results:
        for bbox in result.boxes:
            x1, y1, x2, y2 = map(int, bbox.xyxy[0])
            confidence = float(bbox.conf[0])
            class_id = int(bbox.cls[0])
            label = label_map.get(class_id, "Unknown")

            # === ตรวจจับเฉพาะเมื่อ label เป็น plastic และ confidence > 0.7 ===
            if label == "plastic" and confidence > 0.7:
                detected_plastic = True

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f'{label} {confidence:.2f}', (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # === ส่งคำสั่งให้ Arduino เมื่อมีการเปลี่ยนแปลงสถานะการพบ "plastic" ===
    if detected_plastic and not plastic_detected:
        try:
            arduino.write(b'ON\n')
            print("[Arduino] LED ON (plastic detected)")
        except Exception as e:
            print(f"Failed to send ON to Arduino: {e}")
        plastic_detected = True

    elif not detected_plastic and plastic_detected:
        try:
            arduino.write(b'OFF\n')
            print("[Arduino] LED OFF (plastic not found)")
        except Exception as e:
            print(f"Failed to send OFF to Arduino: {e}")
        plastic_detected = False

    # แสดง FPS
    cv2.putText(frame, f'FPS: {fps:.2f}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('YOLOv8 Real-Time Detection', frame)

    # ออกจาก loop ถ้ากด 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# === ปิดกล้องและการเชื่อมต่อ ===
cap.release()
cv2.destroyAllWindows()
arduino.close()
print("Program ended and Arduino disconnected.")
