"""
Put each pair of pages side by side on one page.

Pages 1 and 2 become the left and right half of the first output page,
pages 3 and 4 the left and right half of the second one, and so on.
If the number of pages is odd, the right half of the last output page
stays blank. The page order is not changed; use `pdfly booklet` to
reorder the pages for booklet printing.

Example:
    pdfly 2-up input.pdf output.pdf

"""

from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.generic import FloatObject


def main(pdf: Path, output: Path) -> None:
    reader = PdfReader(str(pdf))
    writer = PdfWriter()
    for i in range(0, len(reader.pages), 2):
        # pypdf >= 7 only allows merging into pages owned by a writer
        lhs = writer.add_page(reader.pages[i])
        if i + 1 < len(reader.pages):
            rhs = reader.pages[i + 1]
            lhs.merge_translated_page(
                rhs, tx=float(lhs.mediabox.width), ty=0, expand=True
            )
        else:
            # Double the MediaBox width:
            lhs.mediabox[2] = FloatObject(2 * lhs.mediabox[2])
        # Double the CropBox width:
        lhs.cropbox[2] = FloatObject(2 * lhs.cropbox[2])
    with open(output, "wb") as fp:
        writer.write(fp)
    print(f"{output} was created")
