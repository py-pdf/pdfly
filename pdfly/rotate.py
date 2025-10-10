"""
Rotate specified pages by the specified amount

Example:
    pdfly rotate --output output.pdf input.pdf 90
        Rotate all pages by 90 degrees (clockwise)

    pdfly rotate --output output.pdf input.pdf 90 :3
        Rotate first three pages by 90 degrees (clockwise)

    pdfly rotate --output output.pdf input.pdf 90 -- -1
        Rotate last page by 90 degrees (clockwise)

A file not followed by a page range (PGRGS) means all the pages of the file.

PAGE RANGES are like Python slices.

        Remember, page indices start with zero.

        When using page ranges that start with a negative value a
        two-hyphen symbol -- must be used to separate them from
        the command line options.

        Page range expression examples:

            :     all pages.                   -1    last page.
            22    just the 23rd page.          :-1   all but the last page.
            0:3   the first three pages.       -2    second-to-last page.
            :3    the first three pages.       -2:   last two pages.
            5:    from the sixth page onward.  -3:-1 third & second to last.

        The third, "stride" or "step" number is also recognized.

            ::2       0 2 4 ... to the end.    3:0:-1    3 2 1 but not 0.
            1:10:2    1 3 5 7 9                2::-1     2 1 0.
            ::-1      all pages in reverse order.


"""

from pathlib import Path

from pypdf import (
    PageRange,
    PdfReader,
    PdfWriter,
)
from rich.console import Console


def main(
    filename: Path,
    output: Path,
    degrees: int,
    page_range: str,
) -> None:
    try:
        # set up the streams
        reader = PdfReader(filename)
        pages = list(reader.pages)
        writer = PdfWriter()

        # Convert the page range into a set of page numbers
        pages_to_rotate = convert_range_to_pages(page_range, len(pages))

        for page_index, page in enumerate(pages):
            if page_index in pages_to_rotate:
                page = page.rotate(degrees)
            writer.add_page(page)

        # Everything looks good! Write the output file.
        with open(output, "wb") as output_fh:
            writer.write(output_fh)

    except Exception as error:
        console = Console()
        console.print(f"Error while rotating {filename}")
        raise error


def convert_range_to_pages(page_range: str, num_pages: int) -> set[int]:
    pages_to_rotate = {*range(*PageRange(page_range).indices(num_pages))}
    return pages_to_rotate
