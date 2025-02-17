"""
Extract only the annotated pages from a PDF.

Q: Why does this help?
A: https://github.com/py-pdf/pdfly/issues/97
"""

from pathlib import Path
from typing import Optional

from pypdf import PdfReader, PdfWriter
from pypdf.annotations import AnnotationDictionary
from pypdf.generic import ArrayObject  # noqa: TCH002


# Check if an annotation is manipulable.
def is_manipulable(annot: AnnotationDictionary) -> bool:
    return annot.get("/Subtype") not in ["/Link"]


# Main function.
def main(input_pdf: Path, output_pdf: Optional[Path]) -> None:
    if not output_pdf:
        output_pdf = input_pdf.with_name(input_pdf.stem + "_annotated.pdf")
    input = PdfReader(input_pdf)
    output = PdfWriter()
    output_pages = 0
    # Copy only the pages with annotations
    for page in input.pages:
        if "/Annots" not in page:
            continue
        page_annots: ArrayObject = page["/Annots"]  # type: ignore[assignment]
        if not any(is_manipulable(annot) for annot in page_annots):
            continue
        output.add_page(page)
        output_pages += 1
    # Save the output PDF
    output.write(output_pdf)
    print(f"Extracted {output_pages} pages with annotations to {output_pdf}")
