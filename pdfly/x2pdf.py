"""Convert one or more files to PDF. Each file is a page."""

import re

from pathlib import Path
from typing import List

from fpdf import FPDF
from PIL import Image
from rich.console import Console

def get_page_size(format: str):
    """Get page dimensions based on format."""
    sizes = {
        "A4": (210, 297), "A3": (297, 420), "A2": (420, 594),
        "A1": (594, 841), "A0": (841, 1189), "Letter": (215.9, 279.4),
        "Legal": (215.9, 355.6)
    }
    match = re.match(r"(A\d|B\d|C\d|Letter|Legal)(-landscape)?$", format, re.IGNORECASE)
    if match:
        size_key = match.group(1).upper()
        if size_key in sizes:
            width, height = sizes[size_key]
            return (height, width) if match.group(2) else (width, height)
    raise ValueError(f"Invalid or unsupported page format provided: {format}")

def px_to_mm(px: float) -> float:
    px_in_inch = 72
    mm_in_inch = 25.4
    inch = px / px_in_inch
    mm = inch * mm_in_inch
    return mm


def image_to_pdf(pdf: FPDF, x: Path, page_size: tuple) -> None:
    cover = Image.open(x)
    width, height = cover.size
    cover.close()
    
    # Convert dimensions to millimeters
    width, height = px_to_mm(width), px_to_mm(height)
    page_width, page_height = page_size

    # Scale image to fit page size while maintaining aspect ratio
    scale_factor = min(page_width / width, page_height / height)
    scaled_width, scaled_height = width * scale_factor, height * scale_factor

    x_offset = (page_width - scaled_width) / 2
    y_offset = (page_height - scaled_height) / 2
    
    pdf.add_page(format=page_size)
    pdf.image(str(x), x=x_offset, y=y_offset, w=scaled_width, h=scaled_height)



def main(xs: List[Path], output: Path, format: str = None) -> int:
    """Main function to generate PDF with images fitted to specified page format."""
    console = Console()
    pdf = FPDF(unit="mm")
    page_size = get_page_size(format) if format else None
    for x in xs:
        path_str = str(x).lower()
        if path_str.endswith(("doc", "docx", "odt")):
            console.print(f"Skipping unsupported file format: {x}", style="yellow")
            continue
        try:
            image_to_pdf(pdf, x, page_size)
        except Exception as e:
            console.print(f"Error processing {x}: {e}", style="red")
            return 1
    pdf.output(str(output))
    console.print(f"PDF created successfully at {output}", style="green")
    return 0
