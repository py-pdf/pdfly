from endesive import pdf

from .conftest import RESOURCES_ROOT, chdir, run_cli


def test_sign_missing_certificate_key_option(capsys, tmp_path):
    # Act
    with chdir(tmp_path):
        exit_code = run_cli(
            ["sign", str(RESOURCES_ROOT / "input8.pdf"), "-o", "out.pdf"]
        )
    captured = capsys.readouterr()

    # Assert
    assert exit_code == 2
    assert "Missing option" in captured.err


def test_sign_already_signed_pdf(capsys, tmp_path):
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


def test_sign_pkcs12(capsys, tmp_path):
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
    results = pdf.verify(outpdf.read_bytes(), [certificate.read_bytes()])
    for hash_ok, signature_ok, cert_ok in results:
        assert signature_ok
        assert hash_ok
        assert cert_ok


def test_sign_pkcs12_in_place(capsys, tmp_path):
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
    results = pdf.verify(outpdf.read_bytes(), [certificate.read_bytes()])
    for hash_ok, signature_ok, cert_ok in results:
        assert signature_ok
        assert hash_ok
        assert cert_ok
