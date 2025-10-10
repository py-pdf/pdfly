import io
from fpdf import FPDF
from pypdf import PdfReader, PdfWriter
from .conftest import RESOURCES_ROOT, chdir, run_cli


def test_check_sign_manipulated_content(capsys, tmp_path):
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


def test_check_sign_missing_signature(capsys, tmp_path):
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


def test_check_sign_signature_not_matching_to_certificate(capsys, tmp_path):
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


def test_check_sign_pem(capsys, tmp_path):
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


def test_check_sign_pdfly_signed_pdf(capsys, tmp_path):
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
