"""
Extract text from PDF files, optionally restricted to specific pages.

Multiple files may be given, each optionally followed by a page range
that applies to the file named immediately before it. A file not
followed by a page range means all the pages of that file. Text is
printed in the order the files and page ranges are given.

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

Examples
    pdfly extract-text report.pdf

        Print the text of every page of report.pdf.

    pdfly extract-text report.pdf :5

        Print the text of the first five pages of report.pdf.

    pdfly extract-text intro.pdf :3 body.pdf -- -1

        Print the text of the first three pages of intro.pdf, followed
        by the text of the last page of body.pdf.

    pdfly extract-text report.pdf --output extracted.txt

        Write the extracted text to extracted.txt instead of stdout.

"""

import sys
from pathlib import Path

from pypdf import PdfReader
from rich.console import Console

from pdfly._utils import decrypt_or_exit
from pdfly.cat import parse_filepaths_and_pagerange_args


def main(
    filename: Path,
    fn_pgrgs: list[str] | None,
    output: Path | None = None,
    password: str | None = None,
) -> None:
    console = Console()
    filename_page_ranges = parse_filepaths_and_pagerange_args(
        console, filename, fn_pgrgs
    )

    if output:
        output_fh = open(output, "w", encoding="utf-8")
    else:
        output_fh = sys.stdout

    in_fs = {}
    try:
        for filepath, page_range in filename_page_ranges:
            if filepath not in in_fs:
                in_fs[filepath] = open(filepath, "rb")

            reader = PdfReader(in_fs[filepath])
            decrypt_or_exit(reader, password, Console())

            num_pages = len(reader.pages)
            start, end, _step = page_range.indices(num_pages)
            if (
                start < 0
                or end < 0
                or start >= num_pages
                or end > num_pages
                or start > end
            ):
                print(
                    f"WARNING: Page range {page_range} is out of bounds",
                    file=sys.stderr,
                )

            for page_num in range(*page_range.indices(num_pages)):
                text = reader.pages[page_num].extract_text()
                print(text, file=output_fh)
    finally:
        if output:
            output_fh.close()
        for fh in in_fs.values():
            fh.close()
