import streamlit as st
from datetime import datetime

# ==========================================
# 1. KONFIGURACIJA I STILIZACIJA STRANICE
# ==========================================
st.set_page_config(
    page_title="EV Punjač - Lidl Galenika",
    page_icon="⚡",
    layout="centered"
)

# CSS za tamnu temu, Lidl logo i povećana slova (identično kao na slici)
st.markdown("""
    <style>
        /* Pozadina aplikacije i fontovi */
        .stApp {
            background-color: #111214;
            color: #FFFFFF;
        }
        
        /* Glavni naslov ⚡ EV Punjač */
        .main-title {
            font-size: 38px !important;
            font-weight: bold !important;
            color: #FFFFFF !important;
            text-align: center;
            margin-top: -10px;
            margin-bottom: 2px;
        }
        
        /* Podnaslov Lidl Galenika */
        .sub-title {
            font-size: 22px !important;
            color: #A0A0A0 !important;
            text-align: center;
            margin-bottom: 15px;
        }

        /* Zeleni Online bedž */
        .online-badge {
            background-color: rgba(40, 167, 69, 0.2);
            color: #28a745;
            border: 1px solid #28a745;
            padding: 4px 15px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 16px;
            display: inline-block;
            margin-bottom: 25px;
        }

        /* Glavni kontejner oko punjača */
        .charger-box {
            background-color: #1A1C1E;
            border: 1px solid #2D3135;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        }

        /* Naslov unutar kutije */
        .charger-header {
            font-size: 26px !important;
            font-weight: bold !important;
            color: #FFFFFF !important;
        }

        /* Crveni status bedž "Zauzet (Tab)" */
        .status-badge {
            background-color: rgba(220, 53, 69, 0.15);
            color: #dc3545;
            border: 1px solid #dc3545;
            padding: 4px 12px;
            border-radius: 6px;
            font-weight: bold;
            font-size: 16px;
            float: right;
        }

        /* Crvena napomena sekcija */
        .alert-box {
            background-color: rgba(220, 53, 69, 0.08);
            border-left: 4px solid #dc3545;
            padding: 12px;
            border-radius: 4px;
            margin-top: 15px;
            font-size: 18px !important;
        }

        /* Tekst "Tab puni već 4 min" */
        .timer-text {
            font-size: 20px !important;
            color: #FFFFFF;
            margin-top: 15px;
            margin-bottom: 15px;
        }
        .timer-highlight {
            color: #3894FF;
            font-weight: bold;
        }

        /* Plavo glavno dugme */
        div.stButton > button:first-child {
            background-color: #007BFF !important;
            color: #FFFFFF !important;
            font-size: 22px !important;
            font-weight: bold !important;
            border: 1px solid #0056b3 !important;
            border-radius: 8px !important;
            width: 100% !important;
            padding: 12px !important;
            margin-top: 10px;
            transition: 0.3s;
        }
        div.stButton > button:first-child:hover {
            background-color: #0056b3 !important;
            border-color: #004085 !important;
        }

        /* Sekcija Lista čekanja */
        .queue-header {
            font-size: 24px !important;
            font-weight: bold !important;
            margin-top: 25px;
            margin-bottom: 15px;
        }
        .queue-count {
            background-color: #2D3135;
            color: #3894FF;
            padding: 2px 10px;
            border-radius: 12px;
            font-size: 16px;
            float: right;
        }
        .empty-queue {
            color: #70757A;
            text-align: center;
            font-size: 18px;
            margin-top: 10px;
            margin-bottom: 20px;
        }

        /* Stil za input polje */
        .stTextInput input {
            background-color: #1A1C1E !important;
            color: #FFFFFF !important;
            border: 1px solid #2D3135 !important;
            font-size: 18px !important;
            padding: 10px !important;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. STRUKTURA I VIZUELNI ELEMENTI (Sa slike)
# ==========================================

# Centrirani Lidl Logo na samom vrhu
col1, col2, col3 = st.columns([1, 0.6, 1])
with col2:
    st.image("https://wikimedia.org", use_container_width=True)

# Glavni naslovi i online status
st.markdown('<p class="main-title">⚡ EV Punjač</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Lidl Galenika</p>', unsafe_allow_html=True)

st.markdown('<div style="text-align: center;"><span class="online-badge">✓ Online</span></div>', unsafe_allow_html=True)

# GLAVNI KONTEJNER PUNJAČA
st.markdown('<div class="charger-box">', unsafe_allow_html=True)

# Zaglavlje punjača sa crvenim statusom desno
col_left, col_right = st.columns([2, 1])
with col_left:
    st.markdown('<span class="charger-header">EV Punjač Lidl Galenika</span>', unsafe_allow_html=True)
with col_right:
    st.markdown('<span class="status-badge">Zauzet (Tab)</span>', unsafe_allow_html=True)

# Lokacija i jačina punjača
st.write("")
st.markdown("📍 **Galenika, Zemun** &nbsp;&nbsp;&nbsp;&nbsp; 🔋 **22kW**")

# Crvena napomena u okviru
st.markdown("""
<div class="alert-box">
    ⚠️ <b>NAPOMENA:</b> Koristite max 1 sat (limit punjenja). Budimo kolegijalni!
</div>
""", unsafe_allow_html=True)

# Informacija o vremenu punjenja
col_time_left, col_time_right = st.columns([2, 1])
with col_time_left:
    st.markdown('<p class="timer-text">🕒 <span class="timer-highlight">Tab</span> puni već <span class="timer-highlight">4 min</span></p>', unsafe_allow_html=True)
with col_time_right:
    st.markdown('<p class="timer-text" style="text-align: right; color: #70757A;">od 14:49h</p>', unsafe_allow_html=True)

# Plavo akciono dugme za oslobađanje punjača
if st.button("Završi punjenje (Oslobodi punjač)"):
    st.success("Punjač je uspešno oslobođen!")

st.markdown('</div>', unsafe_allow_html=True) # Kraj glavnog kontejnera


# SEKCIJA: LISTA ČEKANJA
st.markdown('<div class="queue-header">📋 Lista čekanja <span class="queue-count">0</span></div>', unsafe_allow_html=True)
st.markdown('<p class="empty-queue">Nema ljudi u redu</p>', unsafe_allow_html=True)

# Polje za unos imena na dnu ekrana
ime = st.text_input(label="", placeholder="Ukucaj ime za red ili brisanje...")

# Akcija za unos imena
if ime:
    st.info(# Zvanični sajt Lidl Srbija dostupan je na adresi kompanija.lidl.rs
        f"Korisnik **{ime}** je dodat na listu čekanja za punjač na lokaciji Lidl Galenika."
    )
