from fpdf import FPDF
import io

def generate_pdf(klient, uslugi, netto, vat_rate, brutto):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    
    # Nagłówek
    pdf.cell(0, 10, "OFERTA REMONTOWA - RenovationsArt", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Data: {datetime.date.today().strftime('%d-%m-%Y')}", ln=True, align="R")
    pdf.cell(0, 10, f"Dla: {klient}", ln=True)
    pdf.ln(10)

    # Tabela - Nagłówki
    pdf.set_fill_color(200, 220, 255)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(90, 10, "Usluga", border=1, fill=True)
    pdf.cell(30, 10, "Ilosc", border=1, fill=True, align="C")
    pdf.cell(30, 10, "Cena jedn.", border=1, fill=True, align="C")
    pdf.cell(40, 10, "Wartosc", border=1, fill=True, align="C")
    pdf.ln()

    # Tabela - Dane
    pdf.set_font("Arial", "", 10)
    for u in uslugi:
        pdf.cell(90, 10, u["Usługa"], border=1)
        pdf.cell(30, 10, str(u["Ilość"]), border=1, align="C")
        pdf.cell(30, 10, u["Cena jedn."], border=1, align="C")
        pdf.cell(40, 10, f"{u['Wartość']:.2f} zl", border=1, align="C")
        pdf.ln()

    pdf.ln(5)
    # Podsumowanie
    pdf.set_font("Arial", "B", 12)
    pdf.cell(150, 10, "RAZEM NETTO:", align="R")
    pdf.cell(40, 10, f"{netto:,.2f} zl", align="C")
    pdf.ln()
    pdf.cell(150, 10, f"VAT {vat_rate}%:", align="R")
    pdf.cell(40, 10, f"{(brutto-netto):,.2f} zl", align="C")
    pdf.ln()
    pdf.set_fill_color(255, 255, 0)
    pdf.cell(150, 10, "DO ZAPLATY BRUTTO:", align="R")
    pdf.cell(40, 10, f"{brutto:,.2f} zl", border=1, fill=True, align="C")

    # Zapis do pamięci zamiast do pliku
    return pdf.output(dest='S').encode('latin-1')

# --- PRZYCISK W STREAMLIT ---
if st.button("Generuj profesjonalny PDF"):
    if not klient:
        st.error("Wpisz nazwę klienta!")
    elif not wybrane_uslugi:
        st.warning("Wybierz przynajmniej jedną usługę!")
    else:
        pdf_data = generate_pdf(klient, wybrane_uslugi, suma_netto, vat_rate, suma_brutto)
        st.download_button(
            label="Pobierz Ofertę PDF",
            data=pdf_data,
            file_name=f"Oferta_{klient}.pdf",
            mime="application/pdf"
        )
