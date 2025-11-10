import sys
from subprocess import check_output

import pytest
from pypdf import __version__ as pypdf_version

from .conftest import run_cli


def test_pypdf_cli_can_be_invoked_as_a_module() -> None:
    stdout = check_output(  # noqa: S603
        [sys.executable, "-m", "pdfly", "--help"]
    ).decode()
    assert "pdfly [OPTIONS] COMMAND [ARGS]..." in stdout
    assert (
        "pdfly is a pure-python cli application for manipulating PDF files."
        in stdout
    )


def test_pypdf_cli_version(capsys: pytest.CaptureFixture) -> None:
    exit_code = run_cli(["--version"])
    captured = capsys.readouterr()
    assert not captured.err
    assert pypdf_version in captured.out
    assert exit_code == 0
