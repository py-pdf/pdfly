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


def test_extract_text_range(capsys: pytest.CaptureFixture, tmp_path) -> None:
    # Ensure extract-text supports --from/--end by invoking help and a small range
    # Use a small, known resource PDF
    from pathlib import Path
    from .conftest import RESOURCES_ROOT, chdir

    pdf = RESOURCES_ROOT / "GeoBase_NHNC1_Data_Model_UML_EN.pdf"
    with chdir(tmp_path):
        run_cli(
            ["extract-text", str(pdf), "--from", "0", "--end", "0"]
        )  # one page
    captured = capsys.readouterr()
    assert not captured.err
    # We expect some non-empty text output for that page
    assert captured.out.strip() != ""


def test_extract_text_multipage_range(
    capsys: pytest.CaptureFixture, tmp_path
) -> None:
    # Extract text from a multipage range and ensure content is produced
    from pathlib import Path
    from .conftest import RESOURCES_ROOT, chdir

    pdf = RESOURCES_ROOT / "GeoBase_NHNC1_Data_Model_UML_EN.pdf"
    with chdir(tmp_path):
        run_cli(
            ["extract-text", str(pdf), "--from", "0", "--end", "1"]
        )  # two pages
    captured = capsys.readouterr()
    assert not captured.err
    out = captured.out.strip()
    assert out != ""
    # Heuristic: expect at least some newline separation for multiple pages
    assert "\n" in out
