from pathlib import Path

import pytest

from .conftest import RESOURCES_ROOT, chdir, run_cli


def test_extract_text_echo(
    capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    with chdir(tmp_path):
        run_cli(
            [
                "extract-text",
                str(RESOURCES_ROOT / "input8.pdf"),
            ]
        )
    captured = capsys.readouterr()
    assert not captured.err
    assert (
        """1
2
3
4
5
6
7
8"""
        in captured.out
    )


def test_extract_text_with_pattern(
    capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    with chdir(tmp_path):
        run_cli(
            [
                "extract-text",
                str(RESOURCES_ROOT / "input8.pdf"),
                "-o",
                "page-[].txt",
            ]
        )
    captured = capsys.readouterr()
    assert not captured.err
    files_exist = True
    output_correct = True
    for i in range(8):
        try:
            file = open(tmp_path / f"page-{i}.txt", "r")
            if file.read() != f"{i+1}\n":
                output_correct = False
        except:
            files_exist = False
    assert files_exist
    assert output_correct
