"""
Every CLI command is called here with a typer CliRunner.

Here should only be end-to-end tests.
"""

from pathlib import Path

import pytest
from fpdf import FPDF
from pypdf import PdfReader

from .conftest import run_cli


def test_x2pdf_succeed_to_convert_jpg(
    capsys: pytest.CaptureFixture, tmp_path: Path
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
    capsys: pytest.CaptureFixture, tmp_path: Path
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
    capsys: pytest.CaptureFixture, tmp_path: Path
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
    capsys: pytest.CaptureFixture, tmp_path: Path
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


def test_x2pdf_preserves_input_order(
    capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    # Arrange
    input_filepaths = []
    for char in "abc":
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("helvetica", size=12)
        pdf.cell(200, 10, text=char)
        filepath = tmp_path / f"{char}.pdf"
        pdf.output(filepath)
        input_filepaths.append(str(filepath))
    output = tmp_path / "out.pdf"

    # Act
    exit_code = run_cli(["x2pdf", *input_filepaths, "--output", str(output)])

    # Assert
    captured = capsys.readouterr()
    assert exit_code == 0, captured
    pages = PdfReader(output).pages
    assert [page.extract_text().strip() for page in pages] == ["a", "b", "c"]
