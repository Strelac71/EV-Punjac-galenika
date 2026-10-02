import streamlit as st
import datetime
import json
import os

# Podešavanje stranice - uklanjanje nepotrebnih margina
st.set_page_config(page_title="EV Punjač - Galenika", page_icon="⚡", layout="centered")

# Injektovanje ultra-kompaktnog, suženog i fluidnog CSS-a za mobilne ekrane
st.markdown("""
    <style>
        /* Pozadina aplikacije */
        .stApp {
            background-color: #121214 !important;
            color: #ffffff !important;
        }
        /* Smanjivanje glavnog praznog prostora na vrhu i optimalno fluidno sužavanje celog sadržaja */
        .block-container {
            padding-top: 0.5rem !important;
            padding-bottom: 1rem !important;
            max-width: 94% !important;
            margin: 0 auto !important;
        }
        /* Smanjivanje margina oko markdown elemenata */
        [data-testid="stMarkdownContainer"] p {
            color: #e2e8f0 !important;
            margin-bottom: 4px !important;
        }
        /* Kompaktna dugmad - smanjen unutrašnji padding da tekst nikada ne ispada */
        .stButton > button {
            background-color: #007AFF !important; 
            color: white !important; 
            height: 38px !important; 
            padding: 0px 10px !important;
            font-size: 13px !important; 
            font-weight: bold !important; 
            border-radius: 8px !important;
            border: none !important;
            margin-top: 2px !important;
            margin-bottom: 2px !important;
            width: 94% !important;
            display: block !important;
            margin-left: auto !important;
            margin-right: auto !important;
        }
        /* Crveno dugme za završetak punjenja */
        div.element-container:has(button:contains("Završi punjenje")) button {
            background-color: #ff453a !important;
        }
        /* Fluidna i blago sužena polja za unos teksta */
        .stTextInput > div {
            width: 94% !important;
            margin-left: auto !important;
            margin-right: auto !important;
        }
        .stTextInput input {
            background-color: #1a1a1e !important;
            color: white !important;
            border: 1px solid #2a2a30 !important;
            border-radius: 6px !important;
            height: 36px !important;
            font-size: 13px !important;
        }
        /* Centriranje i fluidno sužavanje Streamlit error/warning poruka */
        .stAlert {
            width: 94% !important;
            margin-left: auto !important;
            margin-right: auto !important;
        }
    </style>
""", unsafe_allow_html=True)

# Lokacija fajla koji glumi bazu podataka
FAJL_BAZE = "baza_stanja.json"

def nase_trenutno_vreme():
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

if "db" not in st.session_state:
    st.session_state.db = ucitaj_bazu()

# MAKSIMALNO SMANJENO ZAGLAVLJE
st.markdown("<h1 style='text-align: center; color: #ffffff; font-size: 24px; font-weight: 800; margin-top: 0; margin-bottom: 0;'>⚡ EV Punjači</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 14px; margin-top: 0; margin-bottom: 4px;'>Lidl Galenika</p>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; margin-bottom: 12px;">
    <span style="display: inline-block; background-color: rgba(57, 211, 83, 0.1); color: #39d353; border: 1px solid rgba(57, 211, 83, 0.3); padding: 2px 10px; border-radius: 20px; font-weight: bold; font-size: 11px;">✓ Online</span>
</div>
""", unsafe_allow_html=True)

db = st.session_state.db

if db["vreme_pocetka"] and hasattr(db["vreme_pocetka"], "tzinfo") and db["vreme_pocetka"].tzinfo is not None:
    db["vreme_pocetka"] = db["vreme_pocetka"].replace(tzinfo=None)

if db["slobodan"]:
    status_tekst, status_boja, status_bg = "Slobodan", "#39d353", "rgba(57, 211, 83, 0.1)"
else:
    status_tekst, status_boja, status_bg = f"Zauzet ({db['korisnik']})", "#ff453a", "rgba(255, 69, 58, 0.1)"

# KARTICA PUNJAČA SA CRVENOM NAPOMENOM
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

# LOGIKA ZA SLOBODAN / ZAUZET PUNJAČ
if db["slobodan"]:
    st.markdown("<p style='font-size: 11px; font-weight: bold; color: #94a3b8; margin-bottom: 2px; text-align: center;'>UKUCAJ SVOJE IME ZA CHECK-IN:</p>", unsafe_allow_html=True)
    ime_korisnika = st.text_input("Ime", placeholder="Tvoje ime...", label_visibility="collapsed", key="checkin_ime")
    
    if st.button("Check-in", use_container_width=True):
        if ime_korisnika.strip() != "":
            db["slobodan"] = False
            db["korisnik"] = ime_korisnika
            db["vreme_pocetka"] = nase_trenutno_vreme()
            sacuvaj_bazu(db)
            st.rerun()
        else:
            st.warning("Unesite ime pre čekiranja.")
else:
    # TAJMER SA POVEĆANIM VREMENOM PUNJENJA (SKALIRAN NA 94% ŠIRINE)
    @st.fragment(run_every="30s")
    def prikazi_tajmer():
        vreme_kacenja = db["vreme_pocetka"].strftime("%H:%M")
        proteklo = nase_trenutno_vreme() - db["vreme_pocetka"]
        ukupno_sekundi = int(proteklo.total_seconds())
        sati = max(0, ukupno_sekundi // 3600)
        minuti = max(0, (ukupno_sekundi % 3600) // 60)
        
        vreme_prikaz = f"{sati}h {minuti}min" if sati > 0 else f"{minuti} min"
            
        status_linija_html = f"""
        <div style="background-color: rgba(0, 122, 255, 0.08); border: 1px solid rgba(0, 122, 255, 0.2); border-radius: 10px; padding: 8px 12px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; width: 94%; margin-left: auto; margin-right: auto;">
            <div style="font-size: 13px; color: #e2e8f0; display: flex; align-items: center; gap: 4px;">
                <span>⏱️</span>
                <span><strong style="color: #ffffff;">{db['korisnik']}</strong> puni već <strong style="color: #007AFF; font-size: 18px; font-weight: 900; background-color: rgba(0, 122, 255, 0.15); padding: 2px 6px; border-radius: 4px;">{vreme_prikaz}</strong></span>
            </div>
            <span style="font-size: 11px; color: #94a3b8;">od {vreme_kacenja}h</span>
        </div>
        """
        st.markdown(status_linija_html, unsafe_allow_html=True)
        
        if ukupno_sekundi >= 3600:
            st.error("⏰ Isteklo je sat vremena punjenja!")
            
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

# SUŽENA LISTA ČEKANJA (SKALIRANA NA 94% ŠIRINE)
broj_u_redu = len(db["red"])
st.markdown(f"""
<div style="border: 1px solid #2a2a30; border-radius: 10px; padding: 10px; background-color: #1a1a1e; margin-top: 6px; margin-bottom: 6px; width: 94%; margin-left: auto; margin-right: auto;">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 14px; font-weight: bold; color: #ffffff;">📋 Lista čekanja</span>
        <span style="background-color: rgba(0, 122, 255, 0.15); color: #007AFF; padding: 1px 8px; border-radius: 20px; font-weight: bold; font-size: 11px;">{broj_u_redu}</span>
    </div>
</div>
""", unsafe_allow_html=True)

if broj_u_redu == 0:
    st.markdown("<p style='text-align: center; color: #64748b; font-size: 12px; margin-bottom: 4px;'>Nema ljudi u redu</p>", unsafe_allow_html=True)
else:
    imena_u_redu = ", ".join([f"<b>{i+1}.</b> {ime}" for i, ime in enumerate(db["red"])])
