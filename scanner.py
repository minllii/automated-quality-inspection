import cv2, time
from pyzbar.pyzbar import decode

while True:
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if not ret:
        continue

    for barcode in decode(frame):
        barcode_data = barcode.data.decode('utf-8')
        with open("current_barcode.txt", "w") as f:
            f.write(barcode_data)
        print("📦 Barcode:", barcode_data)

    time.sleep(1)
