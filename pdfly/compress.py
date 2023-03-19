"""Compress a PDF."""

import os
from pathlib import Path

from pypdf import PdfReader, PdfWriter


def main(pdf: Path, output: Path) -> None:
    reader = PdfReader(pdf)
    writer = PdfWriter()
    for page in reader.pages:
        page.compress_content_streams()
        writer.add_page(page)

    with open(output, "wb") as fp:
        writer.write(fp)

    orig_size = os.path.getsize(pdf)
    comp_size = os.path.getsize(output)
    ratio = comp_size / orig_size

    print(f"Original Size  : {orig_size:,}")
    print(f"Compressed Size: {comp_size:,} ({ratio * 100:2.1f}% of original)")
