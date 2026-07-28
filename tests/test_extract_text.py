"""Tests for extract-text's page-range, multi-file, and output-to-file
support.

Covers slicing, negative/out-of-range indices, combining multiple
files (each with its own range) in argument order, repeated files,
writing to a file instead of stdout, and the malformed-range /
invalid-filepath error contract shared with cat and rm.
extract-text's --password support is covered in
test_password_support alongside the other commands that
gained it in this change.
"""

from pathlib import Path

import pytest

from .conftest import RESOURCES_ROOT, chdir, run_cli


def get_extracted_numbers(output: str) -> list[int]:
    """pdf_file_100 pages each contain only the page index as text."""
    return [int(line) for line in output.splitlines() if line.strip()]


def get_extracted_letters(output: str) -> list[str]:
    """pdf_file_abc pages each contain only a single letter as text."""
    return [line for line in output.splitlines() if line.strip()]

@pytest.mark.parametrize(
    ("slice", "expected"),
    [
        (":", list(range(100))),  # every page
        (":5", [0, 1, 2, 3, 4]),  # first five
        ("95:", [95, 96, 97, 98, 99]),  # from page 95 onward
        ("::2", list(range(0, 100, 2))),  # every other, even index
        ("1::2", list(range(1, 100, 2))),  # every other, odd index
        ("2::-1", [2, 1, 0]),  # reversed, first three
        ("::-1", list(range(99, -1, -1))),  # full-document reverse order
        ("95:200", [95, 96, 97, 98, 99]),  # out-of-bounds end, clamps like slice
    ],
)
def test_extract_text_slices(
    capsys: pytest.CaptureFixture,
    pdf_file_100: Path,
    slice: str,
    expected: list[int],
) -> None:
    args = [
        "extract-text",
        str(pdf_file_100),
        "--",  # end options, so negative slice values work
        slice,
    ]
    exit_code = run_cli(args)
    captured = capsys.readouterr()

    assert exit_code == 0, captured.err
    assert get_extracted_numbers(captured.out) == expected


def test_extract_text_negative_index(
    capsys: pytest.CaptureFixture, pdf_file_100: Path
) -> None:
    args = ["extract-text", str(pdf_file_100), "--", "-1"]
    exit_code = run_cli(args)
    captured = capsys.readouterr()

    assert exit_code == 0, captured.err
    assert get_extracted_numbers(captured.out) == [99]


def test_extract_text_single_page(
    capsys: pytest.CaptureFixture, pdf_file_100: Path
) -> None:
    exit_code = run_cli(["extract-text", str(pdf_file_100), "42"])
    captured = capsys.readouterr()

    assert exit_code == 0, captured.err
    assert get_extracted_numbers(captured.out) == [42]


def test_extract_text_malformed_range(
    capsys: pytest.CaptureFixture, pdf_file_100: Path, tmp_path: Path
) -> None:
    """A malformed range should fail the same way cat/rm do today: a
    clean exit code 2 plus an "invalid file path or page range" message,
    since extract-text now shares cat's multi-file/multi-range parser."""
    with chdir(tmp_path):
        exit_code = run_cli(
            ["extract-text", str(pdf_file_100), "not-a-range"]
        )
    captured = capsys.readouterr()
    assert exit_code == 2
    assert "Error: invalid file path or page range provided" in captured.out


def test_extract_text_invalid_filepath(
    capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    """A nonexistent path given as a second (or later) file argument goes
    through the shared cat/rm parser and must fail the same way: exit
    code 2 with the exact "invalid file path or page range" message on
    stdout. (The first, primary filename argument is validated earlier
    by typer's own exists=True check and is covered separately.)"""
    with chdir(tmp_path):
        exit_code = run_cli(
            [
                "extract-text",
                str(RESOURCES_ROOT / "box.pdf"),
                "does-not-exist.pdf",
            ]
        )
    captured = capsys.readouterr()
    assert exit_code == 2
    assert (
        "Error: invalid file path or page range provided" in captured.out
    )
    assert "does-not-exist.pdf" in captured.out


def test_extract_text_combine_files(
    capsys: pytest.CaptureFixture,
    pdf_file_100: Path,
    pdf_file_abc: Path,
    tmp_path: Path,
) -> None:
    """Multiple files, each with its own page range, print in the order
    they were given -- same convention as `cat`."""
    with chdir(tmp_path):
        exit_code = run_cli(
            [
                "extract-text",
                str(pdf_file_100),
                "1:4",
                str(pdf_file_abc),
                "::2",
            ]
        )
    captured = capsys.readouterr()
    assert exit_code == 0, captured.err

    lines = [line for line in captured.out.splitlines() if line.strip()]
    assert lines[:3] == ["1", "2", "3"]
    assert lines[3:] == list("acegikmoqsuwy")


def test_extract_text_repeated_file(
    capsys: pytest.CaptureFixture, pdf_file_abc: Path, tmp_path: Path
) -> None:
    """The same file may be named twice, each time with a different
    page range applying only to the pages named after it."""
    with chdir(tmp_path):
        exit_code = run_cli(
            [
                "extract-text",
                str(pdf_file_abc),
                "0",
                str(pdf_file_abc),
                "--",
                "-1",
            ]
        )
    captured = capsys.readouterr()
    assert exit_code == 0, captured.err
    assert get_extracted_letters(captured.out) == ["a", "z"]


def test_extract_text_output_to_file(
    capsys: pytest.CaptureFixture, pdf_file_100: Path, tmp_path: Path
) -> None:
    out_path = tmp_path / "extracted.txt"
    exit_code = run_cli(
        [
            "extract-text",
            str(pdf_file_100),
            ":3",
            "--output",
            str(out_path),
        ]
    )
    captured = capsys.readouterr()
    assert exit_code == 0, captured.err
    assert not captured.out

    assert get_extracted_numbers(out_path.read_text()) == [0, 1, 2]


def test_extract_text_output_to_file_short_option(
    capsys: pytest.CaptureFixture, pdf_file_100: Path, tmp_path: Path
) -> None:
    out_path = tmp_path / "extracted.txt"
    exit_code = run_cli(
        [
            "extract-text",
            str(pdf_file_100),
            ":3",
            "-o",
            str(out_path),
        ]
    )
    captured = capsys.readouterr()
    assert exit_code == 0, captured.err
    assert not captured.out

    assert get_extracted_numbers(out_path.read_text()) == [0, 1, 2]