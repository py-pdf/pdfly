"""
Extract images from PDF without resampling or altering.

Adapted from work by Sylvain Pelissier
http://stackoverflow.com/questions/2693820/extract-images-from-pdf-without-resampling-in-python

Example:
    pdfly extract-images input.pdf
        Extract the images from all pages

    pdfly extract-images input.pdf 2
        Extract the images from the third page only

    pdfly extract-images input.pdf 0:3
        Extract the images from the first three pages

    pdfly extract-images input.pdf -- -1
        Extract the images from the last page

PAGE RANGES are like Python slices: page indices start with zero.
When using page ranges that start with a negative value, a two-hyphen
symbol -- must be used to separate them from the command line options.

"""

from pathlib import Path

from pypdf import PageRange, PdfReader


def main(pdf: Path, page_range: str = ":") -> None:
    reader = PdfReader(str(pdf))
    page_indices = range(*PageRange(page_range).indices(len(reader.pages)))
    extracted_images = []
    for page_index in page_indices:
        page0 = reader.pages[page_index]
        for image_file_object in page0.images:
            path = f"{page_index:04d}-{image_file_object.name}"
            with open(path, "wb") as fp:
                fp.write(image_file_object.data)
            extracted_images.append(path)

    if len(extracted_images) == 0:
        print("No image found.")
    else:
        print(f"Extracted {len(extracted_images)} images:")
        for path in extracted_images:
            print(f"- {path}")
