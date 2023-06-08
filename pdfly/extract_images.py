"""
Extract images from PDF without resampling or altering.

Adapted from work by Sylvain Pelissier
http://stackoverflow.com/questions/2693820/extract-images-from-pdf-without-resampling-in-python
"""

from pathlib import Path

from pypdf import PdfReader


def main(pdf: Path) -> None:
    reader = PdfReader(str(pdf))
    extracted_images = []
    for page_index, page0 in enumerate(reader.pages):
        for image_file_object in page0.images:
            path = f"{page_index}-{image_file_object.name}"
            with open(path, "wb") as fp:
                fp.write(image_file_object.data)
            extracted_images.append(path)

    if len(extracted_images) == 0:
        print("No image found.")
    else:
        print(f"Extracted {len(extracted_images)} images:")
        for path in extracted_images:
            print(f"- {path}")
