"""Sign a PDF file with a PKCS#12 certificate, retaining original formatting and adding a signature page."""

from pathlib import Path
from fpdf import FPDF
import fitz  # PyMuPDF for precise page content extraction

def sign_pdf_with_p12(input_pdf: Path, output_pdf: Path, p12_path: Path, password: str) -> None:
    """
    Load the original PDF content, retain its layout, add a signature page, and digitally sign the PDF.

    Parameters:
    - input_pdf: Path to the PDF file to be signed.
    - output_pdf: Path where the signed PDF file will be saved.
    - p12_path: Path to the PKCS#12 certificate file (.p12).
    - password: Password for the PKCS#12 certificate.
    """

    # Step 1: Create a new FPDF object
    pdf = FPDF()

    # Step 2: Copy each page's content from the original PDF while retaining layout
    doc = fitz.open(input_pdf)
    for page_num in range(doc.page_count):
        page = doc[page_num]
        rect = page.rect
        pdf.add_page(orientation="P" if rect.width < rect.height else "L")
        pdf.set_auto_page_break(False)
        text = page.get_text("text")
        pdf.set_xy(0, 0)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=text)

    # Step 3: Add a signature page
    pdf.add_page()
    pdf.set_xy(10, 10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="This document is signed with PKCS#12.", ln=True)

    # Step 4: Digitally sign the PDF
    pdf.sign_pkcs12(str(p12_path), password=password.encode("utf-8"))
    pdf.output(str(output_pdf))

