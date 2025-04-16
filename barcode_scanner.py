import cv2
from pyzbar.pyzbar import decode

def get_serial_number():
    cap = cv2.VideoCapture(0)  # Kamera pertama
    serial_number = None
    print("[INFO] Scanning barcode...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        barcodes = decode(frame)
        for barcode in barcodes:
            serial_number = barcode.data.decode('utf-8')
            print("Detected Serial:", serial_number)
            cap.release()
            return serial_number

        cv2.imshow("Barcode Scanner", frame)
        if cv2.waitKey(1) == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return serial_number
