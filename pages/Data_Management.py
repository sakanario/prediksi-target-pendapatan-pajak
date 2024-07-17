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
st.subheader("Panduan untuk Menginput Data via Upload CSV")
st.markdown("1. Unduh Template CSV: Mulailah dengan mengunduh template unggah file data yang telah disediakan oleh sistem. Template ini memastikan format data sesuai dengan yang dibutuhkan." )
st.markdown("2. Buka Template: Gunakan aplikasi spreadsheet seperti Microsoft Excel, Google Sheets, atau editor teks seperti Notepad untuk membuka file template CSV yang telah diunduh.")
st.markdown("3. Masukkan Data")
st.markdown("- Kolom bulan-tahun: Masukkan data dengan format mm-YYYY. Contoh: 01-2013.")
st.markdown("- Kolom realisasi: Masukkan data dalam format angka tanpa tanda baca. Contoh: 345190762550.")
st.code("# Contoh data dalam file csv\nbulan-tahun,realisasi\n01-2013,345190762550\n02-2013,123456789012\n03-2013,987654321098\n04-2013,234567890123")
st.markdown("4. Unggah File")
st.markdown("- Akses Form Unggah: Kembali ke sistem atau aplikasi dan buka form unggah yang telah disediakan.")
st.markdown("- Pilih File CSV: Klik tombol untuk memilih file dari komputer Anda, lalu pilih file CSV yang telah diedit.")
st.markdown("- Unggah File: Klik tombol unggah untuk memulai proses unggah file ke sistem.")
st.markdown("- Jika pada file yang diunggah terdapat bulan-tahun yang sudah ada dalam sistem, maka sistem akan secara otomatis menggantikan data tersebut dengan data baru yang diunggah.")

# Download Sample
generate_btn_download_sample()


# Form Upload CSV
catch_uploaded_csv()
    
