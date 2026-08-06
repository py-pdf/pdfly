from pathlib import Path

import pytest

from .conftest import RESOURCES_ROOT, chdir, run_cli


def test_extract_links(capsys: pytest.CaptureFixture, tmp_path: Path) -> None:
    with chdir(tmp_path):
        run_cli(
            [
                "extract-links",
                str(RESOURCES_ROOT / "GeoBase_NHNC1_Data_Model_UML_EN.pdf"),
            ]
        )
    captured = capsys.readouterr()
    assert not captured.err
    assert "mailto:geoginfo@RNCan.gc.ca" in captured.out
