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
        # Lucas: expand=True triggers a mediabox size update in PageObject._expand_mediabox(),
        #        but sometimes the cropbox is also update in the process, sometimes it doesn't.
        #        I haven't investigated why, but maybe because those attributes are properties
        #        created with _create_rectangle_accessor().
        #        Anyway, for now I prefer to ensure that the cropbox matches the mediabox:
        lhs.cropbox = lhs.mediabox
        writer.add_page(lhs)
        sys.stdout.flush()
    with open(output, "wb") as fp:
        writer.write(fp)
    print(f"{output} was created")
