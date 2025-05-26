from pathlib import Path
from typing import List
import pytest
from pypdf import PdfReader

from .conftest import RESOURCES_ROOT, chdir, run_cli


def test_rotate_fewer_args(capsys, tmp_path):
    with chdir(tmp_path):
        exit_code = run_cli(
            [
                "rotate",
            ]
        )
    assert exit_code == 2
    captured = capsys.readouterr()
    assert "Missing argument" in captured.err


def test_rotate_extra_args(capsys, tmp_path):
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


def get_page_rotations(fname: Path) -> List[int]:
    reader = PdfReader(fname)
    rotations = []
    for page in reader.pages:
        rotations.append(page.rotation)
    return rotations


def diff_rotations(
    in_: List[int], out: List[int], degrees: int = 0
) -> List[int]:
    diffs = []
    for orig, rotated in zip(in_, out):
        diffs.append(rotated - (orig + degrees))
    return diffs


def test_rotate_default(capsys, tmp_path):
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
def test_rotate_slices(capsys, tmp_path, degrees, slice, expected_diff):
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
