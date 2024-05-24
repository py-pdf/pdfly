"""Compress a PDF."""

from pathlib import Path

from pypdf import PdfReader, PdfWriter


def main(pdf: Path, output: Path) -> None:
    reader = PdfReader(pdf)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    for page in writer.pages:
        page.compress_content_streams()

    with open(output, "wb") as fp:
        writer.write(fp)

    orig_size = pdf.stat().st_size
    comp_size = output.stat().st_size
    ratio = comp_size / orig_size

    print(f"Original Size  : {orig_size:,}")
    print(f"Compressed Size: {comp_size:,} ({ratio * 100:2.1f}% of original)")
