# bike-dashboard-dbs
# Bike Rental Dashboard
Dashboard ini dibuat menggunakan Streamlit untuk menganalisis data penyewaan sepeda berdasarkan waktu, cuaca, dan tipe pengguna.

## Fitur Dashboard
- Analisis pengaruh cuaca terhadap penyewaan
- Pola penyewaan berdasarkan jam (hari kerja vs hari libur)
- Pola penyewaan berdasarkan hari
- Perbandingan pengguna (casual vs registered)
- Tren penyewaan per tahun dan per bulan
- Distribusi kondisi cuaca setiap bulan

## Setup Environment (Shell / Terminal)
# 1. Buat virtual environment
python -m venv venv
# 2. Aktifkan environment
venv\Scripts\activate
# 3. Install dependencies
pip install -r requirements.txt

### Run streamlit dashboard
cd dashboard
streamlit run dashboard.py