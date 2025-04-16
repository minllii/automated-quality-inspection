import threading
from barcode_scanner import get_serial_number
from logo_model_checker import check_logo_model
from ui import run_ui

result_data = {
    "serial": None,
    "logo": "Checking...",
    "model": "Checking...",
    "status": "Pending"
}

def process_barcode():
    serial = get_serial_number()
    result_data["serial"] = serial

def process_logo_model():
    logo_ok, model_ok = check_logo_model()
    result_data["logo"] = "OK" if logo_ok else "FAIL"
    result_data["model"] = "OK" if model_ok else "FAIL"
    if logo_ok and model_ok:
        result_data["status"] = "PASS"
    else:
        result_data["status"] = "FAIL"

if __name__ == "__main__":
    # Start barcode and logo detection in parallel
    t1 = threading.Thread(target=process_barcode)
    t2 = threading.Thread(target=process_logo_model)

    t1.start()
    t2.start()

    # Run UI (blocking)
    run_ui(result_data)

    t1.join()
    t2.join()
