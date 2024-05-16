import streamlit as st
from helper.DbHelper import getAllData
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
import joblib
import tensorflow as tf



# Load the saved scaler 
scaler = joblib.load("scaler.joblib")

# Load the saved model
model = tf.saved_model.load("model_prediksi_pajak_daerah")

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

def generateModelInputDataframe(start_date):
    # generate date index mundur kebelakang sebanyak 18 bulan
    date_index=generate_backward_date_index(start_date,18)
    
    # convert date_index menjadi list of string
    formated_date_index = convertDateIndexToFormatedString(date_index)
    
    # Filter DataFrame berdasarkan list bulan-tahun
    filtered_df = df[df['date'].isin(formated_date_index)]
    
    return filtered_df

# Define Predict Function
def predict_for_n_month(data,n):
    input_data = tf.constant(data, dtype=tf.float32)  # Convert to tf.float32 tensor
    predict_result = []

    for i in range(n):
        # do prediction
        prediction = model(input_data)

        # append the prediction into predict result
        predict_result.append(prediction[0][0].numpy())  # Convert back to NumPy array

        # remove the first element on the input and append prediction to the end
        input_data = tf.concat([input_data[:, 1:], prediction], axis=1)

    return predict_result
        
        
df = getAllData()

st.title('Sistem Prediksi Target Pendapatan Pajak Kendaraan Bermotor')
st.subheader("Realisasi Pendapatan Pajak Kendaraan Bermotor")
generate_all_data_chart(df)

        
# Get start_date
start_date = st.date_input("Pilih tanggal yang Ingin digunakan sebagai Acuan Prediksi",datetime.strptime("1-2022", "%m-%Y"))

n_month = st.slider('Berapa bulan yang akan diprediksi?', 2, 24, 12)

if st.button('Prediksi Sekarang!'):
    model_input_df = generateModelInputDataframe(start_date)
    model_input_df
    
     # take the realisasi row
    realisasi = np.array(model_input_df['realisasi'])
    realisasi
    
    # reshape the data
    input_data = realisasi.reshape(1,-1)

    # scale data
    scaled_input_data = scaler.transform(np.array(input_data).reshape(-1,1))
    scaled_input_data = scaled_input_data.reshape(1,-1)

    # predicting
    predict_result = predict_for_n_month(scaled_input_data,n_month)

    # scaled back the prediction into rupiah
    predict_result_scaled_back = scaler.inverse_transform(np.array(predict_result).reshape(1,-1))
    predict_result_scaled_back[0]
    
    # Generate date_index
    date_index = generate_date_index(start_date,len(predict_result_scaled_back[0]))
    date_index
    
    render_chart(predict_result_scaled_back[0],date_index)
    


    









