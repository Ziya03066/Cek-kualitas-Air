import streamlit as st
import pandas as pd

st.set_page_config(page_title="Indeks Pencemaran Air", layout="centered")

st.title("💧 Aplikasi Indeks Pencemaran Air")
st.markdown("Masukkan parameter kualitas air untuk menghitung Indeks Pencemar (IP).")

# Baku mutu (misal: kelas 2 - Peraturan Pemerintah No. 22 Tahun 2021)
standar = {
    "pH_min": 6.0,
    "pH_max": 9.0,
    "Suhu_max_deviasi": 3.0,  # deviasi terhadap suhu alami
    "BOC": 3.0,
    "COD": 25.0,
    "TSS": 50.0
}

with st.form("form_input"):
    ph = st.number_input("pH", min_value=0.0, step=0.1)
    suhu = st.number_input("Suhu (°C)", min_value=0.0, step=0.1)
    suhu_alami = st.number_input("Suhu Air Alami (°C)", min_value=0.0, step=0.1, help="Masukkan suhu referensi dari lingkungan alami")
    boc = st.number_input("BOC (mg/L)", min_value=0.0, step=0.1)
    cod = st.number_input("COD (mg/L)", min_value=0.0, step=0.1)
    tss = st.number_input("TSS (mg/L)", min_value=0.0, step=0.1)
    submit = st.form_submit_button("Hitung Indeks Pencemar")

if submit:
    hasil = []

    # Fungsi IP umum
    def ip(c_aktual, c_baku, lebih_besar_lebih_baik=False):
        if lebih_besar_lebih_baik:
            if c_aktual >= c_baku:
                return round(c_aktual / c_baku, 2)
            else:
                return round(c_baku / c_aktual, 2)
        else:
            return round(c_aktual / c_baku, 2)

    # pH
    ip_ph = 0
    if ph < standar["pH_min"]:
        ip_ph = round(standar["pH_min"] / ph, 2)
    elif ph > standar["pH_max"]:
        ip_ph = round(ph / standar["pH_max"], 2)
    hasil.append(("pH", ip_ph))

    # Suhu: deviasi dari suhu alami
    delta_suhu = abs(suhu - suhu_alami)
    ip_suhu = round(delta_suhu / standar["Suhu_max_deviasi"], 2)
    hasil.append(("Suhu", ip_suhu))

    # BOC, COD, TSS
    hasil.append(("BOC", ip(boc, standar["BOC"])))
    hasil.append(("COD", ip(cod, standar["COD"])))
    hasil.append(("TSS", ip(tss, standar["TSS"])))

    df = pd.DataFrame(hasil, columns=["Parameter", "Indeks Pencemar"])
    ip_max = df["Indeks Pencemar"].max()
    ip_rata2 = df["Indeks Pencemar"].mean()

    st.subheader("📊 Hasil Perhitungan")
    st.dataframe(df, use_container_width=True)
    st.write(f"**IP Maksimum:** {ip_max}")
    st.write(f"**IP Rata-rata:** {round(ip_rata2, 2)}")

    # Kategori mutu berdasarkan IP max
    if ip_max <= 1:
        mutu = "BAIK (Kelas A)"
    elif ip_max <= 5:
        mutu = "TERCEMAR RINGAN"
    elif ip_max <= 10:
        mutu = "TERCEMAR SEDANG"
    else:
        mutu = "TERCEMAR BERAT"

    st.success(f"🧪 Kualitas Air: **{mutu}**")
