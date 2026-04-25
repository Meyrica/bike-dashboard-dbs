import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# DASHBOARD
st.title("Dasbor Analisis Penyewaan Sepeda")

# baca data
df = pd.read_csv('dashboard/all_data.csv')
df = pd.read_csv('all_data.csv')

df = df.rename(columns={
    'weathersit_x': 'weathersit',
    'cnt_x': 'cnt',
    'casual_x': 'casual',
    'registered_x': 'registered',
    'mnth_x': 'mnth',
    'yr_x': 'yr',
    'weekday_x': 'weekday',
    'workingday_x': 'workingday'
})

# SIDEBAR
st.sidebar.image("dashboard/logo.png", width=260) # Logo diambil dari Pinterest (bukan desain sendiri)
st.sidebar.image("logo.png", width=260) # Logo diambil dari Pinterest (bukan desain sendiri)

# widget buat milih periode data yang mau dianalisis
start_date = st.sidebar.date_input("Start Date", df['dteday'].min())
end_date = st.sidebar.date_input("End Date", df['dteday'].max())

# Labeling
weather_labels = {
    1: "Cerah",
    2: "Berkabut",
    3: "Hujan",
}
df['weather_label'] = df['weathersit'].map(weather_labels)

day_labels = {
    0: 'Minggu', 1: 'Senin', 2: 'Selasa',
    3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'
}
df['weekday_label'] = df['weekday'].map(day_labels)

month_labels = {
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr',
    5: 'Mei', 6: 'Jun', 7: 'Jul', 8: 'Agu',
    9: 'Sep', 10: 'Okt', 11: 'Nov', 12: 'Des'
}
df['month_name'] = df['mnth'].map(month_labels)

df['year'] = df['yr'].map({0: '2011', 1: '2012'})

df['day_type'] = df['workingday'].map({
    0: 'Hari Libur',
    1: 'Hari Kerja'
})

col1, col2 = st.columns(2) # Visualisasinya biar rapih sejajar
col3, col4 = st.columns(2)
col5, col6 = st.columns(2)

with col1:
    st.subheader("Pengaruh Cuaca pada Penyewaan")
    avg_weather = df.groupby('weather_label')['cnt'].mean().reset_index()
    fig1, ax1 = plt.subplots()
    sns.barplot(x='weather_label', y='cnt', data=avg_weather, ax=ax1)
    ax1.set_title('Rata-rata Penyewaan Berdasarkan Cuaca')
    ax1.set_xlabel("Cuaca")
    ax1.set_ylabel("Jumlah Penyewaan")      
    st.pyplot(fig1)

with col2:
    st.subheader("Pola Penyewaan per Jam")
    avg_hour = df.groupby(['hr', 'day_type'])['cnt'].mean().reset_index()
    fig2, ax2 = plt.subplots()
    sns.lineplot(data=avg_hour, x='hr', y='cnt', hue='day_type', ax=ax2)
    ax2.set_title('Penyewaan per Jam')
    ax2.set_xlabel("Jam")
    ax2.set_ylabel("Rata-rata Penyewaan")
    ax2.legend(title="Tipe Hari")  
    
    st.pyplot(fig2)

with col3:
    st.subheader("Pola Penyewaan per Hari")
    avg_day = df.groupby('weekday_label')['cnt'].mean().reset_index()
    fig3, ax3 = plt.subplots()
    sns.barplot(x='weekday_label', y='cnt', data=avg_day, ax=ax3)
    ax3.set_title('Rata-rata Penyewaan per Hari')
    ax3.set_xlabel("Hari")
    ax3.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig3)

with col4:
    st.subheader("Perbandingan Pengguna")
    avg_users = df[['casual','registered']].mean()
    fig4, ax4 = plt.subplots()
    sns.barplot(x=avg_day.index, y=avg_day.values, ax=ax4) # barplot karna mau bandingin rata-rata penyewaan tiap hari, jadi kelihatan hari mana paling tinggi dan paling rendah dengan jelas
    st.pyplot(fig4)
    avg_users.plot(kind='bar', ax=ax4)
    ax4.set_title('Casual vs Registered')
    ax4.set_xlabel("Jenis Pengguna")
    ax4.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig4)

with col5:
    st.subheader("Penyewaan per Tahun")
    yearly_total = df.groupby('year')['cnt'].sum().reset_index()
    fig5, ax5 = plt.subplots()
    sns.barplot(data=yearly_total, x='year', y='cnt', ax=ax5)
    ax5.set_title('Total Penyewaan per Tahun')
    ax5.set_xlabel("Tahun")
    ax5.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig5)

with col6:
    st.subheader("Penyewaan per Bulan")
    monthly_avg = df.groupby('month_name')['cnt'].mean().reset_index()
    fig6, ax6 = plt.subplots()
    sns.barplot(data=monthly_avg, x='month_name', y='cnt', ax=ax6)
    ax6.set_title('Rata-rata Penyewaan per Bulan')
    ax6.set_xlabel("Bulan")
    ax6.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig6)

# 7. CUACA PER BULAN
st.subheader("Distribusi Cuaca per Bulan")
weather_month = df.groupby(['month_name', 'weather_label']).size().reset_index(name='jumlah')
fig7, ax7 = plt.subplots(figsize=(10,5))
sns.barplot(data=weather_month, x='month_name', y='jumlah', hue='weather_label', ax=ax7)
ax7.set_title('Kondisi Cuaca di Setiap Bulan')
ax7.set_xlabel("Bulan")
ax7.set_ylabel("Jumlah Hari")
ax7.legend(title="Cuaca") 
st.pyplot(fig7)
