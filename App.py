import streamlit as st
import datetime
import json
import os

# Podešavanje stranice za mobilne telefone i automatsko forsiranje tamne teme
st.set_page_config(page_title="EV Punjač - Galenika", page_icon="⚡", layout="centered")

# Injektovanje CSS-a za globalnu tamnu pozadinu cele aplikacije i stilizovanje dugmića
st.markdown("""
    <style>
        /* Sila za tamnu pozadinu aplikacije */
        .stApp {
            background-color: #121214 !important;
            color: #ffffff !important;
        }
        /* Srednji deo - uklanjanje podrazumevanih Streamlit margina oko teksta */
        [data-testid="stMarkdownContainer"] p {
            color: #e2e8f0 !important;
        }
        /* Stilizovanje glavnih Streamlit dugmića (Check-in, Oslobodi...) */
        .stButton > button {
            background-color: #007AFF !important; 
            color: white !important; 
            height: 46px !important; 
            font-size: 15px !important; 
            font-weight: bold !important; 
            border-radius: 10px !important;
            border: none !important;
            transition: background 0.2s ease;
        }
        .stButton > button:hover {
            background-color: #0062cc !important;
        }
        /* Poseban stil za dugme za oslobađanje (Crveno/Narandžasto) */
        div.element-container:has(button:contains("Završi punjenje")) button {
            background-color: #ff453a !important;
        }
        /* Stilizovanje polja za unos teksta (Input polja) */
        .stTextInput input {
            background-color: #1a1a1e !important;
            color: white !important;
            border: 1px solid #2a2a30 !important;
            border-radius: 8px !important;
        }
    </style>
""", unsafe_allow_html=True)

# Lokacija fajla koji glumi bazu podataka
FAJL_BAZE = "baza_stanja.json"

def nase_trenutno_vreme():
    # Serversko UTC vreme pomeramo za +2 sata (naša vremenska zona)
    return datetime.datetime.utcnow() + datetime.timedelta(hours=2)

def ucitaj_bazu():
    if os.path.exists(FAJL_BAZE):
        try:
            with open(FAJL_BAZE, "r") as f:
                d = json.load(f)
                if d.get("vreme_pocetka"):
                    try:
                        d["vreme_pocetka"] = datetime.datetime.fromisoformat(d["vreme_pocetka"])
                    except:
                        d["vreme_pocetka"] = nase_trenutno_vreme()
                return d
        except:
            pass
    return {"slobodan": True, "korisnik": "", "vreme_pocetka": None, "red": []}

def sacuvaj_bazu(d):
    kopija = d.copy()
    if kopija.get("vreme_pocetka"):
        if isinstance(kopija["vreme_pocetka"], datetime.datetime):
            kopija["vreme_pocetka"] = kopija["vreme_pocetka"].replace(tzinfo=None).isoformat()
    with open(FAJL_BAZE, "w") as f:
        json.dump(kopija, f)

# Učitavanje trenutnog stanja
if "db" not in st.session_state:
    st.session_state.db = ucitaj_bazu()

# NASLOV I ONLINE STATUS (Novi UI sa većim fontovima i neon zelenom značkom)
st.markdown("<h1 style='text-align: center; color: #ffffff; font-size: 32px; font-weight: 800; margin-bottom: 0;'>⚡ EV Punjači</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 18px; margin-top: 2px; margin-bottom: 8px;'>Lidl Galenika</p>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; margin-bottom: 25px;">
    <span style="display: inline-block; background-color: rgba(57, 211, 83, 0.1); color: #39d353; border: 1px solid rgba(57, 211, 83, 0.3); padding: 4px 14px; border-radius: 20px; font-weight: bold; font-size: 13px;">✓ Online</span>
</div>
""", unsafe_allow_html=True)

db = st.session_state.db

# Popravka u letu ako je vreme povuklo zonu iz prošlog koda
if db["vreme_pocetka"] and hasattr(db["vreme_pocetka"], "tzinfo") and db["vreme_pocetka"].tzinfo is not None:
    db["vreme_pocetka"] = db["vreme_pocetka"].replace(tzinfo=None)

if db["slobodan"]:
    status_tekst, status_boja, status_bg = "Slobodan", "#39d353", "rgba(57, 211, 83, 0.1)"
else:
    status_tekst, status_boja, status_bg = f"Zauzet ({db['korisnik']})", "#ff453a", "rgba(255, 69, 58, 0.1)"

# GLAVNA KARTICA PUNJAČA (Tamna pozadina, pojačana slova za 22kW i uočljiva napomena)
punjac_html = f"""
<div style="border: 1px solid #2a2a30; border-radius: 16px; padding: 20px; background-color: #1a1a1e; margin-bottom: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.3);">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
        <h3 style="margin: 0; color: #ffffff; font-size: 20px; font-weight: 700;">EV Punjač Lidl Galenika</h3>
        <span style="background-color: {status_bg}; color: {status_boja}; border: 1px solid {status_boja}44; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 12px; white-space: nowrap;">{status_tekst}</span>
    </div>
    <p style="margin: 6px 0; color: #94a3b8; font-size: 15px;">📍 Galenika, Zemun</p>
    <p style="margin: 6px 0 12px 0; color: #ffffff; font-size: 24px; font-weight: 900;">🔋 22kW</p>
    <div style="background-color: rgba(245, 158, 11, 0.1); border-left: 4px solid #f59e0b; padding: 10px; border-radius: 0 8px 8px 0; margin-top: 12px;">
        <p style="margin: 0; color: #fef3c7; font-size: 13px; font-weight: 500; line-height: 1.45;">
            <strong>⚠️ NAPOMENA:</strong> Molimo korisnike da punjač koriste maksimalno 1 sat, koliko i sam punjač fabrički dozvoljava. Budimo kolegijalni!
        </p>
    </div>
</div>
"""
st.markdown(punjac_html, unsafe_allow_html=True)

if db["slobodan"]:
    st.markdown("<p style='font-size: 12px; font-weight: bold; color: #94a3b8; margin-bottom: 4px; margin-top: 10px;'>UKUCAJ SVOJE IME IZ VIBER GRUPE:</p>", unsafe_allow_html=True)
    ime_korisnika = st.text_input("Ime", placeholder="Npr. Goran, Nikola, Dejan...", label_visibility="collapsed")
    
    if st.button("Check-in", use_container_width=True):
        if ime_korisnika.strip() != "":
            db["slobodan"] = False
            db["korisnik"] = ime_korisnika
            db["vreme_pocetka"] = nase_trenutno_vreme()
            sacuvaj_bazu(db)
            st.rerun()
        else:
            st.warning("Molimo vas unesite ime pre čekiranja.")
else:
    # SMANJENI I SPAKOVANI DONJI DEO (Automatsko osvežavanje 30s, sve stoji u jednoj tankoj liniji)
    @st.fragment(run_every="30s")
    def prikazi_tajmer():
        vreme_kacenja = db["vreme_pocetka"].strftime("%H:%M")
        proteklo = nase_trenutno_vreme() - db["vreme_pocetka"]
        ukupno_sekundi = int(proteklo.total_seconds())
        sati = max(0, ukupno_sekundi // 3600)
        minuti = max(0, (ukupno_sekundi % 3600) // 60)
        
        if sati > 0:
            vreme_prikaz = f"{sati}h {minuti}min"
        else:
            vreme_prikaz = f"{minuti} min"
            
        # Generisanje tanke plave linije (spojenih podataka) prema tvom zahtevu
        status_linija_html = f"""
        <div style="background-color: rgba(0, 122, 255, 0.1); border: 1px solid rgba(0, 122, 255, 0.25); border-radius: 12px; padding: 12px 16px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
            <div style="font-size: 15px; color: #e2e8f0; display: flex; items-center: center; gap: 6px;">
                <span>⏱️</span>
                <span><strong style="color: #ffffff;">{db['korisnik']}</strong> puni već <strong style="color: #007AFF; font-size: 18px; font-weight: 900;">{vreme_prikaz}</strong></span>
            </div>
            <span style="font-size: 12px; color: #94a3b8; font-weight: 500;">od {vreme_kacenja}h</span>
        </div>
        """
        st.markdown(status_linija_html, unsafe_allow_html=True)
        
        # Ako punjenje pređe 60 minuta, ispisuje se crveno upozorenje
        if ukupno_sekundi >= 3600:
            st.error("⏰ Isteklo je maksimalnih sat vremena punjenja! Molimo oslobodite mesto za sledećeg korisnika.")
    
    # Pozivamo tajmer
    prikazi_tajmer()
        
    if st.button("Završi punjenje (Oslobodi punjač)", use_container_width=True):
        if db["red"]:
            db["korisnik"] = db["red"].pop(0)
            db["vreme_pocetka"] = nase_trenutno_vreme()
        else:
            db["slobodan"] = True
            db["korisnik"] = ""
            db["vreme_pocetka"] = None
        sacuvaj_bazu(db)
        st.rerun()

st.write("") 

# LISTA ČEKANJA (Takođe stilizovana u tamnoj temi)
broj_u_redu = len(db["red"])
st.markdown(f"""
<div style="border: 1px solid #2a2a30; border-radius: 16px; padding: 16px; background-color: #1a1a1e; margin-bottom: 12px;">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 16px; font-weight: bold; color: #ffffff;">📋 Lista čekanja</span>
        <span style="background-color: rgba(0, 122, 255, 0.15); color: #007AFF; padding: 2px 10px; border-radius: 20px; font-weight: bold; font-size: 13px;">{broj_u_redu}</span>
    </div>
</div>
""", unsafe_allow_html=True)

if broj_u_redu == 0:
    st.markdown("<p style='text-align: center; color: #64748b; font-size: 14px; margin-bottom: 15px;'>Nema ljudi u redu</p>", unsafe_allow_html=True)
else:
    for i, ime in enumerate(db["red"]):
        st.markdown(f"<div style='padding: 8px 14px; background: #222226; border: 1px solid #2a2a30; border-radius: 8px; margin-bottom: 6px; font-size: 14px; color: #e2e8f0;'><b>{i+1}.</b> {ime}</div>", unsafe_allow_html=True)

if not db["slobodan"]:
    st.write("")
    ime_za_listu = st.text_input("Tvoje ime za listu", placeholder="Unesi ime za red...", key="red_ime", label_visibility="collapsed")
    if st.button("+ Pridruži se redu", use_container_width=True):
        if ime_za_listu.strip() != "":
            db["red"].append(ime_za_listu)
            sacuvaj_bazu(db)
            st.rerun()
