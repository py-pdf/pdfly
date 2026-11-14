from contextlib import chdir
from pathlib import Path

import pytest
from pypdf import PdfReader, PdfWriter

from pdfly import booklet

from .conftest import RESOURCES_ROOT, run_cli


def test_booklet_fewer_args(
    capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    with chdir(tmp_path):
        exit_code = run_cli(["booklet", str(RESOURCES_ROOT / "box.pdf")])
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
        assert captured.out.split() == expected.split()
        assert page_words(f"output{page_count}.pdf") == page_words_of(expected)

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
        assert captured.out.split() == expected_bc.split()
        assert page_words(f"outputbc{page_count}.pdf") == page_words_of(
            expected_bc
        )


def page_words(filename: str) -> list[list[str]]:
    # Compare words rather than raw text: whether pypdf joins the two halves
    # of a booklet page with a space or a newline depends on its version.
    return [page.extract_text().split() for page in PdfReader(filename).pages]


def page_words_of(expected: str) -> list[list[str]]:
    """Parse an expectation with one line per output page."""
    return [line.split() for line in expected.splitlines()]


def test_booklet_rotated_centerfold(tmp_path: Path) -> None:
    # A /Rotate 90 portrait page is landscape once its rotation is
    # transferred to its content, like the booklet sheet it is merged into:
    centerfold = tmp_path / "rotated-c.pdf"
    writer = PdfWriter(clone_from=RESOURCES_ROOT / "c.pdf")
    writer.pages[0].rotate(90)
    writer.write(centerfold)
    input6 = tmp_path / "input6.pdf"
    writer = PdfWriter()
    writer.append(RESOURCES_ROOT / "input8.pdf", pages=(0, 6))
    writer.write(input6)

    exit_code = run_cli(
        [
            "booklet",
            "--centerfold-file",
            str(centerfold),
            str(input6),
            str(tmp_path / "output.pdf"),
        ]
    )

    assert exit_code == 0
    assert page_words(str(tmp_path / "output.pdf")) == page_words_of(
        "6 1\n2 5\n4 3\nc\n"
    )
    last_page = PdfReader(tmp_path / "output.pdf").pages[-1]
    assert last_page.rotation == 0


def test_booklet_invalid_input(tmp_path: Path) -> None:
    not_a_pdf = tmp_path / "not-a-pdf.pdf"
    not_a_pdf.write_text("This is not a PDF")

    with pytest.raises(RuntimeError, match="Error while processing"):
        booklet.main(not_a_pdf, tmp_path / "out.pdf", None, None)
    assert not (tmp_path / "out.pdf").exists()


@pytest.mark.parametrize("num_pages", [1, 2, 3, 5, 6, 7])
def test_page_iter_requires_multiple_of_4(num_pages: int) -> None:
    with pytest.raises(ValueError, match="divisible by 4"):
        list(booklet.page_iter(num_pages))


def test_page_iter() -> None:
    assert list(booklet.page_iter(8)) == [(7, 0), (1, 6), (5, 2), (3, 4)]
