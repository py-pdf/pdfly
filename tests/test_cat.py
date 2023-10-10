import pytest
from pypdf import PdfReader

from .conftest import RESOURCES_ROOT, chdir, run_cli


def test_cat_incorrect_number_of_args(capsys, tmp_path):
    with chdir(tmp_path):
        exit_code = run_cli(["cat", str(RESOURCES_ROOT / "box.pdf")])
    assert exit_code == 2
    captured = capsys.readouterr()
    assert "Missing argument" in captured.err


def test_cat_two_files_ok(capsys, tmp_path):
    with chdir(tmp_path):
        exit_code = run_cli(
            [
                "cat",
                str(RESOURCES_ROOT / "box.pdf"),
                str(RESOURCES_ROOT / "jpeg.pdf"),
                "--output",
                "./out.pdf",
            ]
        )
    captured = capsys.readouterr()
    assert exit_code == 0, captured
    assert not captured.err
    reader = PdfReader(tmp_path / "out.pdf")
    assert len(reader.pages) == 2


def test_cat_subset_ok(capsys, tmp_path):
    with chdir(tmp_path):
        exit_code = run_cli(
            [
                "cat",
                str(RESOURCES_ROOT / "GeoBase_NHNC1_Data_Model_UML_EN.pdf"),
                "13:15",
                "--output",
                "./out.pdf",
            ]
        )
    captured = capsys.readouterr()
    assert exit_code == 0, captured
    assert not captured.err
    reader = PdfReader(tmp_path / "out.pdf")
    assert len(reader.pages) == 2


@pytest.mark.parametrize(
    "page_range",
    ["a", "-", "1-", "1-1-1", "1:1:1:1"],
)
def test_cat_subset_invalid_args(capsys, tmp_path, page_range):
    with chdir(tmp_path):
        exit_code = run_cli(
            [
                "cat",
                str(RESOURCES_ROOT / "jpeg.pdf"),
                page_range,
                "--output",
                "./out.pdf",
            ]
        )
    captured = capsys.readouterr()
    assert exit_code == 2, captured
    assert "Invalid file path or page range provided" in captured.err


@pytest.mark.skip(reason="This check is not implemented yet")
def test_cat_subset_warn_on_missing_pages(capsys, tmp_path):
    with chdir(tmp_path):
        exit_code = run_cli(
            [
                "cat",
                str(RESOURCES_ROOT / "jpeg.pdf"),
                "2",
                "--output",
                "./out.pdf",
            ]
        )
    captured = capsys.readouterr()
    assert exit_code == 0, captured
    assert "WARN" in captured.out
