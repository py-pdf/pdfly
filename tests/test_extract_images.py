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


def test_extract_images_monochrome(capsys, tmp_path):
    # There used to be a bug for this case: https://github.com/py-pdf/pypdf/issues/2176
    with chdir(tmp_path):
        run_cli(["extract-images", str(RESOURCES_ROOT / "box.pdf")])
    captured = capsys.readouterr()
    assert not captured.err
    assert "Extracted 1 images" in captured.out
