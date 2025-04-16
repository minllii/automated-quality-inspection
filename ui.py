import tkinter as tk
import time

def run_ui(result_data):
    def update_ui():
        while True:
            serial_label.config(text="Serial: " + str(result_data["serial"]))
            logo_label.config(text="Logo: " + result_data["logo"])
            model_label.config(text="Model: " + result_data["model"])
            status_label.config(text="Status: " + result_data["status"])
            root.update()
            time.sleep(0.5)

    root = tk.Tk()
    root.title("Object Verification")
    root.geometry("300x200")

    serial_label = tk.Label(root, text="Serial: ")
    logo_label = tk.Label(root, text="Logo: ")
    model_label = tk.Label(root, text="Model: ")
    status_label = tk.Label(root, text="Status: ", font=("Arial", 14, "bold"))

    serial_label.pack(pady=5)
    logo_label.pack(pady=5)
    model_label.pack(pady=5)
    status_label.pack(pady=10)

    update_ui()
    root.mainloop()
