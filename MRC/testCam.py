import cv2

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("เปิดกล้องไม่สำเร็จ 😢")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow('Camera Test', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
