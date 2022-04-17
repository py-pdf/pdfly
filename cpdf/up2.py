"""
Create a booklet-style PDF from a single input.

Pairs of two pages will be put on one page (left and right)

usage: python 2-up.py input_file output_file
"""

import sys
from pathlib import Path

from PyPDF2 import PdfFileReader, PdfFileWriter


def main(pdf: Path, output: Path) -> None:
    fh_read = open(pdf, "rb")
    reader = PdfFileReader(fh_read)
    writer = PdfFileWriter()
    for i in range(0, reader.getNumPages() - 1, 2):
        lhs = reader.pages[i]
        rhs = reader.pages[i + 1]
        lhs.mergeTranslatedPage(rhs, lhs.mediaBox.getUpperRight_x(), 0, True)
        writer.addPage(lhs)
        print(str(i) + " "),
        sys.stdout.flush()
    fh_read.close()

    print(f"writing {output}")
    with open(output, "wb") as fp:
        writer.write(fp)
    print("done.")
