import streamlit as st
import pandas as pd
import time
import os

st.set_page_config(page_title="Barcode Live Info", layout="centered")

st.title("📦 Sistem Semakan Barcode")

# Muatkan metadata barcode
@st.cache_data
def load_metadata():
    return pd.read_csv("barcode_metadata.csv")

metadata = load_metadata()

# Fungsi cari info barcode
def find_barcode_info(barcode_id):
    matched = metadata[metadata['barcode_id'] == barcode_id]
    if not matched.empty:
        return matched.iloc[0].to_dict()
    return None

# Fungsi baca barcode semasa
def read_current_barcode():
    if os.path.exists("current_barcode.txt"):
        with open("current_barcode.txt", "r") as f:
            return f.read().strip()
    return None

# Auto refresh setiap 2 saat
st.markdown("⏳ Auto-refresh setiap 2 saat...")
placeholder = st.empty()

while True:
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
