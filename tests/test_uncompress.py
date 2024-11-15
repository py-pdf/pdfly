"""Tests for the `uncompress` command."""

import pytest
from pathlib import Path
from pdfly.cli import entry_point
from typer.testing import CliRunner

runner = CliRunner()


@pytest.mark.parametrize("input_pdf_filepath", Path("sample-files").glob("*.pdf"))
def test_uncompress_all_sample_files(input_pdf_filepath: Path, tmp_path: Path) -> None:

    output_pdf_filepath = tmp_path / "uncompressed_output.pdf"

    result = runner.invoke(
        entry_point,
        ["uncompress", str(input_pdf_filepath), str(output_pdf_filepath)],
    )

    assert (
        result.exit_code == 0
    ), f"Error in uncompressing {input_pdf_filepath}: {result.output}"
    assert (
        output_pdf_filepath.exists()
    ), f"Output PDF {output_pdf_filepath} does not exist."

    from pypdf import PdfReader

    reader = PdfReader(str(output_pdf_filepath))
    for page in reader.pages:
        contents = page.get("/Contents")
        if contents:
            assert "/Filter" not in contents, "Content stream is still compressed"
