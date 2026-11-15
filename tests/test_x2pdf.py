"""
Every CLI command is called here with a typer CliRunner.

Here should only be end-to-end tests.
"""

from pathlib import Path

import pytest
from fpdf import FPDF
from PIL import Image
from pypdf import PdfReader

from .conftest import run_cli


def test_x2pdf_succeed_to_convert_jpg(
    capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    # Arrange
    output = tmp_path / "out.pdf"

    # Act
    exit_code = run_cli(
        [
            "x2pdf",
            "sample-files/003-pdflatex-image/page-0-Im1.jpg",
            "--output",
            str(output),
        ]
    )

    # Assert
    captured = capsys.readouterr()
    assert exit_code == 0, captured
    assert captured.out == ""
    assert output.exists()


def test_x2pdf_succeed_to_embed_pdfs(
    capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    # Arrange
    output = tmp_path / "out.pdf"

    # Act
    exit_code = run_cli(
        [
            "x2pdf",
            "sample-files/001-trivial/minimal-document.pdf",
            "sample-files/002-trivial-libre-office-writer/002-trivial-libre-office-writer.pdf",
            "--output",
            str(output),
        ]
    )

    # Assert
    captured = capsys.readouterr()
    assert exit_code == 0, captured
    assert captured.out == ""
    assert output.exists()


def test_x2pdf_fail_to_open_file(
    capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    # Arrange & Act
    exit_code = run_cli(
        [
            "x2pdf",
            "NonExistingFile",
            "--output",
            str(tmp_path / "out.pdf"),
        ]
    )

    # Assert
    captured = capsys.readouterr()
    assert exit_code == 1, captured
    assert "No such file or directory" in captured.out


def test_x2pdf_fail_to_convert(
    capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    # Arrange & Act
    exit_code = run_cli(
        [
            "x2pdf",
            "README.md",
            "--output",
            str(tmp_path / "out.pdf"),
        ]
    )

    # Assert
    captured = capsys.readouterr()
    assert exit_code == 1, captured
    assert "Error: Could not convert 'README.md' to a PDF" in captured.out


def create_input_file(tmp_path: Path, name: str, widths: list[int]) -> Path:
    """
    Create an image (one width) or a PDF (one page per width).

    Each page gets a unique width, which identifies it in the output:
    x2pdf converts an image with a width of N pixels to a page with a width
    of N points.
    """
    if name.lower().endswith(".pdf"):
        pdf = FPDF(unit="pt")
        for width in widths:
            pdf.add_page(format=(width, 50))
        filepath = tmp_path / name
        pdf.output(str(filepath))
        return filepath
    (width,) = widths
    filepath = tmp_path / name
    Image.new("RGB", (width, 50), "white").save(filepath)
    return filepath


@pytest.mark.parametrize(
    ("inputs", "expected_widths"),
    [
        pytest.param(
            [("1.jpg", [100]), ("2.jpg", [200]), ("3.jpg", [300])],
            [100, 200, 300],
            id="images",
        ),
        pytest.param(
            [("doc.pdf", [400, 500, 600])],
            [400, 500, 600],
            id="pages-of-one-pdf",
        ),
        pytest.param(
            [("1.jpg", [100]), ("doc.pdf", [400, 500]), ("2.png", [200])],
            [100, 400, 500, 200],
            id="pdf-between-images",
        ),
        pytest.param(
            [("1.jpg", [100]), ("DOC.PDF", [400, 500])],
            [100, 400, 500],
            id="uppercase-pdf-extension",
        ),
    ],
)
def test_x2pdf_keeps_the_order_of_the_input_pages(
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
    inputs: list[tuple[str, list[int]]],
    expected_widths: list[int],
) -> None:
    # Arrange
    filepaths = [
        create_input_file(tmp_path, name, widths) for name, widths in inputs
    ]
    output = tmp_path / "out.pdf"

    # Act
    exit_code = run_cli(
        ["x2pdf", *map(str, filepaths), "--output", str(output)]
    )

    # Assert
    captured = capsys.readouterr()
    assert exit_code == 0, captured
    widths = [round(page.mediabox.width) for page in PdfReader(output).pages]
    assert widths == expected_widths
