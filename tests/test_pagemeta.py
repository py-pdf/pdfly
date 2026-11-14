import json
import re
from contextlib import chdir
from pathlib import Path

import pytest
from fpdf import FPDF
from pypdf import PdfWriter

from .conftest import RESOURCES_ROOT, run_cli


def test_pagemeta_json(capsys: pytest.CaptureFixture, tmp_path: Path) -> None:
    with chdir(tmp_path):
        run_cli(
            ["pagemeta", str(RESOURCES_ROOT / "box.pdf"), "0", "-o", "json"]
        )
    captured = capsys.readouterr()
    assert not captured.err
    page_metadata = json.loads(captured.out)
    assert page_metadata["mediabox"] == [0.0, 0.0, 60.0, 60.0]
    assert page_metadata["cropbox"] == [0.0, 0.0, 60.0, 60.0]
    assert page_metadata["artbox"] == [0.0, 0.0, 60.0, 60.0]
    assert page_metadata["bleedbox"] == [0.0, 0.0, 60.0, 60.0]


def test_pagemeta_text_with_known_format(
    capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    with chdir(tmp_path):
        run_cli(["pagemeta", str(RESOURCES_ROOT / "c.pdf"), "0"])
    captured = capsys.readouterr()
    assert not captured.err
    assert "(Letter)" in captured.out


def test_pagemeta_text_with_close_format(
    capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    with chdir(tmp_path):
        run_cli(["pagemeta", str(RESOURCES_ROOT / "jpeg.pdf"), "0"])
    captured = capsys.readouterr()
    assert not captured.err
    assert "close to format: A4" in captured.out


def test_pagemeta_text_with_annotations_and_rotation(
    capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    pdf = FPDF()
    pdf.add_page()
    pdf.text_annotation(x=10, y=10, text="A note")
    input_pdf = tmp_path / "in.pdf"
    pdf.output(input_pdf)
    writer = PdfWriter(clone_from=input_pdf)
    writer.pages[0].rotate(90)
    writer.write(input_pdf)

    exit_code = run_cli(["pagemeta", str(input_pdf), "0"])

    captured = capsys.readouterr()
    assert exit_code == 0, captured.err
    assert not captured.err
    assert re.search(r"annotations\W+1\b", captured.out)
    assert re.search(r"rotation\W+90\b", captured.out)
    assert "All annotations:" in captured.out
    assert "1. /Text at" in captured.out


def test_pagemeta_text_with_unknown_format(
    capsys: pytest.CaptureFixture,
) -> None:
    # box.pdf is 60x60 pt: no paper format is close to that
    exit_code = run_cli(["pagemeta", str(RESOURCES_ROOT / "box.pdf"), "0"])

    captured = capsys.readouterr()
    assert exit_code == 0, captured.err
    # The size is not followed by the name of a format:
    assert re.search(
        r"width=60\.00 x height=60\.00\W*$", captured.out, re.MULTILINE
    )
    assert "format" not in captured.out
    # No annotations and no rotation: those rows are omitted
    assert "annotations" not in captured.out
    assert "rotation" not in captured.out
