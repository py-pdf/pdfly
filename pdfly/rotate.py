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
from typing import Generator, Tuple

from pypdf import (
    PageObject,
    PdfReader,
    PdfWriter,
)
from pypdf.generic import RectangleObject


def main(
    filename: Path,
    output: Path,
    page_range: str,
) -> None:
    try:
        # Set up the streams
        reader = PdfReader(filename)
        pages = list(reader.pages)
        writer = PdfWriter()

        # Reorder the pages and place two pages side by side (2-up) on each sheet
        for lhs, rhs in page_iter(len(pages)):
            pages[lhs].merge_translated_page(
                page2=pages[rhs],
                tx=pages[lhs].mediabox.width,
                ty=0,
                expand=True,
                over=True,
            )
            writer.add_page(pages[lhs])

        # Everything looks good! Write the output file.
        with open(output, "wb") as output_fh:
            writer.write(output_fh)

    except Exception:
        print(traceback.format_exc(), file=sys.stderr)
        print(f"Error while reading {filename}", file=sys.stderr)
        sys.exit(1)


def requires_rotate(a: RectangleObject, b: RectangleObject) -> bool:
    """
    Return True if a and b are rotated relative to each other.

    Args:
        a (RectangleObject): The first rectangle.
        b (RectangleObject): The second rectangle.

    """
    a_portrait = a.height > a.width
    b_portrait = b.height > b.width
    return a_portrait != b_portrait


def fetch_first_page(filename: Path) -> PageObject:
    """
    Fetch the first page of a PDF file.

    Args:
        filename (Path): The path to the PDF file.

    Returns:
        PageObject: The first page of the PDF file.

    """
    return PdfReader(filename).pages[0]


# This function written with inspiration, assistance, and code
# from claude.ai & Github Copilot
def page_iter(num_pages: int) -> Generator[Tuple[int, int], None, None]:
    """
    Generate pairs of page numbers for printing a booklet.
    This function assumes that the total number of pages is divisible by 4.
    It yields tuples of page numbers that should be printed on the same sheet
    of paper to create a booklet.

    Args:
        num_pages (int): The total number of pages in the document. Must be divisible by 4.

    Yields:
        Generator[Tuple[int, int], None, None]: Tuples containing pairs of page numbers.
            Each tuple represents the page numbers to be printed on one side of a sheet.

    Raises:
        ValueError: If the number of pages is not divisible by 4.

    """
    if num_pages % 4 != 0:
        raise ValueError("Number of pages must be divisible by 4")

    for sheet in range(num_pages // 4):
        # Outside the fold
        last_page = num_pages - sheet * 2 - 1
        first_page = sheet * 2

        # Inside the fold
        second_page = sheet * 2 + 1
        second_to_last_page = num_pages - sheet * 2 - 2

        yield last_page, first_page
        yield second_page, second_to_last_page
