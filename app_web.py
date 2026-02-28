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

# --- FUNKCJA CZYSZCZENIA POLSKICH ZNAKÓW ---
def clean_pl(text):
    replacements = {
        'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n', 'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z',
        'Ą': 'A', 'Ć': 'C', 'Ę': 'E', 'Ł': 'L', 'Ń': 'N', 'Ó': 'O', 'Ś': 'S', 'Ź': 'Z', 'Ż': 'Z'
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

# --- FUNKCJA GENEROWANIA PDF ---
def generate_pdf(klient, uslugi, netto, vat, brutto, vat_rate):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 10, clean_pl(f"OFERTA REMONTOWA: {FIRMA}"), ln=True, align="C")
    
    pdf.set_font("helvetica", "", 12)
    pdf.ln(5)
    pdf.cell(0, 10, f"Data: {datetime.date.today().strftime('%d-%m-%Y')}", ln=True, align="R")
    pdf.cell(0, 10, clean_pl(f"Dla: {klient}"), ln=True)
    pdf.ln(10)

    pdf.set_fill_color(230, 230, 230)
    pdf.set_font("helvetica", "B", 10)
    pdf.cell(90, 10, "Usluga", border=1, fill=True)
    pdf.cell(20, 10, "Ilosc", border=1, fill=True, align="C")
    pdf.cell(35, 10, "Cena jedn.", border=1, fill=True, align="C")
    pdf.cell(45, 10, "Wartosc", border=1, fill=True, align="C")
    pdf.ln()

    pdf.set_font("helvetica", "", 10)
    for u in uslugi:
        pdf.cell(90, 10, clean_pl(u["Usługa"]), border=1)
        pdf.cell(20, 10, str(u["Ilość"]), border=1, align="C")
        pdf.cell(35, 10, clean_pl(u["Cena jedn."]), border=1, align="C")
        pdf.cell(45, 10, f"{u['Wartość']:.2f} zl", border=1, align="C")
        pdf.ln()

    pdf.ln(10)
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
    
    return pdf
