import streamlit as st
from helper.DataManagementHelper import catch_uploaded_csv
from helper.DataManagementHelper import generate_btn_download_sample

from helper.DbHelper import initDb, insertCsvToDb, getAllData

# Init Database 
initDb()

# Title
st.title('Data Management')

# Show Data
st.markdown("Data Realisasi yang Tersimpan di Sistem:")
t_realisasi = getAllData()
st.dataframe(t_realisasi, use_container_width=True)

# Panduan
st.markdown("Silakan unggah file data dengan [format yang telah ditentukan](app/static/input_data.csv). Setelah mengunggah file, sistem akan memeriksa setiap baris data. Jika pada file yang diunggah terdapat bulan-tahun yang sudah ada dalam sistem, maka sistem akan secara otomatis menggantikan data tersebut dengan data baru yang diunggah.")

# Download Sample
generate_btn_download_sample()

# Form Upload CSV
catch_uploaded_csv()
    
