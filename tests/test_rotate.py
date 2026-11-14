from contextlib import chdir
from pathlib import Path

import pytest
from pypdf import PdfReader
from pypdf.errors import PdfStreamError

from .conftest import RESOURCES_ROOT, run_cli


def test_rotate_fewer_args(
    capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    with chdir(tmp_path):
        exit_code = run_cli(
            [
                "rotate",
            ]
        )
    assert exit_code == 2
    captured = capsys.readouterr()
    assert "Missing argument" in captured.err


def test_rotate_extra_args(
    capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    with chdir(tmp_path):
        exit_code = run_cli(
            [
                "rotate",
                "-o",
                "/dev/null",
                str(RESOURCES_ROOT / "box.pdf"),
                "37",
                "extra 1",
                "extra 2",
            ]
        )
    assert exit_code == 2
    captured = capsys.readouterr()
    assert "unexpected extra argument" in captured.err


def get_page_rotations(fname: str) -> list[int]:
    reader = PdfReader(fname)
    return [page.rotation for page in reader.pages]


def diff_rotations(
    in_: list[int], out: list[int], degrees: int = 0
) -> list[int]:
    diffs = []
    for orig, rotated in zip(in_, out):
        diffs.append(rotated - (orig + degrees))
    return diffs


def test_rotate_default(tmp_path: Path) -> None:
    in_fname = str(RESOURCES_ROOT / "input8.pdf")
    out_fname = "output8.pdf"
    degrees = 90

    with chdir(tmp_path):
        print(f"{tmp_path=}")
        exit_code = run_cli(
            [
                "rotate",
                "-o",
                out_fname,
                in_fname,
                str(degrees),
            ]
        )
        in_rotations = get_page_rotations(in_fname)
        out_rotations = get_page_rotations(out_fname)

    assert exit_code == 0

    assert not any(diff_rotations(in_rotations, out_rotations, degrees))


@pytest.mark.parametrize(
    # NB "slice" can not be specified as the empty string
    ("degrees", "slice", "expected_diff"),
    [
        (90, ":", [90, 90, 90, 90, 90, 90, 90, 90]),  # every page
        (90, "::2", [90, 0, 90, 0, 90, 0, 90, 0]),  # every other, even index
        (90, "1::2", [0, 90, 0, 90, 0, 90, 0, 90]),  # every other, odd index
        (90, ":2", [90, 90, 0, 0, 0, 0, 0, 0]),  # first 2
        (
            -90,
            ":",
            [-90, -90, -90, -90, -90, -90, -90, -90],
        ),  # negative degrees works
        (
            -720,
            ":",
            [-720, -720, -720, -720, -720, -720, -720, -720],
        ),  # |degrees| > 360 is also supported
    ],
)
def test_rotate_slices(
    capsys: pytest.CaptureFixture,
    tmp_path: Path,
    degrees: int,
    slice: str,
    expected_diff: list[int],
) -> None:
    in_fname = str(RESOURCES_ROOT / "input8.pdf")
    out_fname = "output.pdf"
    with chdir(tmp_path):
        args = [
            "rotate",
            "-o",
            f"{out_fname}",
            f"{in_fname}",
            "--",  # end options, so negative degree values work
            f"{degrees}",
            f"{slice}",
        ]
        exit_code = run_cli(args)
        captured = capsys.readouterr()
        assert exit_code == 0, captured.err

        in_rotations = get_page_rotations(in_fname)
        out_rotations = get_page_rotations(out_fname)
        actual_diff = diff_rotations(in_rotations, out_rotations)

    assert not any(diff_rotations(actual_diff, expected_diff))


def test_rotate_invalid_pdf(
    capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    not_a_pdf = tmp_path / "not-a-pdf.pdf"
    not_a_pdf.write_text("This is not a PDF")

    with pytest.raises(PdfStreamError):
        run_cli(
            ["rotate", "-o", str(tmp_path / "out.pdf"), str(not_a_pdf), "90"]
        )

    # Rich wraps long lines, so compare with normalized whitespace:
    out = " ".join(capsys.readouterr().out.split())
    assert f"Error while rotating {not_a_pdf}" in out
    assert not (tmp_path / "out.pdf").exists()
