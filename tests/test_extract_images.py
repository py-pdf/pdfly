from contextlib import chdir
from pathlib import Path

import pytest
from PIL import Image
from pypdf import PdfWriter
from pypdf.generic import (
    ArrayObject,
    DecodedStreamObject,
    DictionaryObject,
    NameObject,
    NullObject,
    NumberObject,
    PdfObject,
)

from pdfly.extract_images import get_image_data, is_unaltered_jpeg

from .conftest import RESOURCES_ROOT, run_cli


def test_extract_images_jpg_png(
    capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    with chdir(tmp_path):
        run_cli(
            [
                "extract-images",
                str(RESOURCES_ROOT / "GeoBase_NHNC1_Data_Model_UML_EN.pdf"),
            ]
        )
    captured = capsys.readouterr()
    assert not captured.err
    assert "Extracted 3 images" in captured.out


def test_extract_images_monochrome(
    capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    # There used to be a bug for this case: https://github.com/py-pdf/pypdf/issues/2176
    with chdir(tmp_path):
        run_cli(["extract-images", str(RESOURCES_ROOT / "box.pdf")])
    captured = capsys.readouterr()
    assert not captured.err
    assert "Extracted 1 images" in captured.out


def test_extract_images_custom_output_dir(
    capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    output_dir = tmp_path / "new" / "images"
    run_cli(
        [
            "extract-images",
            str(RESOURCES_ROOT / "box.pdf"),
            "--output-dir",
            str(output_dir),
        ]
    )
    captured = capsys.readouterr()
    assert not captured.err
    assert output_dir.is_dir()
    assert "- " + str(output_dir) in captured.out
    assert len(list(output_dir.iterdir())) == 1


@pytest.mark.parametrize(
    ("page_range", "expected"),
    [
        ("0", "Extracted 2 images"),
        ("8", "Extracted 1 images"),
        ("1:8", "No image found."),
        ("-11:", "Extracted 1 images"),
        (":", "Extracted 3 images"),
    ],
)
def test_extract_images_page_range(
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
    page_range: str,
    expected: str,
) -> None:
    with chdir(tmp_path):
        run_cli(
            [
                "extract-images",
                str(RESOURCES_ROOT / "GeoBase_NHNC1_Data_Model_UML_EN.pdf"),
                "--",
                page_range,
            ]
        )
    captured = capsys.readouterr()
    assert not captured.err
    assert expected in captured.out
    if page_range == "8":
        assert all(p.name.startswith("0008-") for p in tmp_path.iterdir())


@pytest.mark.parametrize("mode", ["RGB", "L"])
def test_extract_images_keeps_jpeg_unchanged(
    capsys: pytest.CaptureFixture[str], tmp_path: Path, mode: str
) -> None:
    # https://github.com/py-pdf/pdfly/issues/200
    jpeg_path = tmp_path / "in.jpg"
    with Image.open(RESOURCES_ROOT / "baleines.jpg") as image:
        image.convert(mode).save(jpeg_path, quality=99)
    pdf_path = tmp_path / "out.pdf"
    run_cli(["x2pdf", str(jpeg_path), "-o", str(pdf_path)])
    output_dir = tmp_path / "images"

    run_cli(["extract-images", str(pdf_path), "--output-dir", str(output_dir)])

    assert "Extracted 1 images" in capsys.readouterr().out
    (extracted_path,) = output_dir.iterdir()
    assert extracted_path.suffix == ".jpg"
    assert extracted_path.read_bytes() == jpeg_path.read_bytes()


def test_extract_images_converts_jpeg_with_soft_mask(tmp_path: Path) -> None:
    # The JPEG in this file has an /SMask, which pypdf has to apply
    run_cli(
        [
            "extract-images",
            str(RESOURCES_ROOT / "jpeg.pdf"),
            "--output-dir",
            str(tmp_path),
        ]
    )

    (extracted_path,) = tmp_path.iterdir()
    assert extracted_path.suffix == ".jp2"


def _image_stream(**entries: PdfObject) -> DecodedStreamObject:
    stream = DecodedStreamObject()
    stream.set_data(b"embedded JPEG")
    stream.update(
        {NameObject(f"/{key}"): value for key, value in entries.items()}
    )
    return stream


DCT = NameObject("/DCTDecode")
RGB = NameObject("/DeviceRGB")


def _icc_based(components: PdfObject) -> ArrayObject:
    profile = DictionaryObject({NameObject("/N"): components})
    return ArrayObject([NameObject("/ICCBased"), profile])


@pytest.mark.parametrize(
    ("stream", "expected"),
    [
        (_image_stream(Filter=DCT, ColorSpace=RGB), True),
        (
            _image_stream(Filter=DCT, ColorSpace=NameObject("/DeviceGray")),
            True,
        ),
        (
            _image_stream(
                Filter=ArrayObject([NameObject("/FlateDecode"), DCT]),
                ColorSpace=RGB,
            ),
            True,
        ),
        (
            _image_stream(
                Filter=DCT,
                ColorSpace=ArrayObject(
                    [NameObject("/CalRGB"), DictionaryObject()]
                ),
            ),
            True,
        ),
        (
            _image_stream(Filter=DCT, ColorSpace=_icc_based(NumberObject(3))),
            True,
        ),
        (
            _image_stream(Filter=DCT, ColorSpace=_icc_based(NumberObject(1))),
            True,
        ),
        # Not a JPEG
        (_image_stream(ColorSpace=RGB), False),
        (
            _image_stream(Filter=NameObject("/FlateDecode"), ColorSpace=RGB),
            False,
        ),
        (
            _image_stream(
                Filter=ArrayObject([DCT, NameObject("/FlateDecode")]),
                ColorSpace=RGB,
            ),
            False,
        ),
        (_image_stream(Filter=ArrayObject(), ColorSpace=RGB), False),
        # Something has to be applied to the JPEG
        (_image_stream(Filter=DCT, ColorSpace=RGB, SMask=NullObject()), False),
        (_image_stream(Filter=DCT, ColorSpace=RGB, Mask=ArrayObject()), False),
        (
            _image_stream(Filter=DCT, ColorSpace=RGB, Decode=ArrayObject()),
            False,
        ),
        # Color spaces a JPEG file does not show like the PDF
        (_image_stream(Filter=DCT), False),
        (
            _image_stream(Filter=DCT, ColorSpace=NameObject("/DeviceCMYK")),
            False,
        ),
        (_image_stream(Filter=DCT, ColorSpace=ArrayObject()), False),
        (
            _image_stream(
                Filter=DCT,
                ColorSpace=ArrayObject([NameObject("/Indexed"), RGB]),
            ),
            False,
        ),
        (
            _image_stream(Filter=DCT, ColorSpace=_icc_based(NumberObject(4))),
            False,
        ),
        (
            _image_stream(Filter=DCT, ColorSpace=_icc_based(NullObject())),
            False,
        ),
        (
            _image_stream(
                Filter=DCT, ColorSpace=ArrayObject([NameObject("/ICCBased")])
            ),
            False,
        ),
        (
            _image_stream(
                Filter=DCT,
                ColorSpace=ArrayObject(
                    [NameObject("/ICCBased"), NullObject()]
                ),
            ),
            False,
        ),
    ],
)
def test_is_unaltered_jpeg(
    stream: DecodedStreamObject, expected: bool
) -> None:
    assert is_unaltered_jpeg(stream) is expected


def test_get_image_data_falls_back_to_converted_data() -> None:
    page_reference = PdfWriter().add_blank_page(10, 10).indirect_reference
    assert page_reference is not None

    # Inline images have no reference; other objects are not an image stream
    assert get_image_data(b"converted", None) == b"converted"
    assert get_image_data(b"converted", page_reference) == b"converted"
