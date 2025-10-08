from .conftest import RESOURCES_ROOT, chdir, run_cli


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
