from pathlib import Path

import pytest
from pypdf import PdfReader

from .conftest import RESOURCES_ROOT, chdir, run_cli


def test_booklet_fewer_args(
    capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    with chdir(tmp_path):
        exit_code = run_cli(["cat", str(RESOURCES_ROOT / "box.pdf")])
    assert exit_code == 2
    captured = capsys.readouterr()
    assert "Missing" in captured.err


def test_booklet_extra_args(
    capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    with chdir(tmp_path):
        exit_code = run_cli(
            ["booklet", str(RESOURCES_ROOT / "box.pdf"), "a.pdf", "b.pdf"]
        )
    assert exit_code == 2
    captured = capsys.readouterr()
    assert "unexpected extra argument" in captured.err


def test_booklet_page_size(tmp_path: Path) -> None:
    in_fname = str(RESOURCES_ROOT / "input8.pdf")

    with chdir(tmp_path):
        exit_code = run_cli(
            [
                "booklet",
                in_fname,
                "output8.pdf",
            ]
        )
        in_reader = PdfReader(in_fname)
        out_reader = PdfReader("output8.pdf")

    assert exit_code == 0

    assert len(in_reader.pages) == 8
    assert len(out_reader.pages) == 4

    in_height = in_reader.pages[0].mediabox.height
    in_width = in_reader.pages[0].mediabox.width
    out_height = out_reader.pages[0].mediabox.height
    out_width = out_reader.pages[0].mediabox.width

    assert out_width == in_width * 2
    assert in_height == out_height


@pytest.mark.parametrize(
    ("page_count", "expected", "expected_bc"),
    [
        ("8", "8 1\n2 7\n6 3\n4 5\n", "8 1\n2 7\n6 3\n4 5\n"),
        ("7", "7 1\n2\n6 3\n4 5\n", "7 1\n2 b\n6 3\n4 5\n"),
        ("6", "6 1\n2 5\n4 3\n\n", "6 1\n2 5\n4 3\nc\n"),
        ("5", "5 1\n2\n4 3\n\n", "5 1\n2 b\n4 3\nc\n"),
        ("4", "4 1\n2 3\n", "4 1\n2 3\n"),
        ("3", "3 1\n2\n", "3 1\n2 b\n"),
        ("2", "2 1\n\n", "2 1\nc\n"),
        ("1", "1\n\n", "1 b\nc\n"),
    ],
)
def test_booklet_order(
    capsys: pytest.CaptureFixture,
    tmp_path: Path,
    page_count: str,
    expected: str,
    expected_bc: str,
) -> None:
    with chdir(tmp_path):
        exit_code = run_cli(
            [
                "cat",
                "-o",
                f"input{page_count}.pdf",
                str(RESOURCES_ROOT / "input8.pdf"),
                f":{page_count}",
            ]
        )
        assert exit_code == 0

        exit_code = run_cli(
            [
                "booklet",
                f"input{page_count}.pdf",
                f"output{page_count}.pdf",
            ]
        )
        captured = capsys.readouterr()
        assert exit_code == 0, captured.err

        exit_code = run_cli(
            [
                "extract-text",
                f"output{page_count}.pdf",
            ]
        )
        captured = capsys.readouterr()
        assert exit_code == 0, captured.err
        assert captured.out == expected

        exit_code = run_cli(
            [
                "booklet",
                "--centerfold-file",
                str(RESOURCES_ROOT / "c.pdf"),
                "--blank-page-file",
                str(RESOURCES_ROOT / "b.pdf"),
                f"input{page_count}.pdf",
                f"outputbc{page_count}.pdf",
            ]
        )
        captured = capsys.readouterr()
        assert exit_code == 0, captured.err

        exit_code = run_cli(
            [
                "extract-text",
                f"outputbc{page_count}.pdf",
            ]
        )
        captured = capsys.readouterr()
        assert exit_code == 0, captured.err
        assert captured.out == expected_bc
