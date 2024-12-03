import os
import pytest
from pypdf import PdfReader

from .conftest import RESOURCES_ROOT, chdir, run_cli


def test_up2_fewer_args(capsys, tmp_path):
    with chdir(tmp_path):
        exit_code = run_cli(["2-up", str(RESOURCES_ROOT / "box.pdf")])
    assert exit_code == 2
    captured = capsys.readouterr()
    assert "Missing argument" in captured.err


def test_up2_extra_args(capsys, tmp_path):
    with chdir(tmp_path):
        exit_code = run_cli(
            [
                "2-up",
                str(RESOURCES_ROOT / "box.pdf"),
                "./out.pdf",
                "./out2.pdf",
            ]
        )

    assert exit_code == 2
    captured = capsys.readouterr()
    assert "unexpected extra argument" in captured.err

    with chdir(tmp_path):
        assert not os.path.exists("out.pdf"), f"'out.pdf' should not exist."
        assert not os.path.exists("out2.pdf"), f"'out2.pdf' should not exist."


def test_up2_8page_file(capsys, tmp_path):
    # Act
    with chdir(tmp_path):
        exit_code = run_cli(
            [
                "2-up",
                str(RESOURCES_ROOT / "input8.pdf"),
                "./out.pdf",
            ]
        )
    captured = capsys.readouterr()

    # Assert
    assert exit_code == 0, captured
    assert not captured.err
    in_reader = PdfReader(RESOURCES_ROOT / "input8.pdf")
    out_reader = PdfReader(tmp_path / "./out.pdf")

    assert len(in_reader.pages) == 8
    assert len(out_reader.pages) == 4

    in_width = in_reader.pages[0].mediabox.width
    in_height = in_reader.pages[0].mediabox.height
    out_width = out_reader.pages[0].mediabox.width
    out_height = out_reader.pages[0].mediabox.height

    assert out_width == 2 * in_width  # PR #78
    assert out_height == out_height
