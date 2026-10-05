import streamlit as st
import datetime
import json
import os

# Podešavanje stranice
st.set_page_config(
    page_title="EV Punjač - Galenika", 
    page_icon="⚡", 
    layout="centered"
)

# Ultra-kompaktan CSS za Dark Mode i dugmiće
st.markdown("<style> .stApp { background-color: #121214 !important; color: #ffffff !important; } [data-testid='stMarkdownContainer'] p { color: #e2e8f0 !important; margin-bottom: 4px !important; } .stButton > button { background-color: #007AFF !important; color: white !important; height: 38px !important; padding: 0px 10px !important; font-size: 13px !important; font-weight: bold !important; border-radius: 8px !important; border: none !important; margin-top: 2px !important; margin-bottom: 2px !important; display: block !important; margin-left: auto !important; margin-right: auto !important; } div.element-container:has(button:contains('Završi punjenje')) button { background-color: #ff453a !important; } .stTextInput input { background-color: #1a1a1e !important; color: white !important; border: 1px solid #2a2a30 !important; border-radius: 6px !important; height: 36px !important; font-size: 13px !important; } </style>", unsafe_allow_html=True)

FAJL_BAZE = "baza_stanja.json"

def ucitaj_bazu():
    if os.path.exists(FAJL_BAZE):
        try:
            with open(FAJL_BAZE, "r") as f:
                return json.load(f)
        except:
            pass
    return {"slobodan": True, "korisnik": "", "vreme_pocetka": "", "red": []}

def sacuvaj_bazu(d):
    with open(FAJL_BAZE, "w") as f:
        json.dump(d, f)

if "db" not in st.session_state:
    st.session_state.db = ucitaj_bazu()

db = st.session_state.db

# GLAVNI NASLOV
st.markdown("<h1 style='text-align: center; color: #ffffff; font-size: 20px; font-weight: 800; margin-top: 0; margin-bottom: 0;'>⚡ EV Punjač</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 13px; margin-top: 0; margin-bottom: 2px;'>Lidl Galenika</p>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; margin-bottom: 10px;'><span style='display: inline-block; background-color: rgba(57, 211, 83, 0.1); color: #39d353; border: 1px solid rgba(57, 211, 83, 0.3); padding: 1px 8px; border-radius: 20px; font-weight: bold; font-size: 10px;'>✓ Online</span></div>", unsafe_allow_html=True)

if db["slobodan"]:
    status_tekst, status_boja, status_bg = "Slobodan", "#39d353", "rgba(57, 211, 83, 0.1)"
else:
    status_tekst, status_boja, status_bg = f"Zauzet ({db['korisnik']})", "#ff453a", "rgba(255, 69, 58, 0.1)"

# KARTICA SA STATUSOM
punjac_html = f"""
<div style="border: 1px solid #2a2a30; border-radius: 12px; padding: 12px; background-color: #1a1a1e; margin-bottom: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
        <h3 style="margin: 0; color: #ffffff; font-size: 16px; font-weight: 700;">EV Punjač Lidl Galenika</h3>
        <span style="background-color: {status_bg}; color: {status_boja}; border: 1px solid {status_boja}44; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px;">{status_tekst}</span>
    </div>
    <p style="margin: 2px 0; color: #94a3b8; font-size: 13px;">📍 Galenika, Zemun &nbsp;&nbsp;&nbsp; <b>🔋 22kW</b></p>
    <div style="background-color: rgba(239, 68, 68, 0.12); border-left: 3px solid #ff453a; padding: 6px 10px; border-radius: 0 6px 6px 0; margin-top: 6px;">
        <p style="margin: 0; color: #ffffff; font-size: 11px; font-weight: 500; line-height: 1.3;">
            <strong style="color: #ff453a;">⚠️ NAPOMENA:</strong> Koristite max 1 sat (limit punjenja). Budimo kolegijalni!
        </p>
    </div>
</div>
"""
st.markdown(punjac_html, unsafe_allow_html=True)

# LOGIKA KADA JE PUNJAČ SLOBODAN
if db["slobodan"]:
    st.markdown("<p style='font-size: 11px; font-weight: bold; color: #94a3b8; margin-bottom: 2px; text-align: center;'>UKUCAJ SVOJE IME ZA CHECK-IN:</p>", unsafe_allow_html=True)
    ime_korisnika = st.text_input("Ime", placeholder="Tvoje ime...", label_visibility="collapsed", key="kljuc_checkin_input")
    
    if st.button("Check-in", use_container_width=True, key="kljuc_checkin_dugme"):
        if ime_korisnika.strip() != "":
            db["slobodan"] = False
            db["korisnik"] = ime_korisnika
            # Automatsko uzimanje našeg lokalnog vremena za upis (npr. 14:35)
            sada = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
            db["vreme_pocetka"] = sada.strftime("%H:%M")
            sacuvaj_bazu(db)
            st.rerun()
        else:
            st.warning("Unesite ime pre čekiranja.")

# LOGIKA KADA JE PUNJAČ ZAUZET
else:
    status_linija_html = f"""
    <div style="background-color: rgba(0, 122, 255, 0.08); border: 1px solid rgba(0, 122, 255, 0.2); border-radius: 10px; padding: 8px 12px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; margin-left: auto; margin-right: auto;">
        <div style="font-size: 13px; color: #e2e8f0; display: flex; align-items: center; gap: 4px;">
            <span>⏱️</span>
            <span><strong style="color: #ffffff;">{db['korisnik']}</strong> je zauzeo punjač</span>
        </div>
        <span style="font-size: 11px; color: #94a3b8;">od {db['vreme_pocetka']}h</span>
    </div>
    """
    st.markdown(status_linija_html, unsafe_allow_html=True)
    
    if st.button("Završi punjenje (Oslobodi punjač)", use_container_width=True, key="kljuc_Zavrsi_dugme"):
        if db["red"]:
            db["korisnik"] = db["red"].pop(0)
            sada = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
            db["vreme_pocetka"] = sada.strftime("%H:%M")
        else:
            db["slobodan"] = True
            db["korisnik"] = ""
            db["vreme_pocetka"] = ""
        sacuvaj_bazu(db)
        st.rerun()

# LISTA ČEKANJA
broj_u_redu = len(db["red"])
st.markdown(f"""
<div style="border: 1px solid #2a2a30; border-radius: 10px; padding: 10px; background-color: #1a1a1e; margin-top: 6px; margin-bottom: 6px; margin-left: auto; margin-right: auto;">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 14px; font-weight: bold; color: #ffffff;">📋 Lista čekanja</span>
        <span style="background-color: rgba(0, 122, 255, 0.15); color: #007AFF; padding: 1px 8px; border-radius: 20px; font-weight: bold; font-size: 11px;">{broj_u_redu}</span>
    </div>
</div>
""", unsafe_allow_html=True)

if broj_u_redu == 0:
    st.markdown("<div style='text-align: center; padding: 6px 10px; background: #1a1a1e; border-radius: 6px; margin-bottom: 6px; font-size: 13px; color: #64748b; margin-left: auto; margin-right: auto;'>Nema ljudi u redu</div>", unsafe_allow_html=True)
else:
    imena_u_redu = ", ".join([f"<b>{i+1}.</b> {ime}" for i, ime in enumerate(db["red"])])
    st.markdown(f"<div style='text-align: center; padding: 6px 10px; background: #1a1a1e; border-radius: 6px; margin-bottom: 6px; font-size: 13px; color: #e2e8f0; margin-left: auto; margin-right: auto;'>{imena_u_redu}</div>", unsafe_allow_html=True)

# UPIS U RED ŠANSU
st.write("")
ime_za_listu = st.text_input("Tvoje ime za listu", placeholder="Unesi ime za red...", key="kljuc_lista_input", label_visibility="collapsed")
if st.button("+ Pridruži se redu", use_container_width=True, key="kljuc_lista_dugme"):
    if ime_za_listu.strip() != "":
        db["red"].append(ime_za_listu)
        sacuvaj_bazu(db)
        st.rerun()
