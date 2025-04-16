import cv2
import time

def check_logo_model():
    cap1 = cv2.VideoCapture(1)  # Kamera kedua (logo)
    cap2 = cv2.VideoCapture(2)  # Kamera ketiga (model name)

    # Dummy processing (boleh tukar dengan model AI sebenar)
    print("[INFO] Checking logo and model...")
    time.sleep(2)  # Simulasi masa inferens

    logo_ok = True    # Tukar ke keputusan sebenar dari model
    model_ok = True   # Tukar ke keputusan sebenar dari model

    cap1.release()
    cap2.release()
    return logo_ok, model_ok
