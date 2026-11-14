import importlib
import runpy
import sys
from subprocess import check_output

import pytest
from pypdf import __version__ as pypdf_version

from .conftest import run_cli


def test_pypdf_cli_can_be_invoked_as_a_module() -> None:
    stdout = check_output([sys.executable, "-m", "pdfly", "--help"]).decode()
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


def test_main_module(
    capsys: pytest.CaptureFixture, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Same as `python -m pdfly --version`, but in this process,
    # so that coverage measures pdfly/__main__.py
    monkeypatch.setattr(sys, "argv", ["pdfly", "--version"])

    with pytest.raises(SystemExit) as exc_info:
        runpy.run_module("pdfly", run_name="__main__")

    assert exc_info.value.code == 0
    assert pypdf_version in capsys.readouterr().out


def test_importing_main_module_does_not_run_the_cli(
    capsys: pytest.CaptureFixture,
) -> None:
    sys.modules.pop("pdfly.__main__", None)

    importlib.import_module("pdfly.__main__")

    assert capsys.readouterr().out == ""
