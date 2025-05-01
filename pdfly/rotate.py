"""
Rotate specified pages by the specified amount

Example:
    pdfly rotate input.pdf output.pdf

"""

# Copyright (c) 2014, Steve Witham <switham_github@mac-guyver.com>.
# All rights reserved. This software is available under a BSD license;
# see https://github.com/py-pdf/pypdf/LICENSE

import sys
import traceback
from pathlib import Path
from typing import Set

from pypdf import (
    PageRange,
    PdfReader,
    PdfWriter,
)


def main(
    filename: Path,
    output: Path,
    degrees: int,
    page_range: str,
) -> None:
    try:
        # Set up the streams
        reader = PdfReader(filename)
        pages = list(reader.pages)
        writer = PdfWriter()

        # Convert the page range into a set of page numbers
        pages_to_rotate = convert_range_to_pages(page_range, len(pages))

        for page_index, page in enumerate(pages):
            if page_index in pages_to_rotate:
                writer.add_page(page.rotate(degrees))
            else:
                writer.add_page(page)

        # Everything looks good! Write the output file.
        if True:
            with open(output, "wb") as output_fh:
                writer.write(output_fh)

    except Exception:
        print(traceback.format_exc(), file=sys.stderr)
        print(f"Error while reading {filename}", file=sys.stderr)
        sys.exit(1)


def convert_range_to_pages(page_range: str, num_pages: int) -> Set[int]:
    pages_to_rotate = {*range(*PageRange(page_range).indices(num_pages))}
    return pages_to_rotate
