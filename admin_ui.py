import streamlit as st
import pandas as pd
import os

CSV_FILE = 'barcode_metadata.csv'

# Pastikan fail CSV wujud
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=['barcode_id', 'serial_num', 'location', 'description'])
    df.to_csv(CSV_FILE, index=False)

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
