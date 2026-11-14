from contextlib import chdir
from pathlib import Path

import pytest
from endesive.pdf import PDFVerifier
from pypdf.generic import (
    ArrayObject,
    DictionaryObject,
    NameObject,
    NullObject,
    PdfObject,
)

from pdfly.sign import is_signature

from .conftest import RESOURCES_ROOT, run_cli


def test_sign_missing_certificate_key_option(
    capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    # Act
    with chdir(tmp_path):
        exit_code = run_cli(
            ["sign", str(RESOURCES_ROOT / "input8.pdf"), "-o", "out.pdf"]
        )
    captured = capsys.readouterr()

    # Assert
    assert exit_code == 2
    assert "Missing option" in captured.err


def test_sign_already_signed_pdf(
    capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    # Act
    with chdir(tmp_path):
        exit_code = run_cli(
            [
                "sign",
                str(RESOURCES_ROOT / "sign_pkcs12.pdf"),
                "-o",
                "out.pdf",
                "--p12",
                str(RESOURCES_ROOT / "signing-certificate.p12"),
                "--p12-password",
                "fpdf2",
            ]
        )
    captured = capsys.readouterr()

    # Assert
    assert exit_code == 2
    assert "already signed" in captured.err


def test_sign_pkcs12(capsys: pytest.CaptureFixture, tmp_path: Path) -> None:
    # Act
    with chdir(tmp_path):
        exit_code = run_cli(
            [
                "sign",
                str(RESOURCES_ROOT / "input8.pdf"),
                "-o",
                "out.pdf",
                "--p12",
                str(RESOURCES_ROOT / "signing-certificate.p12"),
                "--p12-password",
                "fpdf2",
            ]
        )
    captured = capsys.readouterr()

    # Assert
    assert exit_code == 0
    assert not captured.err

    outpdf = tmp_path / "out.pdf"
    certificate = RESOURCES_ROOT / "signing-certificate.crt"
    results = PDFVerifier(
        outpdf.read_bytes(), [certificate.read_bytes()]
    ).verify_all_signatures()
    assert len(results) == 1
    for result in results:
        assert result.signatureok
        assert result.hashok
        assert result.certok


def test_sign_pkcs12_in_place(
    capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    # Arrange
    input8pdf = RESOURCES_ROOT / "input8.pdf"
    outpdf = tmp_path / "out.pdf"

    outpdf.write_bytes(input8pdf.read_bytes())

    # Act
    with chdir(tmp_path):
        exit_code = run_cli(
            [
                "sign",
                "out.pdf",
                "--in-place",
                "--p12",
                str(RESOURCES_ROOT / "signing-certificate.p12"),
                "--p12-password",
                "fpdf2",
            ]
        )
    captured = capsys.readouterr()

    # Assert
    assert exit_code == 0
    assert not captured.err

    certificate = RESOURCES_ROOT / "signing-certificate.crt"
    results = PDFVerifier(
        outpdf.read_bytes(), [certificate.read_bytes()]
    ).verify_all_signatures()
    assert len(results) == 1
    for result in results:
        assert result.signatureok
        assert result.hashok
        assert result.certok


def test_sign_requires_output_or_in_place(
    capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    with chdir(tmp_path):
        exit_code = run_cli(
            [
                "sign",
                str(RESOURCES_ROOT / "input8.pdf"),
                "--p12",
                str(RESOURCES_ROOT / "signing-certificate.p12"),
            ]
        )
    captured = capsys.readouterr()

    assert exit_code == 2
    assert "One of the options --output or --in-place is required" in (
        captured.err
    )
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize(
    ("annotation", "expected"),
    [
        (
            DictionaryObject(
                {
                    NameObject("/Subtype"): NameObject("/Widget"),
                    NameObject("/FT"): NameObject("/Sig"),
                }
            ),
            True,
        ),
        (
            DictionaryObject(
                {
                    NameObject("/Subtype"): NameObject("/Widget"),
                    NameObject("/FT"): NameObject("/Tx"),
                }
            ),
            False,
        ),
        (
            DictionaryObject({NameObject("/Subtype"): NameObject("/Link")}),
            False,
        ),
        (ArrayObject(), False),
        # What pypdf resolves a reference to a missing object to:
        (NullObject(), False),
    ],
)
def test_is_signature(annotation: PdfObject, expected: bool) -> None:
    assert is_signature(annotation) is expected
