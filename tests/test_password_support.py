"""Tests for --password support across pdfly commands that read PDFs.

Covers cat's siblings that gained --password in this change: rm,
extract-text, extract-images, extract-annotated-pages, compress,
rotate, 2-up, and booklet. cat itself already had password support
before this change and is covered separately by test_cat.py.
"""

from pathlib import Path

import pytest

from .conftest import chdir, run_cli

INVALID_PASSWORD_MSG = "Error: the decrypting password provided is invalid"


# ---------- extract-text ----------

def get_extracted_numbers(output: str) -> list[int]:
    """pdf_file_100 pages each contain only the page index as text."""
    return [int(line) for line in output.splitlines() if line.strip()]


def test_extract_text_password_ok(
    capsys: pytest.CaptureFixture, encrypted_pdf_filepath: Path
) -> None:
    exit_code = run_cli(
        [
            "extract-text",
            "--password=openpassword",
            str(encrypted_pdf_filepath),
        ]
    )
    captured = capsys.readouterr()
    assert exit_code == 0, captured
    assert not captured.err
    assert get_extracted_numbers(captured.out) == [0, 1, 2]


def test_extract_text_password_invalid(
    capsys: pytest.CaptureFixture, encrypted_pdf_filepath: Path
) -> None:
    exit_code = run_cli(
        [
            "extract-text",
            "--password=WRONG",
            str(encrypted_pdf_filepath),
        ]
    )
    captured = capsys.readouterr()
    assert exit_code == 1, captured
    assert INVALID_PASSWORD_MSG in captured.out


# ---------- rm ----------

def test_rm_password_ok(
    capsys: pytest.CaptureFixture, encrypted_pdf_filepath: Path, tmp_path: Path
) -> None:
    output = tmp_path / "out.pdf"
    exit_code = run_cli(
        [
            "rm",
            str(encrypted_pdf_filepath),
            "-o",
            str(output),
            "--password=openpassword",
            "0",
        ]
    )
    captured = capsys.readouterr()
    assert exit_code in (0, None), captured.err
    assert output.exists()


def test_rm_password_invalid(
    capsys: pytest.CaptureFixture, encrypted_pdf_filepath: Path, tmp_path: Path
) -> None:
    output = tmp_path / "out.pdf"
    exit_code = run_cli(
        [
            "rm",
            str(encrypted_pdf_filepath),
            "-o",
            str(output),
            "--password=WRONG",
            "0",
        ]
    )
    captured = capsys.readouterr()
    assert exit_code == 1
    assert INVALID_PASSWORD_MSG in captured.out


# ---------- extract-images ----------

def test_extract_images_password_ok(
    capsys: pytest.CaptureFixture,
    encrypted_pdf_filepath: Path,
    tmp_path: Path,
) -> None:
    with chdir(tmp_path):
        exit_code = run_cli(
            [
                "extract-images",
                str(encrypted_pdf_filepath),
                "--password=openpassword",
            ]
        )
    captured = capsys.readouterr()
    assert exit_code in (0, None), captured.err


def test_extract_images_password_invalid(
    capsys: pytest.CaptureFixture,
    encrypted_pdf_filepath: Path,
    tmp_path: Path,
) -> None:
    with chdir(tmp_path):
        exit_code = run_cli(
            [
                "extract-images",
                str(encrypted_pdf_filepath),
                "--password=WRONG",
            ]
        )
    captured = capsys.readouterr()
    assert exit_code == 1
    assert INVALID_PASSWORD_MSG in captured.out


# ---------- extract-annotated-pages ----------

def test_extract_annotated_pages_password_ok(
    capsys: pytest.CaptureFixture, encrypted_pdf_filepath: Path, tmp_path: Path
) -> None:
    output = tmp_path / "annotated.pdf"
    exit_code = run_cli(
        [
            "extract-annotated-pages",
            str(encrypted_pdf_filepath),
            "-o",
            str(output),
            "--password=openpassword",
        ]
    )
    captured = capsys.readouterr()
    assert exit_code in (0, None), captured.err


def test_extract_annotated_pages_password_invalid(
    capsys: pytest.CaptureFixture, encrypted_pdf_filepath: Path, tmp_path: Path
) -> None:
    output = tmp_path / "annotated.pdf"
    exit_code = run_cli(
        [
            "extract-annotated-pages",
            str(encrypted_pdf_filepath),
            "-o",
            str(output),
            "--password=WRONG",
        ]
    )
    captured = capsys.readouterr()
    assert exit_code == 1
    assert INVALID_PASSWORD_MSG in captured.out


# ---------- compress ----------

def test_compress_password_ok(
    capsys: pytest.CaptureFixture, encrypted_pdf_filepath: Path, tmp_path: Path
) -> None:
    output = tmp_path / "compressed.pdf"
    exit_code = run_cli(
        [
            "compress",
            str(encrypted_pdf_filepath),
            str(output),
            "--password=openpassword",
        ]
    )
    captured = capsys.readouterr()
    assert exit_code in (0, None), captured.err
    assert output.exists()


def test_compress_password_invalid(
    capsys: pytest.CaptureFixture, encrypted_pdf_filepath: Path, tmp_path: Path
) -> None:
    output = tmp_path / "compressed.pdf"
    exit_code = run_cli(
        [
            "compress",
            str(encrypted_pdf_filepath),
            str(output),
            "--password=WRONG",
        ]
    )
    captured = capsys.readouterr()
    assert exit_code == 1
    assert INVALID_PASSWORD_MSG in captured.out


# ---------- rotate ----------

def test_rotate_password_ok(
    capsys: pytest.CaptureFixture, encrypted_pdf_filepath: Path, tmp_path: Path
) -> None:
    output = tmp_path / "rotated.pdf"
    exit_code = run_cli(
        [
            "rotate",
            str(encrypted_pdf_filepath),
            "90",
            "-o",
            str(output),
            "--password=openpassword",
        ]
    )
    captured = capsys.readouterr()
    assert exit_code in (0, None), captured.err
    assert output.exists()


def test_rotate_password_invalid(
    capsys: pytest.CaptureFixture, encrypted_pdf_filepath: Path, tmp_path: Path
) -> None:
    output = tmp_path / "rotated.pdf"
    exit_code = run_cli(
        [
            "rotate",
            str(encrypted_pdf_filepath),
            "90",
            "-o",
            str(output),
            "--password=WRONG",
        ]
    )
    captured = capsys.readouterr()
    assert exit_code == 1
    assert INVALID_PASSWORD_MSG in captured.out


# ---------- 2-up ----------

def test_up2_password_ok(
    capsys: pytest.CaptureFixture, encrypted_pdf_filepath: Path, tmp_path: Path
) -> None:
    output = tmp_path / "up2.pdf"
    exit_code = run_cli(
        [
            "2-up",
            str(encrypted_pdf_filepath),
            str(output),
            "--password=openpassword",
        ]
    )
    captured = capsys.readouterr()
    assert exit_code in (0, None), captured.err
    assert output.exists()


def test_up2_password_invalid(
    capsys: pytest.CaptureFixture, encrypted_pdf_filepath: Path, tmp_path: Path
) -> None:
    output = tmp_path / "up2.pdf"
    exit_code = run_cli(
        [
            "2-up",
            str(encrypted_pdf_filepath),
            str(output),
            "--password=WRONG",
        ]
    )
    captured = capsys.readouterr()
    assert exit_code == 1
    assert INVALID_PASSWORD_MSG in captured.out


# ---------- booklet ----------

def test_booklet_password_ok(
    capsys: pytest.CaptureFixture, encrypted_pdf_filepath: Path, tmp_path: Path
) -> None:
    output = tmp_path / "booklet.pdf"
    exit_code = run_cli(
        [
            "booklet",
            str(encrypted_pdf_filepath),
            str(output),
            "--password=openpassword",
        ]
    )
    captured = capsys.readouterr()
    assert exit_code in (0, None), captured.err
    assert output.exists()


def test_booklet_password_invalid(
    capsys: pytest.CaptureFixture, encrypted_pdf_filepath: Path, tmp_path: Path
) -> None:
    output = tmp_path / "booklet.pdf"
    exit_code = run_cli(
        [
            "booklet",
            str(encrypted_pdf_filepath),
            str(output),
            "--password=WRONG",
        ]
    )
    captured = capsys.readouterr()
    assert exit_code == 1
    assert INVALID_PASSWORD_MSG in captured.out