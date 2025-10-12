"""Compress a PDF."""

import shutil
from io import BytesIO
from pathlib import Path

from pypdf import PdfReader, PdfWriter


def main(pdf: Path, output: Path) -> None:
    reader = PdfReader(pdf)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    if reader.metadata:
        writer.add_metadata(reader.metadata)

    for page in writer.pages:
        page.compress_content_streams()

    # PDF to memory buffer first
    compressed_buffer = BytesIO()
    writer.write(compressed_buffer)
    compressed_data = compressed_buffer.getvalue()
    comp_size = len(compressed_data)

    orig_size = pdf.stat().st_size

    # If compressed size is larger than original, use original file
    if comp_size >= orig_size:
        print(
            f"Compression resulted in larger file ({comp_size:,} >= {orig_size:,} bytes)"
        )
        print("Keeping original file as compressed version would be larger")
        shutil.copy2(pdf, output)
        final_size = orig_size
        ratio = 100.0
        status = "No compression applied (would increase size)"
    else:
        with open(output, "wb") as fp:
            fp.write(compressed_data)
        final_size = comp_size
        ratio = (comp_size / orig_size) * 100
        status = f"Compressed ({ratio:.1f}% of original)"

    print(f"Original Size  : {orig_size:,}")
    print(f"Final Size     : {final_size:,} ({status})")
