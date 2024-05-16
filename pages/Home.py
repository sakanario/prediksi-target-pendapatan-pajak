import streamlit as st
from helper.DbHelper import getAllData
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import pandas as pd

# Define generate index function
def generate_backward_date_index(start_date,n):
    dates = []
    current_date = start_date
    
    for i in range(n):
        # Add one month to the datetime object
        one_month_before = current_date - relativedelta(months=1)

        # append the increment date
        dates.append(one_month_before)

        current_date = one_month_before
    
    return sorted(dates)

def convertDateIndexToFormatedString(dateIndex):
    result = []
    for item in dateIndex:
        result.append(item.strftime("%m-%Y"))
    return result

# Define generate index function
def generate_date_index(start_date,n):
    dates = []
    current_date = start_date
    
    for i in range(n):
        dates.append(current_date)
         
        # Add one month to the datetime object
        current_date = current_date + relativedelta(months=1)
    
    return dates

# Define generate chart
def render_chart(data,date_index):

    line_chart_data = pd.DataFrame({    
        'date' : date_index,
        'Prediksi': data,
    })

    line_chart_data = line_chart_data.rename(columns={'date':'index'}).set_index('index')

    st.line_chart(line_chart_data, use_container_width=True)
    
def generate_all_data_chart(df):
    dates_string = df['date']
    dates_datetime = pd.to_datetime(dates_string, format='%m-%Y')
    min_date = dates_datetime.min()
    date_index = generate_date_index(min_date,len(df))

    render_chart(df['realisasi'],date_index)
        
        
df = getAllData()

st.title('Sistem Prediksi Target Pendapatan Pajak Kendaraan Bermotor')
st.subheader("Realisasi Pendapatan Pajak Kendaraan Bermotor")
generate_all_data_chart(df)




 
        
        
        
        
# Get start_date
# start_date = st.date_input("Pilih tanggal yang Ingin digunakan sebagai Acuan Prediksi",datetime.strptime("12-2020", "%m-%Y"))

# dateIndex=generate_backward_date_index(start_date,3)

# dateIndex

# formatedDateIndex = convertDateIndexToFormatedString(dateIndex)
# formatedDateIndex

# df = getAllData()
# df

# # Filter DataFrame berdasarkan list bulan-tahun
# filtered_df = df[df['date'].isin(formatedDateIndex)]
# filtered_df



