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
    first_pdf = Path("sample-files/001-trivial/minimal-document.pdf")
    second_pdf = Path(
        "sample-files/002-trivial-libre-office-writer/"
        "002-trivial-libre-office-writer.pdf"
    )
    output = tmp_path / "out.pdf"

    # Act
    exit_code = run_cli(
        [
            "x2pdf",
            str(first_pdf),
            str(second_pdf),
            "--output",
            str(output),
        ]
    )

    # Assert
    captured = capsys.readouterr()
    assert exit_code == 0, captured
    assert captured.out == ""
    assert output.exists()
    reader = PdfReader(output)
    assert [page.extract_text() for page in reader.pages] == [
        PdfReader(first_pdf).pages[0].extract_text(),
        PdfReader(second_pdf).pages[0].extract_text(),
    ]


def test_x2pdf_preserve_image_order(
    capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    # Arrange
    specs = [
        ("0001.jpeg", (100, 150), (255, 0, 0)),
        ("0002.jpeg", (200, 250), (0, 255, 0)),
        ("0003.jpeg", (300, 350), (0, 0, 255)),
    ]
    image_paths = []
    for filename, size, color in specs:
        img_path = tmp_path / filename
        Image.new("RGB", size, color=color).save(img_path)
        image_paths.append(str(img_path))
    output = tmp_path / "out.pdf"

    # Act
    exit_code = run_cli(["x2pdf", *image_paths, "--output", str(output)])

    # Assert
    captured = capsys.readouterr()
    assert exit_code == 0, captured
    assert captured.out == ""
    reader = PdfReader(output)
    assert len(reader.pages) == 3
    embedded_images = [page.images[0].image for page in reader.pages]
    assert [img.size for img in embedded_images if img is not None] == [
        (100, 150),
        (200, 250),
        (300, 350),
    ]


def test_x2pdf_preserve_mixed_input_order(
    capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    # Arrange
    first_img = tmp_path / "first.png"
    Image.new("RGB", (120, 80), color=(255, 0, 0)).save(first_img)

    multi_pdf = tmp_path / "middle.pdf"
    pdf = FPDF()
    for label in ("First PDF page", "Second PDF page"):
        pdf.add_page()
        pdf.set_font("helvetica", size=12)
        pdf.cell(text=label)
    pdf.output(multi_pdf)

    last_img = tmp_path / "last.jpg"
    Image.new("RGB", (240, 160), color=(0, 0, 255)).save(last_img)

    output = tmp_path / "out.pdf"

    # Act
    exit_code = run_cli(
        [
            "x2pdf",
            str(first_img),
            str(multi_pdf),
            str(last_img),
            "--output",
            str(output),
        ]
    )

    # Assert
    captured = capsys.readouterr()
    assert exit_code == 0, captured
    assert captured.out == ""
    reader = PdfReader(output)
    assert len(reader.pages) == 4
    first_embedded = reader.pages[0].images[0].image
    assert first_embedded is not None
    assert first_embedded.size == (120, 80)
    assert reader.pages[1].extract_text().strip() == "First PDF page"
    assert reader.pages[2].extract_text().strip() == "Second PDF page"
    last_embedded = reader.pages[3].images[0].image
    assert last_embedded is not None
    assert last_embedded.size == (240, 160)


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
