"""
Reorder and two-up PDF pages for booklet printing.

If the number of pages is not a multiple of four, pages are
added until it is a multiple of four. This includes a centerfold
in the middle of the booklet and a single page on the inside
back cover. The content of those pages are from the
centerfold-file and blank-page-file files, if specified, otherwise
they are blank pages.

Example:
    pdfly booklet input.pdf output.pdf

"""

# Copyright (c) 2014, Steve Witham <switham_github@mac-guyver.com>.
# All rights reserved. This software is available under a BSD license;
# see https://github.com/py-pdf/pypdf/LICENSE

from collections.abc import Generator
from pathlib import Path
from typing import Optional

from pypdf import (
    PageObject,
    PdfReader,
    PdfWriter,
)
from pypdf.generic import RectangleObject


def main(
    filename: Path,
    output: Path,
    inside_cover_file: Optional[Path],
    centerfold_file: Optional[Path],
) -> None:
    try:
        # Set up the streams
        reader = PdfReader(filename)
        pages = list(reader.pages)
        writer = PdfWriter()

        # Add blank pages to make the number of pages a multiple of 4
        # If the user specified an inside-back-cover file, use it.
        blank_page = PageObject.create_blank_page(
            width=pages[0].mediabox.width, height=pages[0].mediabox.height
        )
        if len(pages) % 2 == 1:
            if inside_cover_file:
                ic_reader_page = fetch_first_page(inside_cover_file)
                pages.insert(-1, ic_reader_page)
            else:
                pages.insert(-1, blank_page)
        if len(pages) % 4 == 2:
            pages.insert(len(pages) // 2, blank_page)
            pages.insert(len(pages) // 2, blank_page)
            requires_centerfold = True
        else:
            requires_centerfold = False

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

        # If a centerfold was required, it is already
        # present as a pair of blank pages. If the user
        # specified a centerfold file, use it instead.
        if requires_centerfold and centerfold_file:
            centerfold_page = fetch_first_page(centerfold_file)
            last_page = writer.pages[-1]
            if centerfold_page.rotation != 0:
                centerfold_page.transfer_rotation_to_content()
            if requires_rotate(centerfold_page.mediabox, last_page.mediabox):
                centerfold_page = centerfold_page.rotate(270)
            if centerfold_page.rotation != 0:
                centerfold_page.transfer_rotation_to_content()
            last_page.merge_page(centerfold_page)

        # Everything looks good! Write the output file.
        with open(output, "wb") as output_fh:
            writer.write(output_fh)

    except Exception as error:
        raise RuntimeError(f"Error while processing {filename}") from error


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
def page_iter(num_pages: int) -> Generator[tuple[int, int], None, None]:
    """
    Generate pairs of page numbers for printing a booklet.
    This function assumes that the total number of pages is divisible by 4.
    It yields tuples of page numbers that should be printed on the same sheet
    of paper to create a booklet.

    Args:
        num_pages (int): The total number of pages in the document. Must be divisible by 4.

    Yields:
        Generator[tuple[int, int], None, None]: tuples containing pairs of page numbers.
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
