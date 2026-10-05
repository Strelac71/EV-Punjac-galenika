import streamlit as st

# ==========================================
# 1. KONFIGURACIJA I ISPRAVLJENI STILOVI
# ==========================================
st.set_page_config(
    page_title="EV Punjač - Lidl Galenika",
    page_icon="⚡",
    layout="centered"
)

# Lidl Logo pretvoren u Base64 (čisti kod) da se sigurno učita bez linkova
LIDL_LOGO_BASE64 = (
    "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC"
    "9zdmciIHZpZXdCb3g9IjAgMCA0MCA0MCI+PGNpcmNsZSBjeD0iMjAiIGN5PSIyMCIgcj0iMT"
    "kuNSIgZmlsbD0iIzAwMmQ3MiIgc3Ryb2tlPSIjZmZmMjAwIi8+PHBhdGggZD0iTTkuNiAyNy"
    "40aDIuNlYxNWgtMi42em01LjQtMTIuNGgyLjd2OS44aDMuNnYyLjNoLTYuM3ptOC4zIDBoNC"
    "44YzIuNyAwIDQuNiAxLjYgNC42IDQuM3MtMS45IDQuMy00LjYgNC4zaC0yMXptMi43IDYuNW"
    "gyLjFjMS4xIDAgMi0uNyAyLTEuOHMtOS0xLjgtMi0xLjhocjIuMXptMTMuNCA1LjlsLS42LTE"
    "uN0g0Ni41bC0uNiAxLjdoLTIuN2wzLjMtOS40aDIuOGwzLjMgOS40em0tMi4yLTYuOGwtMS0"
    "zLjEtMSAzLjF6IiBmaWxsPSIjZmZmMjAwIi8+PHBhdGggZD0iTTIwIC41QzkuMi41LjUgOS4"
    "yLjUgMjBzOC43IDE5LjUgMTkuNSAxOS41UzM5LjUgMzAuOCAzOS41IDIwIDI5LjggLjUgMjA"
    "uNXptMCAzNmMtOS4xIDAtMTYuNS03LjQtMTYuNS0xNi41UzEwLjkgMy41IDIwIDMuNXMxNi4"
    "1IDcuNCAxNi41IDE2LjUtNy40IDE2LjUtMTYuNSAxNi41eiIgZmlsbD0iI2RjMzU0NSIvPjw"
    "vc3ZnPg=="
)

# Čišćenje Streamlit-ovih fabričkih okvira i fiksiranje tamne pozadine
st.markdown("""
    <style>
        /* Slanje pozadine i teksta u pravu tamnu temu */
        .stApp {
            background-color: #111214 !important;
            color: #FFFFFF !important;
        }
        
        /* Centriranje i stilizovanje logotipa */
        .logo-container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 10px;
            margin-top: -20px;
        }
        .logo-container img {
            width: 100px !important;
            height: 100px !important;
        }
        
        /* Glavni naslov ⚡ EV Punjač */
        .main-title {
            font-size: 38px !important;
            font-weight: bold !important;
            color: #FFFFFF !important;
            text-align: center;
            margin: 0px !important;
            padding: 0px !important;
        }
        
        /* Podnaslov Lidl Galenika */
        .sub-title {
            font-size: 22px !important;
            color: #A0A0A0 !important;
            text-align: center;
            margin-top: 0px !important;
            margin-bottom: 15px !important;
        }

        /* Zeleni Online bedž */
        .online-badge {
            background-color: rgba(40, 167, 69, 0.15) !important;
            color: #2cbe4e !important;
            border: 1px solid #2cbe4e !important;
            padding: 6px 18px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 16px;
            display: inline-block;
        }

        /* Fiksirani sivi kontejner oko punjača koji Streamlit neće progutati */
        .custom-charger-card {
            background-color: #1A1C1E !important;
            border: 1px solid #2D3135 !important;
            border-radius: 12px !important;
            padding: 22px !important;
            margin-top: 25px !important;
            margin-bottom: 20px !important;
        }

        /* Fleksibilni red za naslov i crveni status u istom nivou */
        .card-header-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        .charger-title {
            font-size: 25px !important;
            font-weight: bold !important;
            color: #FFFFFF !important;
        }
        .status-zauzet {
            background-color: rgba(220, 53, 69, 0.15) !important;
            color: #ff4d5a !important;
            border: 1px solid #ff4d5a !important;
            padding: 5px 12px;
            border-radius: 6px;
            font-weight: bold;
            font-size: 16px;
        }

        /* Crveni boks za napomenu */
        .alert-box {
            background-color: rgba(220, 53, 69, 0.08) !important;
            border-left: 4px solid #dc3545 !important;
            padding: 12px !important;
            border-radius: 4px !important;
            margin-top: 15px !important;
            margin-bottom: 15px !important;
            font-size: 18px !important;
        }

        /* Red sa podacima o vremenu */
        .time-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 20px !important;
            margin-top: 20px;
            margin-bottom: 15px;
        }
        .blue-text {
            color: #3894FF !important;
            font-weight: bold;
        }

        /* Plavo dugme za oslobađanje punjača */
        div.stButton > button:first-child {
            background-color: #007BFF !important;
            color: #FFFFFF !important;
            font-size: 21px !important;
            font-weight: bold !important;
            border: 1px solid #0056b3 !important;
            border-radius: 8px !important;
            width: 100% !important;
            padding: 12px !important;
            transition: 0.2s;
        }
        div.stButton > button:first-child:hover {
            background-color: #0056b3 !important;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. PRIKAZ ELEMENATA (HTML Struktura)
# ==========================================

# Direktno ubacivanje ugrađenog Lidl logotipa na vrh ekrana
st.markdown(f'<div class="logo-container"><img src="{LIDL_LOGO_BASE64}"></div>', unsafe_allow_html=True)

# Naslovi
st.markdown('<p class="main-title">⚡ EV Punjač</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Lidl Galenika</p>', unsafe_allow_html=True)

# Online status centrirano
st.markdown('<div style="text-align: center; margin-bottom: 10px;"><span class="online-badge">✓ Online</span></div>', unsafe_allow_html=True)

# POČETAK GLAVNOG SIVOG KONTEJNERA (KARTICE)
st.markdown('<div class="custom-charger-card">', unsafe_allow_html=True)

# Gornji red unutar kartice: Naslov i status Zauzet
st.markdown(f"""
<div class="card-header-row">
    <span class="charger-title">EV Punjač Lidl Galenika</span>
    <span class="status-zauzet">Zauzet (Tab)</span>
</div>
""", unsafe_allow_html=True)

# Lokacija i jačina (Standardni Streamlit markdown unutar kartice)
st.markdown("📍 **Galenika, Zemun** &nbsp;&nbsp;&nbsp;&nbsp; 🔋 **22kW**")

# Crvena kutija sa napomenom
st.markdown("""
<div class="alert-box">
    ⚠️ <b>NAPOMENA:</b> Koristite max 1 sat (limit punjenja). Budimo kolegijalni!
</div>
""", unsafe_allow_html=True)

# Red za vreme punjenja i satnicu
st.markdown("""
<div class="time-row">
    <span>📋 <span class="blue-text">Tab</span> puni već <span class="blue-text">4 min</span></span>
    <span style="color: #70757A;">od 14:49h</span>
</div>
""", unsafe_allow_html=True)

# Streamlit dugme koje se nalazi unutar sivog okvira kartice
if st.button("Završi punjenje (Oslobodi punjač)"):
    st.success("Punjač je uspešno oslobođen!")

st.markdown('</div>', unsafe_allow_html=True) # KRAJ GLAVNOG KONTEJNERA


# Ostatak elemenata ispod kartice (Lista čekanja i unos)
st.markdown('<div style="font-size: 24px; font-weight: bold; margin-top: 25px;">📋 Lista čekanja <span style="float: right; background-color: #2D3135; color: #3894FF; padding: 2px 10px; border-radius: 12px; font-size: 16px;">0</span></div>', unsafe_allow_html=True)
st.markdown('<p style="color: #70757A; text-align: center; font-size: 18px; margin-top: 15px;">Nema ljudi u redu</p>', unsafe_allow_html=True)

ime = st.text_input(label="", placeholder="Ukucaj ime za red ili brisanje...")
