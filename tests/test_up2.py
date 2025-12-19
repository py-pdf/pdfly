import os.path
from pathlib import Path

import pytest
from pypdf import PdfReader

from .conftest import RESOURCES_ROOT, chdir, run_cli


def test_up2_fewer_args(capsys: pytest.CaptureFixture, tmp_path: Path) -> None:
    with chdir(tmp_path):
        exit_code = run_cli(["2-up", str(RESOURCES_ROOT / "box.pdf")])
    assert exit_code == 2
    captured = capsys.readouterr()
    assert "Missing argument" in captured.err


def test_up2_extra_args(capsys: pytest.CaptureFixture, tmp_path: Path) -> None:
    with chdir(tmp_path):
        exit_code = run_cli(
            [
                "2-up",
                str(RESOURCES_ROOT / "box.pdf"),
                "./out.pdf",
                "./out2.pdf",
            ]
        )

    assert exit_code == 2
    captured = capsys.readouterr()
    assert "unexpected extra argument" in captured.err

    with chdir(tmp_path):
        assert not os.path.exists("out.pdf"), "'out.pdf' should not exist."
        assert not os.path.exists("out2.pdf"), "'out2.pdf' should not exist."


def test_up2_8page_file(capsys: pytest.CaptureFixture, tmp_path: Path) -> None:
    pdf_file = str(RESOURCES_ROOT / "input8.pdf")
    out_file_name = "out.pdf"

    in_reader = PdfReader(pdf_file)
    assert len(in_reader.pages) == 8
    in_height = in_reader.pages[0].mediabox.height
    in_width = in_reader.pages[0].mediabox.width

    # Act
    with chdir(tmp_path):
        exit_code = run_cli(
            [
                "2-up",
                pdf_file,
                out_file_name,
            ]
        )
    captured = capsys.readouterr()

    # Assert
    assert exit_code == 0, captured
    assert not captured.err

    out_reader = PdfReader(tmp_path / out_file_name)
    assert len(out_reader.pages) == 4

    out_width = out_reader.pages[0].mediabox.width
    out_height = out_reader.pages[0].mediabox.height

    assert out_width == 2 * in_width  # PR #78
    assert out_height == in_height


# Fix issue #218
def test_up2_odd_page_number(
    capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    pdf_file = "sample-files/026-latex-multicolumn/multicolumn.pdf"
    out_file_path = tmp_path / "out.pdf"

    # Ensure original page number is odd:
    in_reader = PdfReader(pdf_file)
    assert len(in_reader.pages) % 2 == 1

    # Act
    exit_code = run_cli(
        [
            "2-up",
            pdf_file,
            str(out_file_path),
        ]
    )
    captured = capsys.readouterr()

    # Assert
    assert exit_code == 0, captured
    assert not captured.err

    out_reader = PdfReader(out_file_path)
    assert len(out_reader.pages) == (len(in_reader.pages) + 1) / 2
