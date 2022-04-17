#!/usr/bin/env python
"""
Concatenate pages from pdf files into a single pdf file.

Page ranges refer to the previously-named file.
A file not followed by a page range means all the pages of the file.

PAGE RANGES are like Python slices.

        Remember, page indices start with zero.

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

EXAMPLES

    pdfcat -o output.pdf head.pdf content.pdf :6 7: tail.pdf -1

        Concatenate all of head.pdf, all but page seven of content.pdf,
        and the last page of tail.pdf, producing output.pdf.

    pdfcat chapter*.pdf >book.pdf

        You can specify the output file by redirection.

    pdfcat chapter?.pdf chapter10.pdf >book.pdf

        In case you don't want chapter 10 before chapter 2.

"""
# Copyright (c) 2014, Steve Witham <switham_github@mac-guyver.com>.
# All rights reserved. This software is available under a BSD license;
# see https://github.com/py-pdf/PyPDF2/LICENSE


import os
import traceback
from pathlib import Path
from sys import exit, stderr, stdout
from typing import List

from PyPDF2 import PdfFileMerger, parse_filename_page_ranges


def main(filename: Path, fn_pgrgs: List[str], output: Path, verbose: bool) -> None:
    fn_pgrgs_l = list(fn_pgrgs)
    fn_pgrgs_l.insert(0, str(filename))
    filename_page_ranges = parse_filename_page_ranges(fn_pgrgs_l)
    if output:
        output_fh = open(output, "wb")
    else:
        stdout.flush()
        output_fh = os.fdopen(stdout.fileno(), "wb")

    merger = PdfFileMerger()
    in_fs = dict()
    try:
        for (filename, page_range) in filename_page_ranges:
            if verbose:
                print(filename, page_range, file=stderr)
            if filename not in in_fs:
                in_fs[filename] = open(filename, "rb")
            merger.append(in_fs[filename], pages=page_range)
    except Exception:
        print(traceback.format_exc(), file=stderr)
        print(f"Error while reading {filename}", file=stderr)
        exit(1)
    merger.write(output_fh)
    output_fh.close()
    # In 3.0, input files must stay open until output is written.
    # Not closing the in_fs because this script exits now.
