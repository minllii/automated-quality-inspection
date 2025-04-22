import streamlit as st
import pandas as pd
import os
import time
import cv2
from pyzbar.pyzbar import decode
import numpy as np

# Fail CSV untuk metadata barcode
CSV_FILE = 'barcode_metadata.csv'

# Pastikan fail CSV wujud
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=['barcode_id', 'serial_num', 'location', 'description'])
    df.to_csv(CSV_FILE, index=False)

# Fungsi untuk admin login (tanpa kata laluan, hanya memerlukan nama)
def check_username():
    """Function to check the admin login using username only"""
    username = st.text_input("Masukkan Nama Pengguna", "")
    if username:
        return username
    else:
        return None

# Fungsi untuk cari info barcode
def find_barcode_info(barcode_id):
    matched = metadata[metadata['barcode_id'] == barcode_id]
    if not matched.empty:
        return matched.iloc[0].to_dict()
    return None

# Fungsi untuk baca barcode semasa
def read_current_barcode():
    if os.path.exists("current_barcode.txt"):
        with open("current_barcode.txt", "r") as f:
            return f.read().strip()
    return None

# Admin login page (hanya nama pengguna)
username = check_username()
if not username:
    st.error("⚠️ Sila masukkan nama pengguna untuk login.")
else:
    # Admin Page: Kemas Kini Barcode
    st.title("🔧 Admin Page: Kemas Kini Barcode")

    # Papar data sedia ada
    df = pd.read_csv(CSV_FILE)
    st.subheader("📋 Data Barcode Tersedia")
    st.dataframe(df, use_container_width=True)

    # Borang tambah data baharu
    st.subheader("➕ Tambah Data Baharu")
    with st.form("barcode_form"):
        barcode_id = st.text_input("Barcode ID")
        serial_num = st.text_input("Serial Number")
        location = st.text_input("Location")
        description = st.text_input("Description")
        submitted = st.form_submit_button("Tambah")

        if submitted:
            if barcode_id and serial_num:
                new_data = pd.DataFrame([{
                    'barcode_id': barcode_id,
                    'serial_num': serial_num,
                    'location': location,
                    'description': description
                }])
                new_data.to_csv(CSV_FILE, mode='a', header=False, index=False)
                st.success("✅ Data berjaya ditambah!")
                st.rerun()
            else:
                st.warning("⚠️ Sila isi sekurang-kurangnya Barcode ID dan Serial Number.")

    # Muat turun fail CSV
    st.subheader("⬇️ Muat Turun Data")
    st.download_button("Download CSV", df.to_csv(index=False), file_name="barcodes.csv", mime="text/csv")

    # Streamlit UI untuk barcode scanner
    st.title("📦 Sistem Semakan Barcode")

    # Muatkan metadata barcode
    @st.cache_data
    def load_metadata():
        return pd.read_csv("barcode_metadata.csv")

    metadata = load_metadata()

    # Tempat untuk memaparkan hasil scan
    placeholder = st.empty()

    # Kamera setup untuk barcode scanner
    cap = cv2.VideoCapture(0)  # Gantikan dengan 1 untuk webcam lain
    stframe = st.empty()

    # Auto refresh setiap 2 saat
    st.markdown("⏳ Auto-refresh setiap 2 saat...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        for barcode in decode(frame):
            barcode_data = barcode.data.decode('utf-8')
            pts = np.array([barcode.polygon], np.int32)
            cv2.polylines(frame, [pts], True, (0,255,0), 2)
            cv2.putText(frame, barcode_data, (barcode.rect.left, barcode.rect.top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
            with open("current_barcode.txt", "w") as f:
                f.write(barcode_data)

        stframe.image(frame, channels="BGR", use_column_width=True)

        barcode = read_current_barcode()
        with placeholder.container():
            if barcode:
                st.success(f"✅ Barcode Dijumpai: `{barcode}`")
                info = find_barcode_info(barcode)
                if info:
                    st.write("📍 **Lokasi:**", info['location'])
                    st.write("🔢 **Serial Number:**", info['serial_number'])
                    st.write("📝 **Keterangan:**", info['description'])
                else:
                    st.warning("❌ Barcode tidak ada dalam dataset!")
            else:
                st.info("🔍 Sila imbas barcode...")

        time.sleep(2)  # refresh setiap 2 saat

    cap.release()
