import streamlit as st
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.graphics.barcode import code128
from io import BytesIO

st.set_page_config(page_title="Gerador de Etiquetas WMS", layout="centered")
st.title("Gerador de Etiquetas WMS")
st.write(
    "Gerador de Etiquetas 2.0"
)

uploaded_file = st.file_uploader("Selecione o arquivo Excel (.xlsx)", type="xlsx")
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    coluna_endereco = df.columns[0]

    if st.button("Gerar etiquetas"):
        output = BytesIO()
        largura_mm = 60
        altura_mm = 25
        largura_pt = largura_mm * mm
        altura_pt = altura_mm * mm
        c = canvas.Canvas(output, pagesize=(largura_pt, altura_pt))
        for _, row in df.iterrows():
            endereco_completo = str(row[coluna_endereco]).strip()
            endereco_visual = endereco_completo[5:]
            font_size = 32
            c.setFont("Helvetica-Bold", font_size)
            text_width = c.stringWidth(endereco_visual, "Helvetica-Bold", font_size)
            y_text = altura_pt - (altura_pt * 0.45)
            c.drawString((largura_pt - text_width) / 2, y_text, endereco_visual)
            espacamento = 3 * mm
            bar_height = 9 * mm
            barcode = code128.Code128(endereco_completo, barHeight=bar_height, barWidth=0.8)
            barcode_width = barcode.width
            x_barcode = (largura_pt - barcode_width) / 2
            y_barcode = y_text - espacamento - bar_height
            barcode.drawOn(c, x_barcode, y_barcode)
            c.showPage()
        c.save()
        output.seek(0)
        st.success("PDF gerado com sucesso!")
        st.download_button(
            label="Clique aqui para baixar o PDF",
            data=output,
            file_name="etiquetas_ajustadas.pdf",
            mime="application/pdf"
        )
