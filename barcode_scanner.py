import cv2
from pyzbar.pyzbar import decode
import pandas as pd
import numpy as np

metadata = pd.read_csv("barcode_metadata.csv", dtype={'barcode_id': str})

def find_barcode_info(barcode_data):
    matched = metadata[metadata['barcode_id'] .str.strip() == barcode_data.strip()]
    if not matched.empty:
        return matched.iloc[0].to_dict()
    return None

cap = cv2.VideoCapture(0)
print("🔍 Sila imbas barcode... Tekan Esc untuk keluar.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    for barcode in decode(frame):
        barcode_data = barcode.data.decode('utf-8').strip()
        pts = np.array([barcode.polygon], np.int32)
        cv2.polylines(frame, [pts], True, (0,255,0), 2)
        cv2.putText(frame, barcode_data, (barcode.rect.left, barcode.rect.top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

        print("🔍 Data dari kamera:", barcode_data)
        # Cari maklumat barcode dalam dataset
        info = find_barcode_info(barcode_data)

        if info:
            print("\n✅ Barcode Dijumpai:", barcode_data)
            print("📍 Lokasi:", info['location'])
            print("🔢 Serial:", info['serial_number'])
            print("📝 Info:", info['description'])

            # Tulis barcode ke fail untuk Streamlit baca
            with open("current_barcode.txt", "w") as f:
             f.write(barcode_data)

        else:
            print("\n❌ Barcode tidak dijumpai dalam dataset:", barcode_data)

    cv2.imshow("Barcode Scanner", frame)
    if cv2.waitKey(1) & 0xFF == 27: # Esc key to exit       
        break

cap.release()
cv2.destroyAllWindows()