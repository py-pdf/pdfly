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


def test_extract_images_pages_selects_second_page(
    capsys: pytest.CaptureFixture,
    tmp_path: Path,
    two_pages_pdf_filepath: Path,
) -> None:
    # https://github.com/py-pdf/pdfly/issues/194 - extract images from specific pages
    with chdir(tmp_path):
        run_cli(
            [
                "extract-images",
                str(two_pages_pdf_filepath),
                "--pages",
                "1:",
            ]
        )
        extracted = sorted(p.name for p in tmp_path.glob("*.png")) + sorted(
            p.name for p in tmp_path.glob("*.jpg")
        )
    captured = capsys.readouterr()
    assert not captured.err
    assert "Extracted 1 images" in captured.out
    assert len(extracted) == 1
    assert extracted[0].startswith("0001-")


def test_extract_images_pages_first_page_only(
    capsys: pytest.CaptureFixture,
    tmp_path: Path,
    two_pages_pdf_filepath: Path,
) -> None:
    with chdir(tmp_path):
        run_cli(
            [
                "extract-images",
                str(two_pages_pdf_filepath),
                "--pages",
                "0",
            ]
        )
        extracted = sorted(p.name for p in tmp_path.glob("*.png")) + sorted(
            p.name for p in tmp_path.glob("*.jpg")
        )
    captured = capsys.readouterr()
    assert not captured.err
    assert "Extracted 1 images" in captured.out
    assert len(extracted) == 1
    assert extracted[0].startswith("0000-")
