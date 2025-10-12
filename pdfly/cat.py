"""
Concatenate pages from PDF files into a single PDF file.

Page ranges refer to the previously-named file.
A file not followed by a page range means all the pages of the file.

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
    pdfly cat -o output.pdf head.pdf -- content.pdf :6 7: tail.pdf -1

        Concatenate all of head.pdf, all but page seven of content.pdf,
        and the last page of tail.pdf, producing output.pdf.

    pdfly cat chapter*.pdf >book.pdf

        You can specify the output file by redirection.

    pdfly cat chapter?.pdf chapter10.pdf >book.pdf

        In case you don't want chapter 10 before chapter 2.

"""

# Copyright (c) 2014, Steve Witham <switham_github@mac-guyver.com>.
# All rights reserved. This software is available under a BSD license;
# see https://github.com/py-pdf/pypdf/LICENSE

import os
import sys
from pathlib import Path
from typing import Optional

from pypdf import PageRange, PdfReader, PdfWriter, parse_filename_page_ranges


def main(
    filename: Path,
    fn_pgrgs: list[str],
    output: Path,
    verbose: bool,
    inverted_page_selection: bool = False,
    password: Optional[str] = None,
) -> None:
    filename_page_ranges = parse_filepaths_and_pagerange_args(
        filename, fn_pgrgs
    )
    if output:
        output_fh = open(output, "wb")
    else:
        sys.stdout.flush()
        output_fh = os.fdopen(sys.stdout.fileno(), "wb")

    writer = PdfWriter()
    in_fs = {}
    try:
        for filepath, page_range in filename_page_ranges:  # type: ignore
            if verbose:
                print(filepath, page_range, file=sys.stderr)
            if filepath not in in_fs:
                in_fs[filepath] = open(filepath, "rb")

            reader = PdfReader(in_fs[filepath])
            if password is not None:
                reader.decrypt(password)
            num_pages = len(reader.pages)
            start, end, step = page_range.indices(num_pages)
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
            if inverted_page_selection:
                all_page_nums = set(range(len(reader.pages)))
                page_nums = set(range(*page_range.indices(len(reader.pages))))
                inverted_page_nums = all_page_nums - page_nums
                for page_num in inverted_page_nums:
                    writer.add_page(reader.pages[page_num])
            else:
                for page_num in range(*page_range.indices(len(reader.pages))):
                    writer.add_page(reader.pages[page_num])
        writer.write(output_fh)
    except Exception as error:
        raise RuntimeError(f"Error while reading {filename}") from error
    finally:
        output_fh.close()
    # In 3.0, input files must stay open until output is written.
    # Not closing the in_fs because this script exits now.


def parse_filepaths_and_pagerange_args(
    filename: Path, fn_pgrgs: list[str]
) -> list[tuple[Path, PageRange]]:
    fn_pgrgs_l = list(fn_pgrgs)
    fn_pgrgs_l.insert(0, str(filename))
    filename_page_ranges, invalid_filepaths = [], []
    for filepath, page_range in parse_filename_page_ranges(fn_pgrgs_l):  # type: ignore
        if Path(filepath).is_file():
            filename_page_ranges.append((Path(filepath), page_range))
        else:
            invalid_filepaths.append(str(filepath))
    if invalid_filepaths:
        print(
            f"Invalid file path or page range provided: {' '.join(invalid_filepaths)}",
            file=sys.stderr,
        )
        sys.exit(2)
    return filename_page_ranges
