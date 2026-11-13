"""
Create a booklet-style PDF from a single input.

Pairs of two pages will be put on one page (left and right)

usage: python 2-up.py input_file output_file
"""

from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.generic import FloatObject


def main(pdf: Path, output: Path) -> None:
    reader = PdfReader(str(pdf))
    writer = PdfWriter()
    for i in range(0, len(reader.pages), 2):
        # pypdf >= 7 only allows merging into pages owned by a writer
        lhs = writer.add_page(reader.pages[i])
        if i + 1 < len(reader.pages):
            rhs = reader.pages[i + 1]
            lhs.merge_translated_page(
                rhs, tx=float(lhs.mediabox.width), ty=0, expand=True
            )
        else:
            # Double the MediaBox width:
            lhs.mediabox[2] = FloatObject(2 * lhs.mediabox[2])
        # Double the CropBox width:
        lhs.cropbox[2] = FloatObject(2 * lhs.cropbox[2])
    with open(output, "wb") as fp:
        writer.write(fp)
    print(f"{output} was created")
