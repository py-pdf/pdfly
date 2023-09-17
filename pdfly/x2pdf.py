"""Convert one or more files to PDF. Each file is a page."""

from pathlib import Path
from typing import List

from fpdf import FPDF
from PIL import Image
from rich.console import Console


def px_to_mm(px: float) -> float:
    px_in_inch = 72
    mm_in_inch = 25.4
    inch = px / px_in_inch
    mm = inch * mm_in_inch
    return mm


def image_to_pdf(pdf: FPDF, x: Path) -> None:
    cover = Image.open(x)
    width: float
    height: float
    width, height = cover.size
    cover.close()
    width, height = px_to_mm(width), px_to_mm(height)

    pdf.add_page(format=(width, height))
    pdf.image(x, x=0, y=0)


def main(xs: List[Path], output: Path) -> int:
    console = Console()
    for x in xs:
        path_str = str(x).lower()
        if path_str.endswith(("doc", "docx", "odt")):
            console.print("[red]Error: Cannot convert Word documents to PDF")
            return 1
        if not x.exists():
            console.print(f"[red]Error: File '{x}' does not exist.")
            return 2
    if output.exists():
        console.print(f"[red]Error: Output file '{output}' exist.")
        return 3
    pdf = FPDF(
        unit="mm",
    )
    for x in xs:
        path_str = str(x).lower()
        try:
            image_to_pdf(pdf, x)
        except Exception:
            console.print(f"[red]Error: Could not convert '{x}' to a PDF.")
    pdf.output(str(output))
    return 0
