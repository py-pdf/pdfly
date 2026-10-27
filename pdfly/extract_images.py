"""
Extract images from PDF without resampling or altering.

Adapted from work by Sylvain Pelissier
http://stackoverflow.com/questions/2693820/extract-images-from-pdf-without-resampling-in-python
"""

from pathlib import Path

from pypdf import PageRange, PdfReader


def main(pdf: Path, pages: str | None = None) -> None:
    reader = PdfReader(str(pdf))
    if pages is None:
        page_numbers = range(len(reader.pages))
    else:
        page_numbers = range(*PageRange(pages).indices(len(reader.pages)))
    extracted_images = []
    for page_index in page_numbers:
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
