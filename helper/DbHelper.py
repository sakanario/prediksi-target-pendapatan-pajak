import streamlit as st

conn = st.connection('data_db', type='sql')

def initDb():
    with conn.session as s:
        s.execute('CREATE TABLE IF NOT EXISTS t_realisasi (date TEXT UNIQUE, realisasi REAL);')
        s.close()

def insertCsvToDb(df):
    with conn.session as s:
        # Iterasi DataFrame dan insert ke database
        for index, row in df.iterrows():
            realisasi = row['realisasi']  # int
            tanggal = row['bulan-tahun']  # str
            
            # Lakukan insert dengan parameterized query
            s.execute(
                'INSERT OR REPLACE INTO t_realisasi (realisasi, date) VALUES (:realisasi, :tanggal);',
                params=dict(realisasi=realisasi, tanggal=tanggal)
            )

        # Menyimpan perubahan dan menutup koneksi
        s.commit()
        s.close()
        
def getAllData():
    return conn.query('select * from t_realisasi')