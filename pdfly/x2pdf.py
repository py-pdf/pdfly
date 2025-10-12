"""Convert one or more files to PDF. Each file is a page."""

from io import BytesIO
from pathlib import Path

from fpdf import FPDF
from PIL import Image
from pypdf import PdfReader, PdfWriter
from rich.console import Console


def px_to_mm(px: float) -> float:
    px_in_inch = 72
    mm_in_inch = 25.4
    inch = px / px_in_inch
    mm = inch * mm_in_inch
    return mm


def image_to_pdf(filepath: Path) -> BytesIO:
    with Image.open(filepath) as cover:
        width, height = cover.size
    width, height = px_to_mm(width), px_to_mm(height)
    pdf = FPDF(unit="mm")
    pdf.add_page(format=(width, height))
    pdf.image(filepath, x=0, y=0)
    return BytesIO(pdf.output())


def main(in_filepaths: list[Path], out_filepath: Path) -> int:
    console = Console()
    exit_code = 0
    writer = PdfWriter()
    for filepath in in_filepaths:
        if filepath.name.endswith(".pdf"):
            for page in PdfReader(filepath).pages:
                writer.insert_page(page)
            continue
        try:
            pdf_bytes = image_to_pdf(filepath)
            new_page = PdfReader(pdf_bytes).pages[0]
            writer.insert_page(new_page)
        except Exception:
            console.print(
                f"[red]Error: Could not convert '{filepath}' to a PDF."
            )
            console.print_exception(extra_lines=1, max_frames=1)
            exit_code += 1
    writer.write(out_filepath)
    return exit_code
