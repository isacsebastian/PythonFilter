
# utils.py
from fpdf import FPDF
import pandas as pd
import os

def generate_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Reporte Filtrado", ln=True, align='C')

    for row in data:
        pdf.cell(200, 10, txt=str(row), ln=True, align='L')

    file_path = os.path.join('data/processed', 'filtered_data.pdf')
    pdf.output(file_path)
    return file_path

def generate_csv(data):
    file_path = os.path.join('data/processed', 'filtered_data.csv')
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)
    return file_path