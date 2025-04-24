import cv2
from pyzbar.pyzbar import decode
import pandas as pd
import numpy as np
import os

# Load metadata (ensure columns match!)
if not os.path.exists("barcode_metadata.csv"):
    raise FileNotFoundError("Missing barcode_metadata.csv")

metadata = pd.read_csv("barcode_metadata.csv", dtype={'barcode_id': str})

def validate_barcode(info):
    """Add rules to classify OK/NG (customize as needed)."""
    if info['country'] == 'SIRIM' and info['power'] != '220V':
        return "NG"  # Example: SIRIM requires 220V
    return "OK"

def find_barcode_info(barcode_data):
    matched = metadata[metadata['barcode_id'].str.strip() == barcode_data.strip()]
    if not matched.empty:
        info = matched.iloc[0].to_dict()
        info['status'] = validate_barcode(info)  # Add validation
        return info
    return None

# Webcam setup
cap = cv2.VideoCapture(0)
print("🔍 Scanning for barcodes... Press Esc to exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    for barcode in decode(frame):
        barcode_data = barcode.data.decode('utf-8').strip()
        pts = np.array([barcode.polygon], np.int32)
        cv2.polylines(frame, [pts], True, (0, 255, 0), 2)
        cv2.putText(frame, barcode_data, (barcode.rect.left, barcode.rect.top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        info = find_barcode_info(barcode_data)
        if info:
            print(f"\n✅ Valid Barcode: {barcode_data} (Status: {info['status']})")
            print(f"Details: {info}")
            # Write to file for Streamlit
            with open("current_barcode.txt", "w") as f:
                f.write(f"{barcode_data},{info['status']}")  # Include status
        else:
            print(f"\n❌ Invalid Barcode: {barcode_data}")

    cv2.imshow("Barcode Scanner", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # Esc key to exit
        break

cap.release()
cv2.destroyAllWindows()