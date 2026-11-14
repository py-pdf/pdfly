from contextlib import chdir
from pathlib import Path

import pytest
from fpdf import FPDF

import pdfly.check_sign

from .conftest import RESOURCES_ROOT, plain, run_cli


def test_check_sign_manipulated_content(
    capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    # Arrange
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", style="B", size=16)
    pdf.add_text_markup_annotation(
        "Underline", "Hello World!", [0, 0, 0, 0, 0, 0, 0, 0]
    )
    pdf.sign_pkcs12(str(RESOURCES_ROOT / "signing-certificate.p12"), b"fpdf2")

    input_pdf_bytes = pdf.output()

    # manipulate signed pdf - leaving length intact
    input_pdf_bytes = input_pdf_bytes.replace(b"Hello World!", b"aaaaa aaaaa!")

    input_pdf_manipulated = tmp_path / "signed_manipulated.pdf"
    input_pdf_manipulated.write_bytes(input_pdf_bytes)

    # Act
    with chdir(tmp_path):
        exit_code = run_cli(
            [
                "check-sign",
                input_pdf_manipulated.name,
                "--pem",
                str(RESOURCES_ROOT / "signing-certificate.crt"),
            ]
        )
    captured = capsys.readouterr()

    # Assert
    assert exit_code == 1
    assert "Check failed" in captured.err
    assert "Content hash not ok" in captured.err


def test_check_sign_missing_signature(
    capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    # Act
    with chdir(tmp_path):
        exit_code = run_cli(
            [
                "check-sign",
                str(RESOURCES_ROOT / "input8.pdf"),
                "--pem",
                str(RESOURCES_ROOT / "signing-certificate.crt"),
            ]
        )
    captured = capsys.readouterr()

    # Assert
    assert exit_code == 2
    assert "Signature missing" in captured.err


def test_check_sign_signature_not_matching_to_certificate(
    capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    # Act
    with chdir(tmp_path):
        exit_code = run_cli(
            [
                "check-sign",
                str(RESOURCES_ROOT / "sign_pkcs12.pdf"),
                "--pem",
                str(
                    RESOURCES_ROOT / "demo2_ca.root.crt.pem"
                ),  # sign_pkcs12.pdf signature matched to signing-certificate.crt
            ]
        )
    captured = capsys.readouterr()

    # Assert
    assert exit_code == 1
    assert "Check failed" in captured.err
    assert "Certificate not ok" in captured.err


def test_check_sign_pem(capsys: pytest.CaptureFixture, tmp_path: Path) -> None:
    # Act
    with chdir(tmp_path):
        exit_code = run_cli(
            [
                "check-sign",
                str(RESOURCES_ROOT / "sign_pkcs12.pdf"),
                "--pem",
                str(RESOURCES_ROOT / "signing-certificate.crt"),
            ]
        )
    captured = capsys.readouterr()

    # Assert
    assert exit_code == 0
    assert not captured.err


def test_check_sign_pdfly_signed_pdf(
    capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    # Arrange
    with chdir(tmp_path):
        exit_code = run_cli(
            [
                "sign",
                str(RESOURCES_ROOT / "input8.pdf"),
                "-o",
                str(tmp_path / "input8_signed.pdf"),
                "--p12",
                str(RESOURCES_ROOT / "signing-certificate.p12"),
                "--p12-password",
                "fpdf2",
            ]
        )
    captured = capsys.readouterr()

    # Act
    with chdir(tmp_path):
        exit_code = run_cli(
            [
                "check-sign",
                str(tmp_path / "input8_signed.pdf"),
                "--pem",
                str(RESOURCES_ROOT / "signing-certificate.crt"),
            ]
        )
    captured = capsys.readouterr()

    # Assert
    assert exit_code == 0
    assert not captured.err


def test_check_sign_verbose(capsys: pytest.CaptureFixture) -> None:
    exit_code = run_cli(
        [
            "check-sign",
            str(RESOURCES_ROOT / "sign_pkcs12.pdf"),
            "--pem",
            str(RESOURCES_ROOT / "signing-certificate.crt"),
            "--verbose",
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert not captured.err
    assert (
        "Check succeeded (Signature ok, Content hash ok, Certificate ok)."
        in captured.out
    )


def test_check_sign_malformed_byte_range(
    capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    pdf = tmp_path / "malformed.pdf"
    pdf.write_bytes(b"%PDF-1.7\n1 0 obj << /ByteRange [ 0 a 2 3 ] >> endobj\n")

    exit_code = run_cli(
        [
            "check-sign",
            str(pdf),
            "--pem",
            str(RESOURCES_ROOT / "signing-certificate.crt"),
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 2
    assert "Invalid signature: Invalid ByteRange data" in plain(captured.err)


def test_check_sign_invalid_signature(
    capsys: pytest.CaptureFixture, monkeypatch: pytest.MonkeyPatch
) -> None:
    # A signature that does not match its signed attributes, while the
    # content hash still matches, cannot be produced by editing the file
    # without also breaking its ASN.1 structure: stub the verifier instead.
    class Result:
        hashok = True
        signatureok = False
        certok = True

    class FakeVerifier:
        is_signed = True

        def __init__(self, *args: object) -> None:
            pass

        def verify_all_signatures(self) -> list[Result]:
            return [Result()]

    monkeypatch.setattr(pdfly.check_sign, "PDFVerifier", FakeVerifier)

    exit_code = run_cli(
        [
            "check-sign",
            str(RESOURCES_ROOT / "sign_pkcs12.pdf"),
            "--pem",
            str(RESOURCES_ROOT / "signing-certificate.crt"),
            "--verbose",
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 1
    assert (
        "Check failed (Signature not ok, Content hash ok, Certificate ok)."
        in captured.err
    )
