"""Module for uncompressing PDF content streams."""

import zlib
from pathlib import Path
from typing import Optional

from pypdf import PdfReader, PdfWriter
from pypdf.generic import IndirectObject, PdfObject


def main(pdf: Path, output: Path) -> None:
    reader = PdfReader(pdf)
    writer = PdfWriter()

    for page in reader.pages:
        if "/Contents" in page:
            contents: Optional[PdfObject] = page["/Contents"]
            if isinstance(contents, IndirectObject):
                contents = contents.get_object()
            if contents is not None:
                if isinstance(contents, list):
                    for content in contents:
                        if isinstance(content, IndirectObject):
                            decompress_content_stream(content)
                elif isinstance(contents, IndirectObject):
                    decompress_content_stream(contents)
        writer.add_page(page)

    with open(output, "wb") as fp:
        writer.write(fp)

    orig_size = pdf.stat().st_size
    uncomp_size = output.stat().st_size

    print(f"Original Size  : {orig_size:,}")
    print(
        f"Uncompressed Size: {uncomp_size:,} ({(uncomp_size / orig_size) * 100:.1f}% of original)"
    )


def decompress_content_stream(content: IndirectObject) -> None:
    """Decompress a content stream if it uses FlateDecode."""
    if content.get("/Filter") == "/FlateDecode":
        try:
            compressed_data = content.get_data()
            uncompressed_data = zlib.decompress(compressed_data)
            content.set_data(uncompressed_data)
            del content["/Filter"]
        except zlib.error as error:
            print(
                f"Some content stream with /FlateDecode failed to be decompressed: {error}"
            )
