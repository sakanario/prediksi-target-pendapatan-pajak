import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
import joblib
from datetime import datetime,date
from dateutil.relativedelta import relativedelta

# Load the saved scaler 
scaler = joblib.load("scaler.joblib")

# Load the saved model
model = tf.saved_model.load("model_prediksi_pajak_daerah")

# define csv catcher
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

        # handle wrong shape
        row_count = df['Realisasi'].shape[0]
        if row_count != 18:
            st.error("Data yang terupload tidak berjumlah 18 data, tetapi berjumlah {} data.".format(row_count))
            return
        
        st.success("Data tervalidasi ✅")
        
        st.markdown("Pratinjau data yang terupload:")
        # st.write(df)

        st.dataframe(df, use_container_width=True)

        return df

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

# Define generate index function
def generate_date_index(start_date,n):
    dates = []
    current_date = start_date
    
    for i in range(n):
        # Add one month to the datetime object
        one_month_later = current_date + relativedelta(months=1)

        # append the increment date
        dates.append(one_month_later)

        current_date = one_month_later
    
    return dates

# Define generate chart
def render_chart(data,date_index,detail):
    y_test = [611261700050.0, 676665305325.0, 765706205267.0, 661660916600.0, 573619694300.0, 674970715650.0, 618255992000.0, 578230794800.0, 643159346150.0, 585678661150.0, 748201748860.0, 722339218550.0, 695189101250.0, 748605490450.0, 930129750700.0]

    line_chart_data = pd.DataFrame({
        'date' : date_index,
        # 'y test': y_test,
        'Prediksi': data,
    })

    line_chart_data = line_chart_data.rename(columns={'date':'index'}).set_index('index')

    st.header('Hasil Prediksi')
    st.markdown("Berikut adalah hasil prediksi untuk {} bulan dari {} sampai {}:".format(detail['n_month'],detail['first_month'],detail['last_month']))
    col1, col2 = st.columns([1,3])

    with col1:
        line_chart_data

    with col2:
        st.line_chart(line_chart_data)

    st.markdown("Berdasarkan hasil prediksi, diperkirakan total pendapatan pada {} bulan kedepan adalah sebesar Rp.{}.".format(detail['n_month'],"{:,.0f}".format(sum(data))))



# Driver Code Start

# Title
st.title('Sistem Prediksi Target Pendapatan Pajak Kendaraan Bermotor')

st.markdown("Website ini berfungsi untuk memprediksi pendapatan pajak kendaraan bermotor berdasarkan 18 data terakhir dari Realisasi Pendapatan Bulanan Pajak Kendaraan Bermotor. ")
st.markdown("Cara kerja website ini adalah dengan memasukkan 18 data terakhir dari Realisasi Pendapatan Bulanan Pajak Kendaraan Bermotor melalui mengunggah file csv. Contoh file csv dapat diunduh untuk menjadi panduan penginputan data.")
st.markdown("Silakan unggah data untuk memulai prediksi target pendapatan pajak kendaraan bermotor!")

st.divider()

st.markdown("[Contoh file csv](app/static/input_data.csv)")

# Define driver code
def app():
    df = None
    df = catch_uploaded_csv()

    # Get start_date
    start_date = st.date_input("Kapan bulan terakhir dari data yang diinputkan?", date.today())

    # get n month
    n_month = st.slider('Berapa bulan yang akan diprediksi?', 2, 24, 12)


    if st.button('Prediksi Sekarang!'):

        # handle csv not been uploaded
        if df is None:
            st.error('Silahkan upload data terlebih dahulu', icon="🚨")
            return 

        # take the realisasi row
        realisasi = np.array(df['Realisasi'])

        # reshape the data
        input_data = realisasi.reshape(1,-1)

        # scale data
        scaled_input_data = scaler.transform(np.array(input_data).reshape(-1,1))
        scaled_input_data = scaled_input_data.reshape(1,-1)

        # predicting
        predict_result = predict_for_n_month(scaled_input_data,n_month)

        # scaled back the prediction into rupiah
        predict_result_scaled_back = scaler.inverse_transform(np.array(predict_result).reshape(1,-1))

        # Generate date_index
        date_index = generate_date_index(start_date,n_month)

        detail = {
            "n_month":n_month,
            "first_month":date_index[0],
            "last_month":date_index[-1],
        }

        print(detail)

        render_chart(predict_result_scaled_back[0],date_index,detail)

# Run Driver Code
app()

