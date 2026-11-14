"""Tests for the `decrypt` command."""

import sys
from io import BytesIO
from pathlib import Path

import pytest
from pypdf import PdfReader, PdfWriter

from .conftest import RESOURCES_ROOT, run_cli


class FakeStdin:
    def __init__(self, data: bytes) -> None:
        self.buffer = BytesIO(data)


@pytest.fixture
def encrypted_pdf(tmp_path: Path) -> Path:
    writer = PdfWriter(clone_from=RESOURCES_ROOT / "box.pdf")
    writer.encrypt("secret", algorithm="AES-256")
    path = tmp_path / "encrypted.pdf"
    writer.write(path)
    return path


@pytest.fixture
def encrypted_pdf_with_empty_password(tmp_path: Path) -> Path:
    writer = PdfWriter(clone_from=RESOURCES_ROOT / "box.pdf")
    writer.encrypt("", algorithm="AES-256")
    path = tmp_path / "encrypted-empty-password.pdf"
    writer.write(path)
    return path


def test_decrypt_to_output_file(encrypted_pdf: Path, tmp_path: Path) -> None:
    output = tmp_path / "decrypted.pdf"

    exit_code = run_cli(
        ["decrypt", "-p", "secret", str(encrypted_pdf), str(output)]
    )

    assert exit_code == 0
    reader = PdfReader(output)
    assert not reader.is_encrypted
    assert len(reader.pages) == 1


def test_decrypt_without_output_writes_to_stdout(
    encrypted_pdf: Path, capsysbinary: pytest.CaptureFixture
) -> None:
    exit_code = run_cli(["decrypt", "-p", "secret", str(encrypted_pdf)])

    captured = capsysbinary.readouterr()
    assert exit_code == 0, captured.err
    assert captured.out.startswith(b"%PDF-")
    reader = PdfReader(BytesIO(captured.out))
    assert not reader.is_encrypted
    assert len(reader.pages) == 1


def test_decrypt_from_stdin(
    encrypted_pdf: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(sys, "stdin", FakeStdin(encrypted_pdf.read_bytes()))
    output = tmp_path / "decrypted.pdf"

    exit_code = run_cli(["decrypt", "-p", "secret", "-", str(output)])

    assert exit_code == 0
    reader = PdfReader(output)
    assert not reader.is_encrypted


def test_decrypt_with_empty_password(
    encrypted_pdf_with_empty_password: Path, tmp_path: Path
) -> None:
    output = tmp_path / "decrypted.pdf"

    exit_code = run_cli(
        ["decrypt", str(encrypted_pdf_with_empty_password), str(output)]
    )

    assert exit_code == 0
    reader = PdfReader(output)
    assert not reader.is_encrypted
    assert len(reader.pages) == 1


def test_decrypt_encrypted_requires_password(
    encrypted_pdf: Path, capsys: pytest.CaptureFixture
) -> None:
    exit_code = run_cli(["decrypt", str(encrypted_pdf)])

    assert exit_code == 1
    captured = capsys.readouterr()
    assert "--password" in captured.err


def test_decrypt_invalid_password(
    encrypted_pdf: Path, capsys: pytest.CaptureFixture
) -> None:
    exit_code = run_cli(["decrypt", "-p", "wrong", str(encrypted_pdf)])

    assert exit_code == 1
    captured = capsys.readouterr()
    assert "Invalid password." in captured.err


def test_decrypt_password_decrypt_failure(
    encrypted_pdf: Path, capsys: pytest.CaptureFixture
) -> None:
    def raise_error(_password: str) -> str:
        raise ValueError("boom")

    PdfReader.decrypt = raise_error  # type: ignore[method-assign]
    try:
        exit_code = run_cli(["decrypt", "-p", "secret", str(encrypted_pdf)])
    finally:
        del PdfReader.decrypt

    assert exit_code == 1
    captured = capsys.readouterr()
    assert "Invalid password." in captured.err


def test_decrypt_empty_password_decrypt_failure(
    encrypted_pdf_with_empty_password: Path, capsys: pytest.CaptureFixture
) -> None:
    def raise_error(_password: str) -> str:
        raise ValueError("boom")

    PdfReader.decrypt = raise_error  # type: ignore[method-assign]
    try:
        exit_code = run_cli(
            ["decrypt", str(encrypted_pdf_with_empty_password)]
        )
    finally:
        del PdfReader.decrypt

    assert exit_code == 1
    captured = capsys.readouterr()
    assert "--password" in captured.err


def test_decrypt_unencrypted_file_passthrough(
    capsysbinary: pytest.CaptureFixture,
) -> None:
    # Unencrypted input files are passed through unchanged so that
    # filter chains do not break unexpectedly.
    expected = (RESOURCES_ROOT / "box.pdf").read_bytes()

    exit_code = run_cli(["decrypt", str(RESOURCES_ROOT / "box.pdf")])

    captured = capsysbinary.readouterr()
    assert exit_code == 0, captured.err
    assert captured.out == expected


def test_decrypt_unencrypted_file_to_output(
    tmp_path: Path,
) -> None:
    expected = (RESOURCES_ROOT / "box.pdf").read_bytes()
    output = tmp_path / "output.pdf"

    exit_code = run_cli(
        ["decrypt", str(RESOURCES_ROOT / "box.pdf"), str(output)]
    )

    assert exit_code == 0
    assert output.read_bytes() == expected


def test_decrypt_missing_input_file(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    exit_code = run_cli(["decrypt", str(tmp_path / "not-there.pdf")])

    assert exit_code == 1
    captured = capsys.readouterr()
    assert "not-there.pdf" in captured.err
