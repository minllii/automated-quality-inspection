from picamera2 import Picamera2

import cv2
from pyzbar import pyzbar
import pandas as pd

import numpy as np

import os

# Load metadata
if not os.path.exists("barcode_metadata.csv"):

    raise FileNotFoundError("Missing barcode_metadata.csv")



metadata = pd.read_csv("barcode_metadata.csv", dtype={'barcode_id': str})

def find_barcode_info(barcode_data):

    matched = metadata[metadata['barcode_id'].str.strip() == barcode_data.strip()]

    if not matched.empty:
        return matched.iloc[0].to_dict()
    return None

cap = cv2.VideoCapture("libcamerasrc ! videoconvert ! appsink", cv2.CAP_GSTREAMER)
print("🔍 Scanning for barcodes... Press Esc to exit.")

# Create a barcode detector using OpenCV
barcode_detector = cv2.barcode_BarcodeDetector()

while True:

    # Detect barcodes in the frame
    retval, decoded_info, points, straight_qrcode = barcode_detector.detectAndDecodeMulti(frame)
    
    if retval:
        for i, barcode_data in enumerate(decoded_info):
            barcode_data = barcode_data.strip()
            pts = np.array([points[i]], np.int32)
            cv2.polylines(frame, [pts], True, (0, 255, 0), 2)
            cv2.putText(frame, barcode_data, (points[i][0][0], points[i][0][1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Find matching barcode info
            info = find_barcode_info(barcode_data)
            if info:
                print(f"\n✅ Barcode Found: {barcode_data}")
                print(f"Details: {info}")
                with open("current_barcode.txt", "w") as f:
                    f.write(barcode_data)
            else:
                print(f"\n❌ Barcode Not Found: {barcode_data}")

    cv2.imshow("Barcode Scanner", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
