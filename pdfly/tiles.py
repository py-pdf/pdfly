"""
    Crope and merge PDF files into a single PDF as a layout of `xcount` x `ycount` tiles.

    Especially useful when layouting on A4 printable sticker paper.

    Currently only limited to A4 (portrait) input and output format.
    
    Use '-' to omit the file.
    
    `-x` and `-y` parameters specify the tiles size in relation to A4 format.

        A5: `-x 1 -y 2` (landscape)
        A6: `-x 2 -y 2` (portrait) - the default
        A7: `-x 2 -y 4` (landscape)
        A8: `-x 4 -y 4` (portrait)
        ...

    Examples
    
        pdfly tiles -o out.pdf -x 2 -y 2 A.pdf B.pdf C.pdf D.pdf

            Merge the top left (A6) corners of provided PDFs (A4) as A6 tiles into a single page (A4).
    
            A |        B |       C |       D |                  A | B
            --|--      --|--     --|--     --|--      ===>      --|--
              |          |         |         |                  C | D
    
              
        pdfly tiles -o out.pdf - A.pdf B.pdf C.pdf

            Omitting one position by using `-` (also omitted -x 2 -y 2 as those are by default).
    
            A |        B |       C |                   | A
            --|--      --|--     --|--     ===>      --|--
              |          |         |                 B | C
              
"""

# Stanislav Ulrych <stanislav.ulrych@gmail.com>.

import os
import sys
import traceback
from pathlib import Path
from typing import List

from pypdf import PdfReader, PdfWriter, Transformation, PaperSize


def main(
    output: Path, xcount: int, ycount: int, fn_pgrgs: List[str]
) -> None:
    if output:
        output_fh = open(output, "wb")
    else:
        sys.stdout.flush()
        output_fh = os.fdopen(sys.stdout.fileno(), "wb")

    xsize = PaperSize.A4.width
    ysize = PaperSize.A4.height

    writer = PdfWriter()
    destPage = writer.add_blank_page(width=xsize, height=ysize)
    try:
        for i in range(len(fn_pgrgs)):
            f = fn_pgrgs[i]
            if f == "-":
                continue

            reader = PdfReader(f)
            for p in reader.pages:
                t = {
                    "tx": (i % xcount)*(xsize/xcount),
                    "ty": -(i // xcount)*(ysize/ycount) 
                }
                print(t)
                p.add_transformation(Transformation().translate(**t))
                destPage.merge_page(p)

        writer.write(output_fh)
    except Exception:
        print(traceback.format_exc(), file=sys.stderr)
        print(f"Error while reading {f}", file=sys.stderr)
        sys.exit(1)
    finally:
        output_fh.close()
    # In 3.0, input files must stay open until output is written.
    # Not closing the in_fs because this script exits now.



