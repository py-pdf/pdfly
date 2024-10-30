"""Convert one or more files to PDF. Each file is a page."""

import re

from pathlib import Path
from typing import List

from fpdf import FPDF
from PIL import Image
from rich.console import Console

def get_page_size(format: str):
    if format.lower() == 'letter':
        return (215.9, 279.4)
    elif format.lower() == 'a4-portrait':
        return (210, 297)
    elif format.lower() == 'a4-landscape':
        return (297, 210)
    else:
        match = re.match(r"(\d+)x(\d+)", format)
        if match:
            return float(match.group(1)), float(match.group(2))
        else:
            raise ValueError(f"Invalid format: {format}")

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



def main(xs: List[Path], output: Path, format: str = 'A4-portrait') -> int:
    console = Console()
    pdf = FPDF()

    # Retrieve the page size based on format
    page_size = get_page_size(format)

    for x in xs:
        path_str = str(x).lower()
        if path_str.endswith(("doc", "docx", "odt")):
            console.print(f"Skipping unsupported file format: {x}", style="yellow")
            continue
        try:
            image_to_pdf(pdf, x, page_size)
        except Exception as e:
            console.print(f"Error processing {x}: {e}", style="red")

    pdf.output(str(output))
    console.print(f"PDF created successfully at {output}", style="green")
    return 0
