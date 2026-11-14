import shutil
from contextlib import chdir
from pathlib import Path

import pytest
from fpdf import FPDF
from pypdf import PdfReader

from .conftest import RESOURCES_ROOT, run_cli


def test_extract_annotated_pages_input8(
    capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    # The default output is written next to the input file,
    # so we work on a copy to keep the resources/ directory clean:
    input_pdf = tmp_path / "input8.pdf"
    shutil.copy(RESOURCES_ROOT / "input8.pdf", input_pdf)
    with chdir(tmp_path):
        run_cli(
            [
                "extract-annotated-pages",
                str(input_pdf),
            ]
        )
    captured = capsys.readouterr()
    assert not captured.err
    assert "Extracted 1 pages with annotations" in captured.out
    assert (tmp_path / "input8_annotated.pdf").exists()


def test_extract_annotated_pages_skips_links(
    capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    pdf = FPDF()
    pdf.set_font("helvetica")
    pdf.add_page()  # only a link: not considered annotated
    pdf.cell(text="Link", link="https://example.com")
    pdf.add_page()  # a text annotation
    pdf.cell(text="Note")
    pdf.text_annotation(x=10, y=10, text="A note")
    pdf.add_page()  # no annotation at all
    pdf.cell(text="Nothing")
    input_pdf = tmp_path / "in.pdf"
    pdf.output(input_pdf)
    output_pdf = tmp_path / "out.pdf"

    exit_code = run_cli(
        ["extract-annotated-pages", str(input_pdf), "-o", str(output_pdf)]
    )

    captured = capsys.readouterr()
    assert exit_code == 0, captured.err
    assert (
        f"Extracted 1 pages with annotations to {output_pdf}" in captured.out
    )
    pages = PdfReader(output_pdf).pages
    assert len(pages) == 1
    assert "Note" in pages[0].extract_text()
    # The default output file was not written:
    assert not (tmp_path / "in_annotated.pdf").exists()
