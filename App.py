import streamlit as st

# 1. PODEŠAVANJE STRANICE
st.set_page_config(
    page_title="EV Punjač Galenika",
    page_icon="⚡",
    layout="centered"
)

# 2. STABILAN ZVANIČNI LINK ZA LIDL LOGO (Učitava se bez greške)
lidl_logo_url = "https://wikimedia.org"

# Prikaz logotipa na sredini ekrana pomoću kolona
col1, col2, col3 = st.columns([1, 0.5, 1])
with col2:
    st.image(lidl_logo_url, width=100)

# 3. GLAVNI NASLOV (Krupniji tekst)
st.markdown("<h1 style='text-align: center; font-size: 38px;'>EV Punjač Galenika</h1>", unsafe_allow_html=True)
st.write("") # Razmak

# 4. STATUSI I CENA (Veća i uočljivija slova)
st.markdown("<p style='font-size: 24px; font-weight: 500;'>Status punjača: 🟢 Dostupno / Slobodno</p>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 24px; font-weight: 500;'>Trenutna cena: 45 RSD / kWh</p>", unsafe_allow_html=True)
st.write("") # Razmak

# 5. POVEĆANO I STILIZOVANO ŽUTO DUGME
st.markdown("""
    <style>
        div.stButton > button:first-child {
            background-color: #FFF200 !important;
            color: #002D72 !important;
            font-size: 24px !important;
            font-weight: bold !important;
            border: 3px solid #002D72 !important;
            border-radius: 8px !important;
            width: 100% !important;
            padding: 12px 0px !important;
        }
        /* Efekat kada se pređe prstom/mišem preko dugmeta */
        div.stButton > button:first-child:hover {
            background-color: #002D72 !important;
            color: #FFF200 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Glavno dugme za pokretanje
if st.button("ZAPOČNI PUNJENJE"):
    st.success("Punjenje je uspešno pokrenuto!")
