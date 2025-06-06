import cv2
from pyzbar.pyzbar import decode

def real_time_barcode_scanner():
    # เปิดกล้องเว็บแคม (0 = Default Camera)
    cap = cv2.VideoCapture(0)

    # ตรวจสอบว่ากล้องเปิดได้หรือไม่
    if not cap.isOpened():
        print("ไม่สามารถเปิดกล้องได้")
        return

    print("เริ่มการสแกนบาร์โค้ด (กด 'q' เพื่อออก)")

    while True:
        # อ่านเฟรมจากกล้อง
        ret, frame = cap.read()
        if not ret:
            break

        # ถอดรหัสบาร์โค้ดจากเฟรม
        barcodes = decode(frame)

        for barcode in barcodes:
            # ดึงตำแหน่งกรอบสี่เหลี่ยม
            (x, y, w, h) = barcode.rect

            # วาดกรอบสี่เหลี่ยมรอบบาร์โค้ด
            cv2.rectangle(frame, (x - 10, y - 10), 
                          (x + w + 10, y + h + 10), 
                          (0, 255, 0), 2)

            # ถอดรหัสข้อมูลบาร์โค้ด
            barcode_data = barcode.data.decode("utf-8")
            barcode_type = barcode.type

            # พิมพ์ข้อมูลบาร์โค้ดลงใน Console
            print(f"Data: {barcode_data} | Type: {barcode_type}")

            # แสดงข้อมูลบนภาพ
            text = f"{barcode_data} ({barcode_type})"
            cv2.putText(frame, text, (x, y - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # แสดงผลเฟรม
        cv2.imshow("Real-Time Barcode Scanner", frame)

        # กด 'q' เพื่อออกจากการสแกน
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # ปิดกล้องและหน้าต่างทั้งหมด
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    real_time_barcode_scanner()
