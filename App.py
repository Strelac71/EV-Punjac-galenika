import streamlit as st

# 1. PODEŠAVANJE STRANICE I VEĆIH SLOVA + LIDL BOJA (Tamno plava i Žuta)
st.markdown("""
    <style>
        /* Promena pozadine cele aplikacije i glavnog fonta */
        .stApp {
            background-color: #f8f9fa;
        }
        
        /* Povećavanje glavnog naslova i promena boje u Lidl plavu */
        h1 {
            color: #002d72 !important;
            font-size: 42px !important; /* Veća slova za naslov */
            font-weight: bold !important;
            text-align: center;
        }
        
        /* Povećavanje podnaslova i običnog teksta */
        .stMarkdown p, p, span {
            font-size: 20px !important; /* Veća slova za tekst i statuse */
            color: #333333;
        }
        
        /* Stilizovanje glavnog dugmeta u Lidl žutu boju sa plavim tekstom */
        div.stButton > button:first-child {
            background-color: #fff200 !important;
            color: #002d72 !important;
            font-size: 22px !important; /* Veća slova na dugmetu */
            font-weight: bold !important;
            border: 2px solid #002d72 !important;
            border-radius: 8px !important;
            width: 100% !important;
            padding: 10px !important;
        }
        
        /* Efekat kada se mišem pređe preko dugmeta */
        div.stButton > button:first-child:hover {
            background-color: #002d72 !important;
            color: #fff200 !important;
        }
    </style>
""", unsafe_allow_html=True)

# 2. UBACIVANJE LIDL LOGOTIPA NA VRH STRANICE
# Logo je centriran pomoću Streamlit kolona
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.image("https://wikimedia.org", width=120)

# 3. VAŠ GLAVNI NASLOV (Sada je automatski plav i veći)
st.title("EV Punjač Galenika")

# --- OVDE NASTAVLJA VAŠ OSTATAK KODA ZA STATUSE I DUGMRE ---
st.write("---")
st.markdown("**Status punjača:** 🟢 Dostupno / Slobodno")
st.markdown("**Trenutna cena:** 45 RSD / kWh")

st.write("") # Razmak

if st.button("ZAPOČNI PUNJENJE"):
    st.success("Punjenje je uspešno pokrenuto!")
