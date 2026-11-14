"""Tests for the `meta` command."""

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest
from fpdf import FPDF
from pypdf import PdfWriter

from .conftest import RESOURCES_ROOT, run_cli


@pytest.fixture
def pdf_with_info(tmp_path: Path) -> Path:
    """A PDF with every /Info entry, an /ID, a font and an image."""
    pdf = FPDF()
    pdf.set_title("The Title")
    pdf.set_author("The Author")
    pdf.set_subject("The Subject")
    pdf.set_keywords("keyword1 keyword2")
    pdf.set_creator("The Creator")
    pdf.set_producer("The Producer")
    pdf.set_creation_date(datetime(2024, 1, 2, 3, 4, 5, tzinfo=UTC))
    pdf.add_page()
    pdf.set_font("helvetica")
    pdf.cell(text="Hello")
    pdf.image(RESOURCES_ROOT / "baleines.jpg", w=20)
    path = tmp_path / "with-info.pdf"
    pdf.output(path)
    return path


@pytest.fixture
def pdf_without_info(tmp_path: Path) -> Path:
    """A PDF with neither an /Info dictionary nor an /ID."""
    writer = PdfWriter()
    writer.add_blank_page(width=100, height=100)
    writer.metadata = None
    path = tmp_path / "without-info.pdf"
    writer.write(path)
    return path


@pytest.fixture
def encrypted_pdf(tmp_path: Path) -> Path:
    writer = PdfWriter(clone_from=RESOURCES_ROOT / "box.pdf")
    writer.encrypt("secret", algorithm="AES-256")
    path = tmp_path / "encrypted.pdf"
    writer.write(path)
    return path


def run_meta(
    pdf: Path, output: str, capsys: pytest.CaptureFixture
) -> tuple[int | str | None, str, str]:
    exit_code = run_cli(["meta", str(pdf), "--output", output])
    captured = capsys.readouterr()
    return exit_code, captured.out, captured.err


def test_meta_json_with_info(
    pdf_with_info: Path, capsys: pytest.CaptureFixture
) -> None:
    exit_code, out, err = run_meta(pdf_with_info, "json", capsys)

    assert exit_code == 0, err
    assert not err
    meta = json.loads(out)
    assert meta["title"] == "The Title"
    assert meta["author"] == "The Author"
    assert meta["subject"] == "The Subject"
    assert meta["keywords"] == "keyword1 keyword2"
    assert meta["creator"] == "The Creator"
    assert meta["producer"] == "The Producer"
    assert meta["creation_date"].startswith("2024-01-02T03:04:05")
    assert meta["pdf_file_version"] == "%PDF-1.3"
    assert meta["pages"] == 1
    assert meta["encryption"] is None
    assert meta["id1"] is not None
    assert meta["id2"] is not None
    assert len(meta["images"]) == 1
    assert meta["file_size"] == pdf_with_info.stat().st_size


def test_meta_json_without_info(
    pdf_without_info: Path, capsys: pytest.CaptureFixture
) -> None:
    exit_code, out, err = run_meta(pdf_without_info, "json", capsys)

    assert exit_code == 0, err
    assert not err
    meta = json.loads(out)
    assert meta["title"] is None
    assert meta["author"] is None
    assert meta["id1"] is None
    assert meta["id2"] is None
    assert meta["images"] == []
    assert meta["pages"] == 1


def test_meta_json_encrypted(
    encrypted_pdf: Path, capsys: pytest.CaptureFixture
) -> None:
    exit_code, out, err = run_meta(encrypted_pdf, "json", capsys)

    assert exit_code == 0, err
    assert not err
    meta = json.loads(out)
    assert meta["encryption"] == {"revision": 6, "v_value": 5}
    # Regression test: this used to be read at the parser's current position
    assert meta["pdf_file_version"] == "%PDF-1.3"
    assert meta["pages"] is None


def test_meta_text_with_info(
    pdf_with_info: Path, capsys: pytest.CaptureFixture
) -> None:
    exit_code, out, err = run_meta(pdf_with_info, "text", capsys)

    assert exit_code == 0, err
    assert not err
    for expected in (
        "The Title",
        "The Author",
        "2024-01-02 03:04:05",
        "The Creator",
        "The Producer",
        "The Subject",
        "keyword1 keyword2",
        "%PDF-1.3",
        "Helvetica",
        "1 images",
        "Operating System Data",
    ):
        assert expected in out
    assert "Encryption information" not in out


def test_meta_text_without_info(
    pdf_without_info: Path, capsys: pytest.CaptureFixture
) -> None:
    exit_code, out, err = run_meta(pdf_without_info, "text", capsys)

    assert exit_code == 0, err
    assert not err
    assert "Title" not in out
    assert "Author" not in out
    assert "0 images (0 bytes)" in out
    assert "ID1=None ID2=None" in out


def test_meta_text_encrypted(
    encrypted_pdf: Path, capsys: pytest.CaptureFixture
) -> None:
    exit_code, out, err = run_meta(encrypted_pdf, "text", capsys)

    assert exit_code == 0, err
    assert not err
    assert "Encryption information" in out
    assert "Security Handler Revision Number" in out
    assert "unknown" in out  # number of pages
    # Fonts cannot be listed without the password:
    assert "Fonts" not in out
