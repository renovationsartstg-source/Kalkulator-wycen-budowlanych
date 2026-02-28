import streamlit as st
import datetime
from fpdf import FPDF

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

# --- FUNKCJA CZYSZCZENIA POLSKICH ZNAKÓW DLA PDF ---
def clean_pl(text):
    replacements = {
        'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n', 'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z',
        'Ą': 'A', 'Ć': 'C', 'Ę': 'E', 'Ł': 'L', 'Ń': 'N', 'Ó': 'O', 'Ś': 'S', 'Ź': 'Z', 'Ż': 'Z'
    }
    for k, v in replacements.items():
        text = str(text).replace(k, v)
    return text

# --- FUNKCJA GENEROWANIA PDF ---
def generate_pdf(klient, uslugi, netto, vat, brutto, vat_rate):
    pdf = FPDF()
    pdf.add_page()
    
    # Nagłówek
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 10, clean_pl(f"OFERTA REMONTOWA: {FIRMA}"), ln=True, align="C")
    
    pdf.set_font("helvetica", "", 12)
    pdf.ln(5)
    pdf.cell(0, 10, f"Data: {datetime.date.today().strftime('%d-%m-%Y')}", ln=True, align="R")
    pdf.cell(0, 10, clean_pl(f"Dla: {klient}"), ln=True)
    pdf.ln(10)

    # Tabela Nagłówki
    pdf.set_fill_color(230, 230, 230)
    pdf.set_font("helvetica", "B", 10)
    pdf.cell(90, 10, "Usluga", border=1, fill=True)
    pdf.cell(20, 10, "Ilosc", border=1, fill=True, align="C")
    pdf.cell(35, 10, "Cena jedn.", border=1, fill=True, align="C")
    pdf.cell(45, 10, "Wartosc", border=1, fill=True, align="C")
    pdf.ln()

    # Tabela Dane
    pdf.set_font("helvetica", "", 10)
    for u in uslugi:
        pdf.cell(90, 10, clean_pl(u["Usługa"]), border=1)
        pdf.cell(20, 10, str(u["Ilość"]), border=1, align="C")
        pdf.cell(35, 10, clean_pl(u["Cena jedn."]), border=1, align="C")
        pdf.cell(45, 10, f"{u['Wartość']:.2f} zl", border=1, align="C")
        pdf.ln()

    pdf.ln(10)
    
    # Podsumowanie
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(145, 10, "Suma Netto:", align="R")
    pdf.cell(45, 10, f"{netto:,.2f} zl", align="R")
    pdf.ln()
    pdf.cell(145, 10, f"VAT ({vat_rate}%):", align="R")
    pdf.cell(45, 10, f"{vat:,.2f} zl", align="R")
    pdf.ln()
    pdf.set_fill_color(255, 255, 0)
    pdf.cell(145, 10, "KWOTA BRUTTO:", align="R")
    pdf.cell(45, 10, f"{brutto:,.2f} zl", border=1, fill=True, align="R")
    
    return pdf.output()

# --- INTERFEJS UŻYTKOWNIKA ---
st.title(f"🏗️ {FIRMA} - System Ofertowy")
st.markdown("Wprowadź dane, aby wygenerować profesjonalną ofertę.")

klient = st.text_input("Nazwa Klienta", placeholder="np. Jan Kowalski")
data_dzis = datetime.date.today().strftime("%d-%m-%Y")

wybrane_uslugi = []
suma_netto = 0

tabs = st.tabs(list(CENNIK.keys()))

for i, kategoria in enumerate(CENNIK.keys()):
    with tabs[i]:
        st.subheader(f"Kategoria: {kategoria}")
        for usluga, cena in CENNIK[kategoria].items():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"{usluga} (**{cena} zł**)")
            with col2:
                # Klucz unikalny dla każdego pola (input_kategoria_usluga)
                ilosc = st.number_input("Ilość", min_value=0.0, step=1.0, key=f"in_{kategoria}_{usluga}")
            
            if ilosc > 0:
                wartosc = ilosc * cena
                wybrane_uslugi.append({
                    "Usługa": usluga,
                    "Ilość": ilosc,
                    "Cena jedn.": f"{cena} zł",
                    "Wartość": wartosc
                })
                suma_netto += wartosc

st.divider()
vat_rate = st.radio("Stawka VAT", [8, 23], index=0, horizontal=True)

suma_vat = suma_netto * (vat_rate / 100)
suma_brutto = suma_netto + suma_vat

st.sidebar.header("Podsumowanie Finansowe")
st.sidebar.write(f"**Netto:** {suma_netto:,.2f} zł")
st.sidebar.write(f"**VAT ({vat_rate}%):** {suma_vat:,.2f} zł")
st.sidebar.subheader(f"**BRUTTO: {suma_brutto:,.2f} zł**")

# --- GENEROWANIE OFERTY ---
if st.button("Przygotuj ofertę do pobrania"):
    if not klient:
        st.error("Proszę podać nazwę klienta!")
    elif suma_netto == 0:
        st.warning("Nie wybrano żadnych usług!")
    else:
        try:
            # Generowanie danych PDF
            pdf_data = generate_pdf(klient, wybrane_uslugi, suma_netto, suma_vat, suma_brutto, vat_rate)
            
            # Konwersja do bytes() naprawia błąd Invalid binary data format
            pdf_bytes = bytes(pdf_data)
            
            st.success("Oferta PDF gotowa!")
            st.download_button(
                label="📥 Pobierz Ofertę PDF",
                data=pdf_bytes,
                file_name=f"Oferta_{klient}_{data_dzis}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Błąd podczas generowania: {e}")
