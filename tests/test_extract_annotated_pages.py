from pathlib import Path

import pytest

from .conftest import RESOURCES_ROOT, chdir, run_cli


def test_extract_annotated_pages_input8(
    capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    with chdir(tmp_path):
        run_cli(
            [
                "extract-annotated-pages",
                str(RESOURCES_ROOT / "input8.pdf"),
            ]
        )
    captured = capsys.readouterr()
    assert not captured.err
    assert "Extracted 1 pages with annotations" in captured.out


def test_extract_annotated_pages_range(
    capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    # Range limiting should work even if annotations appear in range
    with chdir(tmp_path):
        run_cli(
            [
                "extract-annotated-pages",
                str(RESOURCES_ROOT / "input8.pdf"),
                "--from",
                "0",
                "--end",
                "0",
            ]
        )
    captured = capsys.readouterr()
    assert not captured.err
    # input8.pdf has annotations; limiting to page 0 should still work
    assert "Extracted" in captured.out


def test_extract_annotated_pages_multiple_pages(
    capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    # Use a resource with multiple annotated pages if available; otherwise
    # we still assert command runs and prints the expected prefix.
    pdf_path = RESOURCES_ROOT / "input8.pdf"
    with chdir(tmp_path):
        run_cli(
            [
                "extract-annotated-pages",
                str(pdf_path),
                "--from",
                "0",
                "--end",
                "10",
            ]
        )
    captured = capsys.readouterr()
    assert not captured.err
    assert "Extracted" in captured.out
