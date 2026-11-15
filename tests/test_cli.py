import importlib
import runpy
import sys
from subprocess import check_output

import pytest
from pypdf import __version__ as pypdf_version

from .conftest import plain, run_cli


def test_pypdf_cli_can_be_invoked_as_a_module() -> None:
    stdout = check_output([sys.executable, "-m", "pdfly", "--help"]).decode()
    assert "pdfly [OPTIONS] COMMAND [ARGS]..." in stdout
    assert (
        "pdfly is a pure-python cli application for manipulating PDF files."
        in stdout
    )


@pytest.mark.parametrize(
    ("command", "description"),
    [
        (
            "2-up",
            "Put each pair of input pages side by side on one output page.",
        ),
        ("uncompress", "Uncompress the content streams of a PDF."),
    ],
)
def test_command_help_description(
    capsys: pytest.CaptureFixture[str], command: str, description: str
) -> None:
    exit_code = run_cli([command, "--help"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert not captured.err
    assert description in plain(captured.out)


def test_2up_help_example(capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = run_cli(["2-up", "--help"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "pdfly 2-up input.pdf output.pdf" in plain(captured.out)


def test_pypdf_cli_version(capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = run_cli(["--version"])
    captured = capsys.readouterr()
    assert not captured.err
    assert pypdf_version in captured.out
    assert exit_code == 0


def test_main_module(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    # Same as `python -m pdfly --version`, but in this process,
    # so that coverage measures pdfly/__main__.py
    monkeypatch.setattr(sys, "argv", ["pdfly", "--version"])

    with pytest.raises(SystemExit) as exc_info:
        runpy.run_module("pdfly", run_name="__main__")

    assert exc_info.value.code == 0
    assert pypdf_version in capsys.readouterr().out


def test_importing_main_module_does_not_run_the_cli(
    capsys: pytest.CaptureFixture[str],
) -> None:
    sys.modules.pop("pdfly.__main__", None)

    importlib.import_module("pdfly.__main__")

    assert capsys.readouterr().out == ""
