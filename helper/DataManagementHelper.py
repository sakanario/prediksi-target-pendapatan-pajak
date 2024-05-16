import streamlit as st
import pandas as pd
from helper.DbHelper import insertCsvToDb

def catch_uploaded_csv():
     # Catch the file
    uploaded_file = st.file_uploader("Unggah file csv:")

    if uploaded_file is not None:

        # handle type check
        if uploaded_file.type != "text/csv":
            st.error('Mohon upload file yang ber-format .csv, file yang terupload: {}'.format(uploaded_file.type), icon="🚨")
            return

        # read file as csv
        df = pd.read_csv(uploaded_file)
        
        # Print Data Preview
        st.markdown("Pratinjau data yang terupload:")
        st.dataframe(df, use_container_width=True)
        
        # Button Upload
        if st.button('Input Data!'): 
            insertCsvToDb(df)