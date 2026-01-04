import json
from pathlib import Path

import pytest

from .conftest import RESOURCES_ROOT, chdir, run_cli


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
