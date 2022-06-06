"""
Create a booklet-style PDF from a single input.

Pairs of two pages will be put on one page (left and right)

usage: python 2-up.py input_file output_file
"""

import sys
from pathlib import Path

from PyPDF2 import PdfReader, PdfWriter


def main(pdf: Path, output: Path) -> None:
    fh_read = open(pdf, "rb")
    reader = PdfReader(fh_read)
    writer = PdfWriter()
    for i in range(0, len(reader.pages) - 1, 2):
        lhs = reader.pages[i]
        rhs = reader.pages[i + 1]
        lhs.mergeTranslatedPage(rhs, float(lhs.mediabox.right), 0, True)
        writer.add_page(lhs)
        print(str(i) + " "),
        sys.stdout.flush()
    fh_read.close()

    print(f"writing {output}")
    with open(output, "wb") as fp:
        writer.write(fp)
    print("done.")
