"""Tests for the `meta` command."""

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest
from fpdf import FPDF
from pypdf import PdfWriter
from pypdf.constants import UserAccessPermissions

from .conftest import PROJECT_ROOT, RESOURCES_ROOT, plain, run_cli

ALL_PERMISSIONS = {
    "print": True,
    "modify": True,
    "copy": True,
    "annotate": True,
    "fill-forms": True,
    "copy-for-accessibility": True,
    "assemble": True,
    "print-high-quality": True,
}


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


def encrypt(
    tmp_path: Path, algorithm: str, permissions: UserAccessPermissions
) -> Path:
    writer = PdfWriter(clone_from=RESOURCES_ROOT / "box.pdf")
    writer.encrypt("secret", algorithm=algorithm, permissions_flag=permissions)
    path = tmp_path / "encrypted.pdf"
    writer.write(path)
    return path


def run_meta(
    pdf: Path, output: str, capsys: pytest.CaptureFixture[str]
) -> tuple[int | str | None, str, str]:
    exit_code = run_cli(["meta", str(pdf), "--output", output])
    captured = capsys.readouterr()
    return exit_code, captured.out, captured.err


def test_meta_json_with_info(
    pdf_with_info: Path, capsys: pytest.CaptureFixture[str]
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
    pdf_without_info: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    exit_code, out, err = run_meta(pdf_without_info, "json", capsys)

    assert exit_code == 0, err
    assert not err
    meta = json.loads(out)
    assert meta["title"] is None
    assert meta["author"] is None
    assert meta["id1"] == ""
    assert meta["id2"] == ""
    assert meta["images"] == []
    assert meta["pages"] == 1


def test_meta_json_encrypted(
    encrypted_pdf: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    exit_code, out, err = run_meta(encrypted_pdf, "json", capsys)

    assert exit_code == 0, err
    assert not err
    meta = json.loads(out)
    assert meta["encryption"] == {
        "revision": 6,
        "v_value": 5,
        "permissions": ALL_PERMISSIONS,
    }
    # Regression test: this used to be read at the parser's current position
    assert meta["pdf_file_version"] == "%PDF-1.3"
    assert meta["pages"] is None


def test_meta_text_with_info(
    pdf_with_info: Path, capsys: pytest.CaptureFixture[str]
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
    pdf_without_info: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    exit_code, out, err = run_meta(pdf_without_info, "text", capsys)

    assert exit_code == 0, err
    assert not err
    assert "Title" not in out
    assert "Author" not in out
    assert "0 images (0 bytes)" in out
    assert "ID1=None ID2=None" in out


def test_meta_text_encrypted(
    encrypted_pdf: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    exit_code, out, err = run_meta(encrypted_pdf, "text", capsys)

    assert exit_code == 0, err
    assert not err
    assert "Encryption information" in out
    assert "Security Handler Revision Number" in out
    assert "unknown" in out  # number of pages
    # Fonts cannot be listed without the password:
    assert "Fonts" not in out


@pytest.mark.parametrize(
    ("algorithm", "permissions", "expected"),
    [
        pytest.param(
            # Revision 2 only defines the first four permissions
            "RC4-40",
            UserAccessPermissions.PRINT,
            {"print": True, "modify": False, "copy": False, "annotate": False},
            id="revision-2",
        ),
        pytest.param(
            "RC4-128",
            UserAccessPermissions.PRINT
            | UserAccessPermissions.EXTRACT_TEXT_AND_GRAPHICS,
            {
                **dict.fromkeys(ALL_PERMISSIONS, False),
                "print": True,
                "copy-for-accessibility": True,
            },
            id="revision-3",
        ),
        pytest.param(
            "AES-256",
            UserAccessPermissions.all() & ~UserAccessPermissions.MODIFY,
            {**ALL_PERMISSIONS, "modify": False},
            id="revision-6",
        ),
    ],
)
def test_meta_json_permissions(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    algorithm: str,
    permissions: UserAccessPermissions,
    expected: dict[str, bool],
) -> None:
    # Arrange
    pdf = encrypt(tmp_path, algorithm, permissions)

    # Act
    exit_code, out, err = run_meta(pdf, "json", capsys)

    # Assert
    assert exit_code == 0, err
    assert json.loads(out)["encryption"]["permissions"] == expected


def test_meta_json_permissions_of_libreoffice_pdf(
    capsys: pytest.CaptureFixture[str],
) -> None:
    # Arrange
    # qpdf --show-encryption: all permissions except "modify document assembly"
    pdf = (
        PROJECT_ROOT
        / "sample-files"
        / "005-libreoffice-writer-password"
        / "libreoffice-writer-password.pdf"
    )

    # Act
    exit_code, out, err = run_meta(pdf, "json", capsys)

    # Assert
    assert exit_code == 0, err
    assert json.loads(out)["encryption"]["permissions"] == {
        **ALL_PERMISSIONS,
        "assemble": False,
    }


@pytest.mark.parametrize(
    ("permissions", "expected"),
    [
        pytest.param(UserAccessPermissions.all(), "all", id="all"),
        pytest.param(UserAccessPermissions(0), "none", id="none"),
        pytest.param(
            UserAccessPermissions.all()
            & ~UserAccessPermissions.ASSEMBLE_DOC
            & ~UserAccessPermissions.MODIFY,
            "all except modify, assemble",
            id="few-denied",
        ),
        pytest.param(
            UserAccessPermissions.PRINT | UserAccessPermissions.EXTRACT,
            "only print, copy",
            id="few-allowed",
        ),
    ],
)
def test_meta_text_permissions(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    permissions: UserAccessPermissions,
    expected: str,
) -> None:
    # Arrange
    pdf = encrypt(tmp_path, "AES-256", permissions)

    # Act
    exit_code, out, err = run_meta(pdf, "text", capsys)

    # Assert
    assert exit_code == 0, err
    assert "Encrypted yes" in plain(out)
    assert f"Permissions {expected} " in plain(out)


def test_meta_text_permissions_not_encrypted(
    pdf_with_info: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    exit_code, out, err = run_meta(pdf_with_info, "text", capsys)

    assert exit_code == 0, err
    assert "Encrypted no" in plain(out)
    assert "Permissions all (not encrypted)" in plain(out)
