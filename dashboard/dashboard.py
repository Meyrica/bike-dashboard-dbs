import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# baca data
df = pd.read_csv('all_data.csv')

# bersihkan kolom hasil merge
df.rename(columns={
    'cnt_x': 'cnt',
    'temp_x': 'temp',
    'hum_x': 'hum',
    'windspeed_x': 'windspeed',
    'weathersit_x': 'weathersit',
    'weekday_x': 'weekday'
}, inplace=True)

df = df.drop(columns=[col for col in df.columns if '_y' in col]) # Hapus kolom duplikat (_y)

df['dteday'] = pd.to_datetime(df['dteday']) # perbaiki tipe data

# SIDEBAR
st.sidebar.image("logo.png", width=260) # Logo diambil dari Pinterest (bukan desain sendiri)
# widget buat milih periode data yang mau dianalisis
start_date = st.sidebar.date_input("Start Date", df['dteday'].min())
end_date = st.sidebar.date_input("End Date", df['dteday'].max())

df = df[(df['dteday'] >= pd.to_datetime(start_date)) & 
        (df['dteday'] <= pd.to_datetime(end_date))]

# DASHBOARD
st.title("Bike Rental Analytics Dashboard")

st.subheader("Data Preview") # menampilkan preview data
st.write(df.head())

# PENGARUH CUACA
st.subheader("Weather Effects on Rentals")

st.write("Correlation:") # menampilkan hasil korelasi
st.write(df[['temp','hum','windspeed','cnt']].corr())

col1, col2 = st.columns(2) # bikin 2 kolom visialisasi sejajar
col3, col4 = st.columns(2)

with col1:
    st.subheader("Temperature vs Count")
    fig1, ax1 = plt.subplots()
    sns.scatterplot(x='temp', y='cnt', data=df, ax=ax1) # scatter plot karna mau lihat hubungan langsung antara 2 variabel angka
    st.pyplot(fig1)

with col2:
    st.subheader("Weather Conditions")
    fig2, ax2 = plt.subplots()
    sns.boxplot(x='weathersit', y='cnt', data=df, ax=ax2) # Boxplot karna mau lihat perbedaan distribusi jumlah penyewaan di tiap kondisi cuaca, mastiin apakah datanya konsisten atau random
    st.pyplot(fig2)

avg_hour = df.groupby('hr')['cnt'].mean()
with col3:
    st.subheader("Hourly Rentals")
    fig3, ax3 = plt.subplots()
    ax3.plot(avg_hour.index, avg_hour.values) # linechart krna mau lihat perubahan jumlah penyewaan sepanjang waktu (jam ke jam), jdi lihat grafik peningkatan dn penurunannya
    st.pyplot(fig3)

avg_day = df.groupby('weekday')['cnt'].mean()
with col4:
    st.subheader("Rental by Day")
    fig4, ax4 = plt.subplots()
    sns.barplot(x=avg_day.index, y=avg_day.values, ax=ax4) # barplot karna mau bandingin rata-rata penyewaan tiap hari, jadi kelihatan hari mana paling tinggi dan paling rendah dengan jelas
    st.pyplot(fig4)