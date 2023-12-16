"""Utilities and fixtures that are available automatically for all tests."""

import io, os
from pathlib import Path

from fpdf import FPDF
import pytest
from pdfly.cli import entry_point

try:
    from contextlib import chdir  # type: ignore
except ImportError:  # Fallback when not available (< Python 3.11):
    from contextlib import contextmanager

    @contextmanager
    def chdir(dir_path):
        """Non thread-safe context manager to change the current working directory."""
        cwd = Path.cwd()
        os.chdir(dir_path)
        try:
            yield
        finally:
            os.chdir(cwd)


TESTS_ROOT = Path(__file__).parent.resolve()
PROJECT_ROOT = TESTS_ROOT.parent
RESOURCES_ROOT = PROJECT_ROOT / "resources"


def run_cli(args):
    try:
        entry_point(args)
    except SystemExit as error:
        return error.code


@pytest.fixture
def two_pages_pdf_filepath(tmp_path):
    "A PDF with 2 pages, and a different image on each page"
    pdf = FPDF()
    pdf.add_page()
    pdf.image(RESOURCES_ROOT / "baleines.jpg")
    pdf.add_page()
    pdf.image(RESOURCES_ROOT / "pythonknight.png")
    pdf_filepath = tmp_path / "two_pages.pdf"
    pdf.output(pdf_filepath)
    return pdf_filepath


@pytest.fixture
def pdf_file_100(tmp_path):
    """A PDF with 100 pages; each has only the page index on it."""
    pdf = FPDF()

    for i in range(100):
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"{i}", ln=True, align="C")

    pdf_filepath = tmp_path / "two_pages.pdf"
    pdf.output(pdf_filepath)
    return pdf_filepath
