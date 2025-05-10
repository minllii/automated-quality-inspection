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



# Initialize camera

picam2 = Picamera2()

picam2.preview_configuration.main.size = (640, 480)

picam2.preview_configuration.main.format = "RGB888"

picam2.configure("preview")

picam2.start()



print("? Barcode scanner started. Press Esc to exit.")



while True:

    frame = picam2.capture_array()



    # Decode barcodes using pyzbar

    barcodes = pyzbar.decode(frame)



    for barcode in barcodes:

        barcode_data = barcode.data.decode('utf-8').strip()

        (x, y, w, h) = barcode.rect

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.putText(frame, barcode_data, (x, y - 10),

                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)



        info = find_barcode_info(barcode_data)

        if info:

            print(f"\n? Barcode Found: {barcode_data}")

            print(f"?? Details: {info}")

            with open("current_barcode.txt", "w") as f:

                f.write(barcode_data)

        else:

            print(f"\n? Barcode Not Found: {barcode_data}")



    # Display the video

    cv2.imshow("Barcode Scanner", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC key

        break



cv2.destroyAllWindows()

picam2.stop()

