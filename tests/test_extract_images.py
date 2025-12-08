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


def test_extract_images_range_first_only(
    capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    # Use a file with multiple images; request only the first image
    with chdir(tmp_path):
        run_cli(
            [
                "extract-images",
                str(RESOURCES_ROOT / "GeoBase_NHNC1_Data_Model_UML_EN.pdf"),
                "--from",
                "0",
                "--end",
                "0",
            ]
        )
    captured = capsys.readouterr()
    assert not captured.err
    assert "Extracted 1 images" in captured.out


def test_extract_images_range_start_to_end(
    capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    # Request first two images from a file that has three
    with chdir(tmp_path):
        run_cli(
            [
                "extract-images",
                str(RESOURCES_ROOT / "GeoBase_NHNC1_Data_Model_UML_EN.pdf"),
                "--from",
                "0",
                "--end",
                "1",
            ]
        )
    captured = capsys.readouterr()
    assert not captured.err
    assert "Extracted 2 images" in captured.out
