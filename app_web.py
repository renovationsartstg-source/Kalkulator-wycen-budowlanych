import streamlit as st
import datetime
import pandas as pd

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="RenovationsArt - Kalkulator", page_icon="🏗️")

# --- DANE FIRMY I CENNIK ---
FIRMA = "RenovationsArt"
CENNIK = {
    "Stan Surowy": {
        "Wykop pod fundamenty (m3)": 75,
        "Wylanie ław (m2)": 140,
        "Murowanie nośne (m2)": 125,
        "Murowanie działowe (m2)": 62,
        "Wykonanie stropu (m2)": 107,
        "Więźba dachowa (m2)": 77,
        "Pokrycie dachu (m2)": 100
    },
    "Wykończenia": {
        "Tynkowanie maszynowe (m2)": 46,
        "Gładź gipsowa (m2)": 52,
        "Malowanie 2x (m2)": 28,
        "Sufit podwieszany G-K (m2)": 135,
        "Płytki standard (m2)": 135,
        "Gres wielki format (m2)": 210,
        "Panele podłogowe (m2)": 62,
        "Montaż drzwi wew. (szt)": 525
    },
    "Instalacje": {
        "Punkt elektryczny (szt)": 110,
        "Punkt wod-kan (szt)": 175,
        "Ogrzewanie podłogowe (m2)": 307,
        "Biały montaż WC/Umyw. (szt)": 200,
        "Biały montaż Wanna/Kab. (szt)": 500
    },
    "Wyburzenia i Inne": {
        "Skuwanie płytek (m2)": 55,
        "Wyburzanie ścian (m2)": 140,
        "Prace dodatkowe (h)": 90,
        "Utylizacja gruzu (szt)": 250
    }
}

st.title(f"🏗️ {FIRMA} - System Ofertowy")
st.markdown("Wprowadź dane, aby wygenerować profesjonalną ofertę dla klienta.")

# --- FORMULARZ ---
klient = st.text_input("Nazwa Klienta", placeholder="np. Jan Kowalski")
data_dzis = datetime.date.today().strftime("%d-%m-%Y")

wybrane_uslugi = []
suma_netto = 0

# Interfejs zakładek
tabs = st.tabs(list(CENNIK.keys()))

for i, kategoria in enumerate(CENNIK.keys()):
    with tabs[i]:
        st.subheader(f"Kategoria: {kategoria}")
        for usluga, cena in CENNIK[kategoria].items():
            # Używamy kolumn, aby interfejs był czysty
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"{usluga} (**{cena} zł**)")
            with col2:
                ilosc = st.number_input("Ilość", min_value=0.0, step=1.0, key=usluga)
            
            if ilosc > 0:
                wartosc = ilosc * cena
                wybrane_uslugi.append({
                    "Usługa": usluga,
                    "Ilość": ilosc,
                    "Cena jedn.": f"{cena} zł",
                    "Wartość": wartosc
                })
                suma_netto += wartosc

# --- PODSUMOWANIE I VAT ---
st.divider()
col_v1, col_v2 = st.columns(2)
with col_v1:
    vat_rate = st.radio("Stawka VAT", [8, 23], index=0, horizontal=True)

suma_vat = suma_netto * (vat_rate / 100)
suma_brutto = suma_netto + suma_vat

st.sidebar.header("Podsumowanie Finansowe")
st.sidebar.write(f"**Netto:** {suma_netto:,.2f} zł")
st.sidebar.write(f"**VAT ({vat_rate}%):** {suma_vat:,.2f} zł")
st.sidebar.subheader(f"**BRUTTO: {suma_brutto:,.2f} zł**")

# --- GENEROWANIE RAPORTU ---
if st.button("Przygotuj ofertę do pobrania"):
    if not klient:
        st.error("Proszę podać nazwę klienta!")
    elif suma_netto == 0:
        st.warning("Nie wybrano żadnych usług!")
    else:
        raport = f"OFERTA FIRMY: {FIRMA}\nDLA KLIENTA: {klient}\nDATA: {data_dzis}\n"
        raport += "="*40 + "\n\n"
        
        for item in wybrane_uslugi:
            raport += f"- {item['Usługa']}\n  {item['Ilość']} x {item['Cena jedn.']} = {item['Wartość']:.2f} zł\n"
        
        raport += "\n" + "="*40 + "\n"
        raport += f"SUMA NETTO: {suma_netto:,.2f} zł\n"
        raport += f"VAT {vat_rate}%: {suma_vat:,.2f} zł\n"
        raport += f"KWOTA BRUTTO: {suma_brutto:,.2f} zł\n"
        raport += "="*40 + "\n"
        raport += "\n* Ważność oferty: 30 dni.\n* Dokument wygenerowany automatycznie."

        st.text_area("Podgląd oferty", raport, height=300)
        
        st.download_button(
            label="Pobierz plik tekstowy (.txt)",
            data=raport,
            file_name=f"Oferta_{klient}_{data_dzis}.txt",
            mime="text/plain"
        )