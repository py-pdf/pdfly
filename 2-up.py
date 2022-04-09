"""
Create a booklet-style PDF from a single input.

Pairs of two pages will be put on one page (left and right)

usage: python 2-up.py input_file output_file
"""

import sys

from PyPDF2 import PdfFileReader, PdfFileWriter


def main():
    if len(sys.argv) != 3:
        print("usage: python 2-up.py input_file output_file")
        sys.exit(1)
    print("2-up input " + sys.argv[1])
    fh_read = open(sys.argv[1], "rb")
    reader = PdfFileReader(fh_read)
    writer = PdfFileWriter()
    for i in range(0, reader.getNumPages() - 1, 2):
        lhs = reader.pages[i]
        rhs = reader.pages[i + 1]
        lhs.mergeTranslatedPage(rhs, lhs.mediaBox.getUpperRight_x(), 0, True)
        writer.addPage(lhs)
        print(str(i) + " "),
        sys.stdout.flush()
    fh_read.close()

    print(f"writing {sys.argv[2]}")
    with open(sys.argv[2], "wb") as fp:
        writer.write(fp)
    print("done.")


if __name__ == "__main__":
    main()
