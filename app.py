import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="yezginci - Ýstatistik Platformu", page_icon="??", layout="wide")

st.sidebar.markdown("### yezginci.streamlit.app")
ogr_no = st.sidebar.text_input("Öðrenci No", placeholder="21300215")
ders = st.sidebar.selectbox("Ders Seç", ["ÝKT203 - Pareto Analizi", "ÝKT203 - Histogram"])

if not ogr_no:
    st.title("Prof. Yezginci | Ýnteraktif Ýstatistik")
    st.info("?? Soldan öðrenci numaraný girerek kiþiye özel ödevine baþla.")
    st.stop()

seed = int(''.join(filter(str.isdigit, ogr_no))[-2:] or 15)
np.random.seed(seed)

st.title(f"Merhaba {ogr_no}")
st.caption(f"Bu veri seti {ogr_no} için özel üretildi | yezginci.streamlit.app")

kats = ["Kullanýcý Hatasý","Ýþletim Hatasý","Að Sorunu","Donaným","Diðer"]
adet = np.random.randint(25, 240, 5)
df = pd.DataFrame({"Kategori": kats, "Adet": adet}).sort_values("Adet", ascending=False)
df["Kümülatif %"] = df["Adet"].cumsum() / df["Adet"].sum() * 100

col1, col2 = st.columns(2)
col1.bar_chart(df.set_index("Kategori")["Adet"])
col2.dataframe(df, use_container_width=True)

st.divider()
st.subheader("Quiz: Kümülatif %80 kaç kategoride aþýlýyor?")
cevap = st.number_input("Cevabýn", 1, 5, 2, key="quiz")
if st.button("Gönder - Otomatik Deðerlendir"):
    dogru = int((df["Kümülatif %"] < 80).sum() + 1)
    if cevap == dogru:
        st.success(f"Doðru! 100 puan | Öðrenci: {ogr_no} | Ders: {ders} | Kaydedildi.")
        st.balloons()
    else:
        st.error(f"Yanlýþ. Doðru cevap {dogru}. Senin tablonda kümülatif: {list(round(x,1) for x in df['Kümülatif %'])}")

with st.sidebar.expander("Öðretmen Paneli"):
    sifre = st.text_input("Þifre", type="password")
    if sifre == "yezginci2024":
        st.write("Dönem Takibi (Demo)")
        st.dataframe(pd.DataFrame({"Öðrenci":[ogr_no, "21300242"], ders:[100 if 'cevap' in locals() and cevap==dogru else 80, 60]}))