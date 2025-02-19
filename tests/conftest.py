"""Utilities and fixtures that are available automatically for all tests."""

import os
from pathlib import Path

import pytest
from fpdf import FPDF

from pdfly.cli import entry_point

try:
    from contextlib import chdir  # type: ignore
except ImportError:  # Fallback when not available (< Python 3.11):
    from contextlib import contextmanager

    @contextmanager  # type: ignore
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


@pytest.fixture()
def two_pages_pdf_filepath(tmp_path):
    "A PDF with 2 pages, and a different image on each page"
    # Note: prior to v2.7.9, fpdf2 produced incorrect /Resources dicts for each page (cf. fpdf2 PR #1133),
    # leading to an "abnormal" two_pages.pdf generated there, and for test_cat_subset_ensure_reduced_size() to fail.
    pdf = FPDF()
    pdf.add_page()
    pdf.image(RESOURCES_ROOT / "baleines.jpg")
    pdf.add_page()
    pdf.image(RESOURCES_ROOT / "pythonknight.png")
    pdf_filepath = tmp_path / "two_pages.pdf"
    pdf.output(pdf_filepath)
    return pdf_filepath


@pytest.fixture()
def pdf_file_100(tmp_path):
    """A PDF with 100 pages; each has only the page index on it."""
    pdf = FPDF()

    for i in range(100):
        pdf.add_page()
        pdf.set_font("helvetica", size=12)
        pdf.cell(200, 10, text=f"{i}", ln=True, align="C")

    pdf_filepath = tmp_path / "pdf_file_100.pdf"
    pdf.output(pdf_filepath)
    return pdf_filepath


@pytest.fixture()
def pdf_file_abc(tmp_path):
    """A PDF with 100 pages; each has only the page index on it."""
    pdf = FPDF()

    for char in [chr(i) for i in range(ord("a"), ord("z") + 1)]:
        pdf.add_page()
        pdf.set_font("helvetica", size=12)
        pdf.cell(200, 10, text=f"{char}", ln=True, align="C")

    pdf_filepath = tmp_path / "abc.pdf"
    pdf.output(pdf_filepath)
    return pdf_filepath
