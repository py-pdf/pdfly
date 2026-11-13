import shutil
from pathlib import Path

import pytest

from .conftest import RESOURCES_ROOT, chdir, run_cli


def test_extract_annotated_pages_input8(
    capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    # The default output is written next to the input file,
    # so we work on a copy to keep the resources/ directory clean:
    input_pdf = tmp_path / "input8.pdf"
    shutil.copy(RESOURCES_ROOT / "input8.pdf", input_pdf)
    with chdir(tmp_path):
        run_cli(
            [
                "extract-annotated-pages",
                str(input_pdf),
            ]
        )
    captured = capsys.readouterr()
    assert not captured.err
    assert "Extracted 1 pages with annotations" in captured.out
    assert (tmp_path / "input8_annotated.pdf").exists()
