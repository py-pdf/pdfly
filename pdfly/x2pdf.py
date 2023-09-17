"""Convert a file to PDF."""

from pathlib import Path

from fpdf import FPDF
from PIL import Image
from rich.console import Console


def px_to_mm(px: float) -> float:
    px_in_inch = 72
    mm_in_inch = 25.4
    inch = px / px_in_inch
    mm = inch * mm_in_inch
    return mm


def image_to_pdf(x: Path, output: Path) -> None:
    cover = Image.open(x)
    width: float
    height: float
    width, height = cover.size
    cover.close()
    width, height = px_to_mm(width), px_to_mm(height)

    pdf = FPDF(unit="mm", format=(width, height))
    pdf.add_page()
    pdf.image(x, x=0, y=0)
    pdf.output(str(output))


def main(x: Path, output: Path) -> int:
    console = Console()
    path_str = str(x).lower()
    if path_str.endswith(("doc", "docx", "odt")):
        console.print("[red]Error: Cannot convert Word documents to PDF")
        return -1
    image_to_pdf(x, output)
    return 0
