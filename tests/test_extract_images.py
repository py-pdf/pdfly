from pathlib import Path

import pytest

from .conftest import RESOURCES_ROOT, chdir, run_cli


def test_extract_images_jpg_png(
    capsys: pytest.CaptureFixture, tmp_path: Path
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
    capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    # There used to be a bug for this case: https://github.com/py-pdf/pypdf/issues/2176
    with chdir(tmp_path):
        run_cli(["extract-images", str(RESOURCES_ROOT / "box.pdf")])
    captured = capsys.readouterr()
    assert not captured.err
    assert "Extracted 1 images" in captured.out


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
    capsys: pytest.CaptureFixture,
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
