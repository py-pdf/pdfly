import pytest
from pypdf import PdfReader

from .conftest import RESOURCES_ROOT, chdir, run_cli


def test_booklet_fewer_args(capsys, tmp_path):
    with chdir(tmp_path):
        exit_code = run_cli(["cat", str(RESOURCES_ROOT / "box.pdf")])
    assert exit_code == 2
    captured = capsys.readouterr()
    assert "Missing argument" in captured.err


def test_booklet_extra_args(capsys, tmp_path):
    with chdir(tmp_path):
        exit_code = run_cli(
            ["booklet", str(RESOURCES_ROOT / "box.pdf"), "a.pdf", "b.pdf"]
        )
    assert exit_code == 2
    captured = capsys.readouterr()
    assert "unexpected extra argument" in captured.err


def test_booklet_page_size(capsys, tmp_path):
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
        ("8", "81\n27\n63\n45\n", "81\n27\n63\n45\n"),
        ("7", "71\n2\n63\n45\n", "71\n2b\n63\n45\n"),
        ("6", "61\n25\n43\n\n", "61\n25\n43\nc\n"),
        ("5", "51\n2\n43\n\n", "51\n2b\n43\nc\n"),
        ("4", "41\n23\n", "41\n23\n"),
        ("3", "31\n2\n", "31\n2b\n"),
        ("2", "21\n\n", "21\nc\n"),
        ("1", "1\n\n", "1b\nc\n"),
    ],
)
def test_booklet_order(capsys, tmp_path, page_count, expected, expected_bc):
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
