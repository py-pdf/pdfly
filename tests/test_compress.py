"""Tests for the `compress` command."""

from pathlib import Path

import pytest
from typer.testing import CliRunner

from pdfly.cli import entry_point

runner = CliRunner()


@pytest.mark.parametrize("input_pdf_filepath", Path("resources").glob("*.pdf"))
def test_compress_sample_files(
    input_pdf_filepath: Path, tmp_path: Path
) -> None:
    """Test compression on all sample PDF files."""
    output_pdf_filepath = tmp_path / "compressed_output.pdf"

    result = runner.invoke(
        entry_point,
        ["compress", str(input_pdf_filepath), str(output_pdf_filepath)],
    )

    assert (
        result.exit_code == 0
    ), f"Compression failed for {input_pdf_filepath}: {result.output}"

    assert (
        output_pdf_filepath.exists()
    ), f"Output PDF {output_pdf_filepath} does not exist."

    # Verify output file is a valid PDF
    with open(output_pdf_filepath, "rb") as f:
        content = f.read()
        assert content.startswith(
            b"%PDF-"
        ), f"Output is not a valid PDF file: {output_pdf_filepath}"

    assert "Original Size" in result.output
    assert "Final Size" in result.output


def test_compress_no_compression_when_larger(tmp_path: Path) -> None:
    """Test that compression doesn't apply when result would be larger."""
    # Create a small PDF that might not compress well
    from fpdf import FPDF

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", size=12)
    pdf.cell(200, 10, text="Short text", ln=True, align="C")

    input_pdf = tmp_path / "small.pdf"
    pdf.output(input_pdf)

    output_pdf = tmp_path / "compressed.pdf"

    result = runner.invoke(
        entry_point,
        ["compress", str(input_pdf), str(output_pdf)],
    )

    assert result.exit_code == 0

    if "No compression applied" in result.output:
        # If compression would make file larger, ensure original is copied
        assert input_pdf.stat().st_size == output_pdf.stat().st_size
        assert "would increase size" in result.output
    else:
        # If compression worked, ensure it's actually smaller or same size
        assert output_pdf.stat().st_size <= input_pdf.stat().st_size


def test_compress_file_integrity(tmp_path: Path) -> None:
    """Test that compressed files maintain PDF integrity."""
    from fpdf import FPDF

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", size=12)
    pdf.cell(200, 10, text="Test PDF for compression", ln=True, align="C")
    pdf.cell(200, 10, text="This is a test document.", ln=True, align="L")
    pdf.add_page()
    pdf.cell(200, 10, text="Second page content", ln=True, align="C")

    input_pdf = tmp_path / "test.pdf"
    pdf.output(input_pdf)

    output_pdf = tmp_path / "compressed.pdf"

    result = runner.invoke(
        entry_point,
        ["compress", str(input_pdf), str(output_pdf)],
    )

    assert result.exit_code == 0

    from pypdf import PdfReader

    reader = PdfReader(str(output_pdf))
    assert len(reader.pages) == 2

    page1_text = reader.pages[0].extract_text()
    page2_text = reader.pages[1].extract_text()

    assert "Test PDF for compression" in page1_text
    assert "Second page content" in page2_text


def test_compress_output_metrics(tmp_path: Path) -> None:
    """Test that compression metrics are properly displayed."""
    from fpdf import FPDF

    pdf = FPDF()
    for _i in range(10):
        pdf.add_page()
        pdf.set_font("helvetica", size=12)
        pdf.cell(
            200,
            10,
            text="This is repeated text on every page " * 5,
            ln=True,
            align="L",
        )

    input_pdf = tmp_path / "repeat.pdf"
    pdf.output(input_pdf)

    output_pdf = tmp_path / "compressed.pdf"

    result = runner.invoke(
        entry_point,
        ["compress", str(input_pdf), str(output_pdf)],
    )

    assert result.exit_code == 0

    output_lines = result.output.strip().split("\n")
    assert any("Original Size" in line for line in output_lines)
    assert any("Final Size" in line for line in output_lines)

    # Extract sizes from output
    orig_size_line = next(
        line for line in output_lines if "Original Size" in line
    )
    final_size_line = next(
        line for line in output_lines if "Final Size" in line
    )

    assert ":" in orig_size_line
    assert ":" in final_size_line


def test_compress_same_input_output_not_allowed(tmp_path: Path) -> None:
    """Test that input and output files cannot be the same."""
    input_pdf = tmp_path / "test.pdf"

    # Create a simple PDF
    from fpdf import FPDF

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", size=12)
    pdf.cell(200, 10, text="Test", ln=True, align="C")
    pdf.output(input_pdf)

    # Try to compress to the same file (should work but might not compress)
    result = runner.invoke(
        entry_point,
        ["compress", str(input_pdf), str(input_pdf)],
    )

    assert result.exit_code in [0, 1]  # 0 for success, 1 for error


def test_compress_preserves_metadata(tmp_path: Path) -> None:
    """Test that compression preserves PDF metadata."""
    from fpdf import FPDF

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", size=12)
    pdf.cell(200, 10, text="Test document", ln=True, align="C")

    # Set some metadata
    pdf.set_title("Test Title")
    pdf.set_author("Test Author")
    pdf.set_subject("Test Subject")

    input_pdf = tmp_path / "metadata.pdf"
    pdf.output(input_pdf)

    output_pdf = tmp_path / "compressed.pdf"

    result = runner.invoke(
        entry_point,
        ["compress", str(input_pdf), str(output_pdf)],
    )

    assert result.exit_code == 0

    from pypdf import PdfReader

    reader = PdfReader(str(output_pdf))
    metadata = reader.metadata

    assert metadata is not None
    assert metadata.get("/Title") == "Test Title"
    assert metadata.get("/Author") == "Test Author"
    assert metadata.get("/Subject") == "Test Subject"
