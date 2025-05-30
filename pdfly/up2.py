"""
Create a booklet-style PDF from a single input.

Pairs of two pages will be put on one page (left and right)

usage: python 2-up.py input_file output_file
"""

import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter


def main(pdf: Path, output: Path) -> None:
    reader = PdfReader(str(pdf))
    writer = PdfWriter()
    for i in range(0, len(reader.pages) - 1, 2):
        lhs = reader.pages[i]
        rhs = reader.pages[i + 1]
        lhs.merge_translated_page(
            rhs, tx=float(lhs.mediabox.width), ty=0, expand=True
        )
        writer.add_page(lhs)
        sys.stdout.flush()

    with open(output, "wb") as fp:
        writer.write(fp)
    print(f"{output} was created")
