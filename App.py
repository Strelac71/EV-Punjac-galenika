import streamlit as st
import datetime
import json
import os

# Podešavanje stranice za mobilne telefone
st.set_page_config(page_title="EV Punjač - Galenika", page_icon="⚡", layout="centered")

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

st.markdown("<h1 style='text-align: center; color: #1e293b; font-size: 28px; margin-bottom: 0;'>⚡ EV Punjači</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b; font-size: 18px; margin-top: 0;'>Lidl Galenika</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #22c55e; font-weight: bold; margin-top: -10px;'>✓ Online</p>", unsafe_allow_html=True)

db = st.session_state.db

# Popravka u letu ako je vreme povuklo zonu iz prošlog koda
if db["vreme_pocetka"] and hasattr(db["vreme_pocetka"], "tzinfo") and db["vreme_pocetka"].tzinfo is not None:
    db["vreme_pocetka"] = db["vreme_pocetka"].replace(tzinfo=None)

if db["slobodan"]:
    status_tekst, status_boja, status_bg = "Slobodan", "#22c55e", "#f0fdf4"
else:
    status_tekst, status_boja, status_bg = f"Zauzet ({db['korisnik']})", "#ef4444", "#fef2f2"

# Snaga 22kW + Dodata zvanična napomena o limitu od 1 sat
punjac_html = f"""
<div style="border: 2px solid #22c55e; border-radius: 12px; padding: 15px; background-color: white; margin-bottom: 10px;">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <h3 style="margin: 0; color: #1e293b; font-size: 18px;">EV Punjač Lidl Galenika</h3>
        <span style="background-color: {status_bg}; color: {status_boja}; border: 1px solid {status_boja}33; padding: 4px 10px; border-radius: 20px; font-weight: bold; font-size: 12px;">{status_tekst}</span>
    </div>
    <p style="margin: 8px 0 4px 0; color: #64748b; font-size: 14px;">📍 Galenika, Zemun</p>
    <p style="margin: 0 0 6px 0; color: #64748b; font-size: 14px;">🔋 22kW</p>
    <hr style="margin: 8px 0; border: 0; border-top: 1px dashed #cbd5e1;">
    <p style="margin: 0; color: #b45309; font-size: 12px; font-weight: bold; line-height: 1.4;">
        ⚠️ NAPOMENA: Molimo korisnike da punjač koriste maksimalno 1 sat, koliko i sam punjač fabrički dozvoljava. Budimo kolegijalni!
    </p>
</div>
"""
st.markdown(punjac_html, unsafe_allow_html=True)

if db["slobodan"]:
    st.markdown("<p style='font-size: 11px; font-weight: bold; color: #64748b; margin-bottom: 2px;'>UKUCAJ SVOJE IME IZ VIBER GRUPE:</p>", unsafe_allow_html=True)
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
    # OVAJ DEO KODA SE AUTOMATSKI OSVEŽAVA SVAKIH 30 SEKUNDI
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
            
        st.info(f"⚡ Zakačio/la se: **{db['korisnik']}** u **{vreme_kacenja}h**\n\n⏱️ Puni se već: **{vreme_prikaz}**")
        
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

broj_u_redu = len(db["red"])
st.markdown(f"""
<div style="border: 1px solid #e2e8f0; border-radius: 12px; padding: 15px; background-color: white; margin-bottom: 10px;">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 16px; font-weight: bold; color: #1e293b;">📋 Lista čekanja</span>
        <span style="background-color: #eff6ff; color: #3b82f6; padding: 2px 8px; border-radius: 50%; font-weight: bold; font-size: 12px;">{broj_u_redu}</span>
    </div>
</div>
""", unsafe_allow_html=True)

if broj_u_redu == 0:
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 14px;'>Nema ljudi u redu</p>", unsafe_allow_html=True)
else:
    for i, ime in enumerate(db["red"]):
        st.markdown(f"<div style='padding: 6px 12px; background: #f8fafc; border-radius: 6px; margin-bottom: 4px; font-size: 14px;'><b>{i+1}.</b> {ime}</div>", unsafe_allow_html=True)

if not db["slobodan"]:
    ime_za_listu = st.text_input("Tvoje ime za listu", placeholder="Unesi ime za red...", key="red_ime", label_visibility="collapsed")
    if st.button("+ Pridruži se redu", use_container_width=True):
        if ime_za_listu.strip() != "":
            db["red"].append(ime_za_listu)
            sacuvaj_bazu(db)
            st.rerun()

st.markdown("<style>.stButton > button { background-color: #22c55e !important; color: white !important; height: 44px !important; font-size: 15px !important; font-weight: bold !important; border-radius: 8px !important; }</style>", unsafe_allow_html=True)
