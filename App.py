import streamlit as st
import datetime
import json
import os

# 1. Podešavanje stranice i automatsko sakrivanje menija kroz sistemska podešavanja
st.set_page_config(
    page_title="EV Punjač - Galenika", 
    page_icon="⚡", 
    layout="centered"
)

# Sakrivanje preostalih Streamlit sistemskih menija i dugmeta "Manage app" preko čistog CSS-a
st.markdown("<style> .stApp { background-color: #121214 !important; color: #ffffff !important; } [data-testid='stHeader'] { display: none !important; } footer { display: none !important; } .viewerBadge { display: none !important; } .stAppDeployButton { display: none !important; } iframe[title='Managed Hosting Badge'] { display: none !important; } div[data-testid='stStatusWidget'] { display: none !important; } [data-testid='stDecoration'] { display: none !important; } [data-testid='stMarkdownContainer'] p { color: #e2e8f0 !important; margin-bottom: 4px !important; } .stButton > button { background-color: #007AFF !important; color: white !important; height: 38px !important; padding: 0px 10px !important; font-size: 13px !important; font-weight: bold !important; border-radius: 8px !important; border: none !important; margin-top: 2px !important; margin-bottom: 2px !important; display: block !important; margin-left: auto !important; margin-right: auto !important; } div.element-container:has(button:contains('Završi punjenje')) button { background-color: #ff453a !important; } div.element-container:has(button:contains('Odustani od čekanja')) button { background-color: #e11d48 !important; } .stTextInput input { background-color: #1a1a1e !important; color: white !important; border: 1px solid #2a2a30 !important; border-radius: 6px !important; height: 36px !important; font-size: 13px !important; } </style>", unsafe_allow_html=True)

FAJL_BAZE = "baza_stanja.json"

def nase_trenutno_vreme():
    return datetime.datetime.utcnow() + datetime.timedelta(hours=2)

# Funkcija koja sama proverava ispravnost baze i popravlja je ako ima starih formata vremena
def ucitaj_i_osiguraj_bazu():
    fabricko_stanje = {"slobodan": True, "korisnik": "", "vreme_pocetka": "", "red": []}
    if not os.path.exists(FAJL_BAZE):
        return fabricko_stanje
    try:
        with open(FAJL_BAZE, "r") as f:
            d = json.load(f)
            if d.get("vreme_pocetka") and ":" in d["vreme_pocetka"] and "-" not in d["vreme_pocetka"]:
                d["vreme_pocetka"] = ""
                d["slobodan"] = True
                d["korisnik"] = ""
            return d
    except:
        return fabricko_stanje

def sacuvaj_bazu(d):
    with open(FAJL_BAZE, "w") as f:
        json.dump(d, f)

if "db" not in st.session_state:
    st.session_state.db = ucitaj_i_osiguraj_bazu()

db = st.session_state.db

# PRIKAZ LOGOTIPA PREKO STABILNOG I PROVERENOG PNG LINKA
col1, col2, col3 = st.columns([1, 0.35, 1])
with col2:
    st.image("https://wikimedia.org", use_container_width=True)

# GLAVNI NASLOV
st.markdown("<h1 style='text-align: center; color: #ffffff; font-size: 20px; font-weight: 800; margin-top: 5px; margin-bottom: 0;'>⚡ EV Punjač</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 13px; margin-top: 0; margin-bottom: 2px;'>Lidl Galenika</p>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; margin-bottom: 10px;'><span style='display: inline-block; background-color: rgba(57, 211, 83, 0.1); color: #39d353; border: 1px solid rgba(57, 211, 83, 0.3); padding: 1px 8px; border-radius: 20px; font-weight: bold; font-size: 10px;'>✓ Online</span></div>", unsafe_allow_html=True)

if db["slobodan"]:
    status_tekst, status_boja, status_bg = "Slobodan", "#39d353", "rgba(57, 211, 83, 0.1)"
else:
    status_tekst, status_boja, status_bg = f"Zauzet ({db['korisnik']})", "#ff453a", "rgba(255, 69, 58, 0.1)"

# KARTICA SA STATUSOM PUNJAČA
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

# EKRAN KADA JE PUNJAČ SLOBODAN
if db["slobodan"]:
    st.markdown("<p style='font-size: 11px; font-weight: bold; color: #94a3b8; margin-bottom: 2px; text-align: center;'>UKUCAJ SVOJE IME ZA CHECK-IN:</p>", unsafe_allow_html=True)
    ime_korisnika = st.text_input("Ime", placeholder="Tvoje ime...", label_visibility="collapsed", key="kljuc_checkin_input")
    
    if st.button("Check-in", use_container_width=True, key="kljuc_checkin_dugme"):
        if ime_korisnika.strip() != "":
            db["slobodan"] = False
            db["korisnik"] = ime_korisnika.strip()
            db["vreme_pocetka"] = nase_trenutno_vreme().isoformat()
            sacuvaj_bazu(db)
            st.rerun()
        else:
            st.warning("Unesite ime pre čekiranja.")

# EKRAN KADA JE PUNJAČ ZAUZET
else:
    vreme_prikaz = "0 min"
    sat_kacenja = "--:--"
    
    if db.get("vreme_pocetka"):
        try:
            vp = datetime.datetime.fromisoformat(db["vreme_pocetka"])
            sat_kacenja = vp.strftime("%H:%M")
            proteklo = nase_trenutno_vreme() - vp
            ukupno_sekundi = int(proteklo.total_seconds())
            sati = max(0, ukupno_sekundi // 3600)
            minuti = max(0, (ukupno_sekundi % 3600) // 60)
            vreme_prikaz = f"{sati}h {minuti}min" if sati > 0 else f"{minuti} min"
            
            if ukupno_sekundi >= 3600:
                st.error("⏰ Korisnik je prekoračio limit od 1 sat punjenja!")
        except:
            pass

    status_linija_html = f"""
    <div style="background-color: rgba(0, 122, 255, 0.08); border: 1px solid rgba(0, 122, 255, 0.2); border-radius: 10px; padding: 8px 12px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; margin-left: auto; margin-right: auto;">
        <div style="font-size: 13px; color: #e2e8f0; display: flex; align-items: center; gap: 4px;">
            <span>⏱️</span>
            <span><strong style="color: #ffffff;">{db['korisnik']}</strong> puni već <strong style="color: #007AFF; font-size: 14px; font-weight: bold;">{vreme_prikaz}</strong></span>
        </div>
        <span style="font-size: 11px; color: #94a3b8;">od {sat_kacenja}h</span>
    </div>
    """
    st.markdown(status_linija_html, unsafe_allow_html=True)
    
    if st.button("Završi punjenje (Oslobodi punjač)", use_container_width=True, key="kljuc_Zavrsi_dugme"):
        if db["red"]:
            db["korisnik"] = db["red"].pop(0)
            db["vreme_pocetka"] = nase_trenutno_vreme().isoformat()
        else:
            db["slobodan"] = True
            db["korisnik"] = ""
            db["vreme_pocetka"] = ""
        sacuvaj_bazu(db)
        st.rerun()

# PRIKAZ LISTE ČEKANJA
broj_u_redu = len(db["red"])
st.markdown(f"""
<div style="border: 1px solid #2a2a30; border-radius: 10px; padding: 10px; background-color: #1a1a1e; margin-top: 6px; margin-bottom: 6px; margin-left: auto; margin-right: auto;">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 14px; font-weight: bold; color: #ffffff;">📋 Lista čekanja</span>
        <span style="background-color: rgba(0, 122, 255, 0.15); color: #007AFF; padding: 1px 8px; border-radius: 12px; font-weight: bold; font-size: 11px;">{broj_u_redu}</span>
    </div>
</div>
""", unsafe_allow_html=True)

if broj_u_redu == 0:
    st.markdown("<p style='color: #70757A; text-align: center; font-size: 12px; margin-top: 5px; margin-bottom: 10px;'>Nema ljudi u redu</p>", unsafe_allow_html=True)
else:
    za_prikaz_reda = ""
    for i, osoba in enumerate(db["red"], 1):
        za_prikaz_reda += f"<div style='padding: 4px 8px; background: #222226; border-radius: 6px; margin-bottom: 4px; font-size: 13px;'>{i}. <b>{osoba}</b></div>"
    st.markdown(za_prikaz_reda, unsafe_allow_html=True)

# Polje za unos na dnu aplikacije
st.markdown("<p style='font-size: 11px; font-weight: bold; color: #94a3b8; margin-top: 6px; margin-bottom: 2px;'>DODAJ ILI OBRIŠI SEBE IZ REDA:</p>", unsafe_allow_html=True)
ime_red = st.text_input("Ime za red", placeholder="Ukucaj ime za red ili brisanje...", label_visibility="collapsed", key="kljuc_red_input")

if ime_red:
    ime_cisto = ime_red.strip()
    if ime_cisto:
        if ime_cisto in db["red"]:
            db["red"].remove(ime_cisto)
            sacuvaj_bazu(db)
            st.rerun()
        elif db["korisnik"] == ime_cisto:
            st.error("Već koristiš punjač!")
        else:
            db["red"].append(ime_cisto)
            sacuvaj_bazu(db)
            st.rerun()
