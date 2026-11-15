"""
Extract images from PDF without resampling or altering.

Adapted from work by Sylvain Pelissier
http://stackoverflow.com/questions/2693820/extract-images-from-pdf-without-resampling-in-python

Example:
    pdfly extract-images input.pdf
        Extract the images from all pages

    pdfly extract-images input.pdf --output-dir images
        Extract the images into the images directory

    pdfly extract-images input.pdf 2
        Extract the images from the third page only

    pdfly extract-images input.pdf 0:3
        Extract the images from the first three pages

    pdfly extract-images input.pdf -- -1
        Extract the images from the last page

PAGE RANGES are like Python slices: page indices start with zero.
When using page ranges that start with a negative value, a two-hyphen
symbol -- must be used to separate them from the command line options.

JPEG images are written exactly as they are embedded in the PDF, unless a
mask, a /Decode array or a color space like CMYK has to be applied to them.
Other images are converted to a common format like PNG or TIFF.

"""

from pathlib import Path

from pypdf import PageRange, PdfReader
from pypdf.generic import (
    ArrayObject,
    DictionaryObject,
    IndirectObject,
    NameObject,
    NumberObject,
    PdfObject,
    StreamObject,
)

# Color spaces for which a JPEG file looks the same as the image in the PDF
_JPEG_COLOR_SPACES = ("/DeviceGray", "/DeviceRGB")
_JPEG_COLOR_SPACE_FAMILIES = ("/CalGray", "/CalRGB")
_JPEG_ICC_COMPONENTS = (1, 3)


def main(
    pdf: Path, page_range: str = ":", output_dir: Path | None = None
) -> None:
    if output_dir is not None:
        output_dir.mkdir(parents=True, exist_ok=True)
    reader = PdfReader(str(pdf))
    page_indices = range(*PageRange(page_range).indices(len(reader.pages)))
    extracted_images: list[str] = []
    for page_index in page_indices:
        page0 = reader.pages[page_index]
        for image_file_object in page0.images:
            file_name = f"{page_index:04d}-{image_file_object.name}"
            path = (
                Path(file_name)
                if output_dir is None
                else output_dir / file_name
            )
            data = get_image_data(
                image_file_object.data, image_file_object.indirect_reference
            )
            with open(path, "wb") as fp:
                fp.write(data)
            extracted_images.append(str(path))

    if len(extracted_images) == 0:
        print("No image found.")
    else:
        print(f"Extracted {len(extracted_images)} images:")
        for extracted_path in extracted_images:
            print(f"- {extracted_path}")


def get_image_data(
    converted_data: bytes, indirect_reference: IndirectObject | None
) -> bytes:
    """
    Get the bytes of the image file to write.

    pypdf decodes every image with Pillow and encodes it again. For JPEG
    images, this changes the file even if the quality is kept. Hence the
    embedded JPEG is used as it is, if nothing has to be applied to it.

    Args:
        converted_data: The image file as converted by pypdf
        indirect_reference: The reference to the image XObject. It is None
            for inline images.

    Returns:
        The embedded JPEG file, if possible. Otherwise converted_data.

    """
    if indirect_reference is not None:
        x_object = indirect_reference.get_object()
        if isinstance(x_object, StreamObject) and is_unaltered_jpeg(x_object):
            return x_object.get_data()
    return converted_data


def is_unaltered_jpeg(x_object: StreamObject) -> bool:
    """
    Check if the stream of an image XObject is a JPEG file as displayed.

    This is the case if the last filter is /DCTDecode, no mask or /Decode
    array is applied, and the color space is a gray or RGB one.
    """
    filters = _resolve(x_object.get("/Filter"))
    if isinstance(filters, ArrayObject):
        filters = _resolve(filters[-1]) if filters else None
    if _name(filters) != "/DCTDecode":
        return False
    if any(key in x_object for key in ("/SMask", "/Mask", "/Decode")):
        return False
    return _is_gray_or_rgb(_resolve(x_object.get("/ColorSpace")))


def _is_gray_or_rgb(color_space: PdfObject | None) -> bool:
    if _name(color_space) in _JPEG_COLOR_SPACES:
        return True
    if not isinstance(color_space, ArrayObject) or not color_space:
        return False
    family = _name(_resolve(color_space[0]))
    if family in _JPEG_COLOR_SPACE_FAMILIES:
        return True
    if family == "/ICCBased" and len(color_space) > 1:
        icc_profile = _resolve(color_space[1])
        if isinstance(icc_profile, DictionaryObject):
            components = _resolve(icc_profile.get("/N"))
            return (
                isinstance(components, NumberObject)
                and int(components) in _JPEG_ICC_COMPONENTS
            )
    return False


def _resolve(obj: PdfObject | None) -> PdfObject | None:
    return None if obj is None else obj.get_object()


def _name(obj: PdfObject | None) -> str | None:
    return str(obj) if isinstance(obj, NameObject) else None
