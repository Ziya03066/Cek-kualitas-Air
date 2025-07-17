import streamlit as st
import pandas as pd

st.set_page_config(page_title="Indeks Pencemaran Air", layout="centered")
st.title("💧 Aplikasi Indeks Pencemaran Air")

st.markdown("""
Masukkan parameter kualitas air berdasarkan hasil pengukuran lapangan. 
Perhitungan menggunakan metode **Indeks Pencemar (IP max)** berdasarkan baku mutu Kelas II (PP No. 22 Tahun 2021).
""")

# Baku mutu acuan (kelas II)
baku_mutu = {
    "pH_min": 6.0,
    "pH_max": 9.0,
    "Suhu_deviasi_max": 3.0,  # deviasi dari suhu alami
    "DO": 4.0,
    "BOD": 3.0,
    "COD": 25.0,
    "TSS": 50.0,
    "Logam Berat": 0.03,  # misal total logam berat (Pb atau Hg)
    "E.coli": 1000  # JPT/100mL
}

with st.form("input_form"):
    ph = st.number_input("pH", min_value=0.0, step=0.1)
    suhu = st.number_input("Suhu Air Saat Ini (°C)", min_value=0.0, step=0.1)
    suhu_alami = st.number_input("Suhu Alami Referensi (°C)", min_value=0.0, step=0.1)
    do = st.number_input("Oksigen Terlarut / DO (mg/L)", min_value=0.0, step=0.1)
    bod = st.number_input("BOD (mg/L)", min_value=0.0, step=0.1)
    cod = st.number_input("COD (mg/L)", min_value=0.0, step=0.1)
    tss = st.number_input("TSS (mg/L)", min_value=0.0, step=0.1)
    logam = st.number_input("Logam Berat (mg/L)", min_value=0.0, step=0.001)
    ecoli = st.number_input("E.coli (JPT/100 mL)", min_value=0.0, step=1.0)
    submit = st.form_submit_button("Hitung Indeks Pencemar")

if submit:
    hasil = []

    # Fungsi IP
    def hitung_ip(c_aktual, c_baku, lebih_besar_lebih_baik=False):
        if lebih_besar_lebih_baik:
            if c_aktual >= c_baku:
                return round(c_aktual / c_baku, 2)
            else:
                return round(c_baku / c_aktual, 2)
        else:
            return round(c_aktual / c_baku, 2)

    # pH
    ip_ph = 0
    if ph < baku_mutu["pH_min"]:
        ip_ph = round(baku_mutu["pH_min"] / ph, 2)
    elif ph > baku_mutu["pH_max"]:
        ip_ph = round(ph / baku_mutu["pH_max"], 2)
    hasil.append(("pH", ip_ph))

    # Suhu
    delta_suhu = abs(suhu - suhu_alami)
    ip_suhu = round(delta_suhu / baku_mutu["Suhu_deviasi_max"], 2)
    hasil.append(("Suhu", ip_suhu))

    # DO (semakin tinggi semakin baik)
    ip_do = hitung_ip(do, baku_mutu["DO"], lebih_besar_lebih_baik=True)
    hasil.append(("DO", ip_do))

    # Parameter lainnya
    hasil.append(("BOD", hitung_ip(bod, baku_mutu["BOD"])))
    hasil.append(("COD", hitung_ip(cod, baku_mutu["COD"])))
    hasil.append(("TSS", hitung_ip(tss, baku_mutu["TSS"])))
    hasil.append(("Logam Berat", hitung_ip(logam, baku_mutu["Logam Berat"])))
    hasil.append(("E.coli", hitung_ip(ecoli, baku_mutu["E.coli"])))

    # Tabel hasil
    df = pd.DataFrame(hasil, columns=["Parameter", "Indeks Pencemar"])
    ip_max = df["Indeks Pencemar"].max()
    ip_rata2 = df["Indeks Pencemar"].mean()

    st.subheader("📊 Hasil Perhitungan")
    st.dataframe(df, use_container_width=True)
    st.write(f"**IP Maksimum:** {ip_max}")
    st.write(f"**IP Rata-rata:** {round(ip_rata2, 2)}")

    # Klasifikasi mutu air
    if ip_max <= 1:
        mutu = "BAIK (Kelas A)"
    elif ip_max <= 5:
        mutu = "TERCEMAR RINGAN"
    elif ip_max <= 10:
        mutu = "TERCEMAR SEDANG"
    else:
        mutu = "TERCEMAR BERAT"

    st.success(f"🧪 Kualitas Air: **{mutu}**")
