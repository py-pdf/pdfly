"""
Every CLI command is called here with a typer CliRunner.

Here should only be end-to-end tests.
"""

from pathlib import Path

from .conftest import run_cli


def test_x2pdf_succeed_to_convert_jpg(capsys, tmp_path: Path):
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


def test_x2pdf_succeed_to_embed_pdfs(capsys, tmp_path: Path):
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


def test_x2pdf_fail_to_open_file(capsys, tmp_path: Path):
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


def test_x2pdf_fail_to_convert(capsys, tmp_path: Path):
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
