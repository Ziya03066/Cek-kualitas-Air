import streamlit as st
import pandas as pd

st.set_page_config(page_title="Kualitas Pencemaran Air", layout="centered")
st.title("💧 Aplikasi Kualitas Pencemaran Air")

st.markdown("""
Masukkan parameter kualitas air berikut.  
Tidak semua parameter harus diisi — aplikasi akan menghitung berdasarkan data yang tersedia.
""")

# Baku mutu berdasarkan PP No. 22 Tahun 2021 (Kelas II)
baku_mutu = {
    "pH_min": 6.0,
    "pH_max": 9.0,
    "Suhu_deviasi_max": 3.0,
    "DO": 4.0,
    "BOD": 3.0,
    "COD": 25.0,
    "TSS": 50.0,
    "Logam Berat": 0.03,
    "E.coli": 1000
}

with st.form("input_form"):
    ph = st.number_input("pH", min_value=0.0, step=0.1, format="%.2f")
    suhu = st.number_input("Suhu Saat Ini (°C)", min_value=0.0, step=0.1)
    suhu_alami = st.number_input("Suhu Alami Referensi (°C)", min_value=0.0, step=0.1)
    do = st.number_input("DO - Oksigen Terlarut (mg/L)", min_value=0.0, step=0.1)
    bod = st.number_input("BOD (mg/L)", min_value=0.0, step=0.1)
    cod = st.number_input("COD (mg/L)", min_value=0.0, step=0.1)
    tss = st.number_input("TSS (mg/L)", min_value=0.0, step=0.1)
    logam = st.number_input("Logam Berat (mg/L)", min_value=0.0, step=0.001)
    ecoli = st.number_input("E.coli (JPT/100mL)", min_value=0.0, step=1.0)

    submitted = st.form_submit_button("Hitung Kualitas Air")

if submitted:
    hasil = []

    def hitung_ip(nilai, baku, lebih_besar_lebih_baik=False):
        if nilai == 0:
            return None
        if lebih_besar_lebih_baik:
            return round(baku / nilai, 2) if nilai < baku else round(nilai / baku, 2)
        else:
            return round(nilai / baku, 2)

    # Hitung IP untuk setiap parameter yang diisi
    if ph > 0:
        if ph < baku_mutu["pH_min"]:
            ip_ph = round(baku_mutu["pH_min"] / ph, 2)
        elif ph > baku_mutu["pH_max"]:
            ip_ph = round(ph / baku_mutu["pH_max"], 2)
        else:
            ip_ph = 1.0
        hasil.append(("pH", ip_ph))

    if suhu > 0 and suhu_alami > 0:
        delta_suhu = abs(suhu - suhu_alami)
        ip_suhu = round(delta_suhu / baku_mutu["Suhu_deviasi_max"], 2)
        hasil.append(("Suhu", ip_suhu))

    ip_do = hitung_ip(do, baku_mutu["DO"], lebih_besar_lebih_baik=True)
    if ip_do is not None: hasil.append(("DO", ip_do))

    ip_bod = hitung_ip(bod, baku_mutu["BOD"])
    if ip_bod is not None: hasil.append(("BOD", ip_bod))

    ip_cod = hitung_ip(cod, baku_mutu["COD"])
    if ip_cod is not None: hasil.append(("COD", ip_cod))

    ip_tss = hitung_ip(tss, baku_mutu["TSS"])
    if ip_tss is not None: hasil.append(("TSS", ip_tss))

    ip_logam = hitung_ip(logam, baku_mutu["Logam Berat"])
    if ip_logam is not None: hasil.append(("Logam Berat", ip_logam))

    ip_ecoli = hitung_ip(ecoli, baku_mutu["E.coli"])
    if ip_ecoli is not None: hasil.append(("E.coli", ip_ecoli))

    if hasil:
        df = pd.DataFrame(hasil, columns=["Parameter", "Indeks Pencemar"])
        ip_max = df["Indeks Pencemar"].max()
        ip_mean = df["Indeks Pencemar"].mean()

        st.subheader("📊 Hasil Indeks Pencemar")
        st.dataframe(df, use_container_width=True)
        st.write(f"**IP Maksimum:** {ip_max}")
        st.write(f"**IP Rata-rata:** {round(ip_mean, 2)}")

        # Klasifikasi mutu air
        if ip_max <= 1:
            kategori = "BAIK (Air memenuhi baku mutu)"
        elif ip_max <= 5:
            kategori = "TERCEMAR RINGAN"
        elif ip_max <= 10:
            kategori = "TERCEMAR SEDANG"
        else:
            kategori = "TERCEMAR BERAT"

        st.success(f"🧪 Kategori Kualitas Air: **{kategori}**")
    else:
        st.warning("⚠️ Tidak ada parameter yang diisi. Masukkan minimal satu nilai untuk menghitung.")
