import pytest

from .conftest import RESOURCES_ROOT, chdir, run_cli


def test_extract_images_jpg_png(capsys, tmp_path):
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


@pytest.mark.xfail()  # There is currently a bug there
def test_extract_images_monochrome(capsys, tmp_path):
    with chdir(tmp_path):
        run_cli(["extract-images", str(RESOURCES_ROOT / "box.pdf")])
    captured = capsys.readouterr()
    assert not captured.err
    assert "Image extracted" in captured.out
