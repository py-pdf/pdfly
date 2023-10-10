"""
Every CLI command is called here with a typer CliRunner.

Here should only be end-to-end tests.
"""

from pathlib import Path

from .conftest import run_cli


def test_x2pdf(capsys, tmp_path: Path) -> None:
    # Arrange
    output = tmp_path / "out.pdf"
    assert not output.exists()

    # Act
    exit_code = run_cli(
        [
            "x2pdf",
            "sample-files/003-pdflatex-image/page-0-Im1.jpg",
            "--output",
            str(output),
        ]
    )

    # Assert
    captured = capsys.readouterr()
    assert exit_code == 0, captured
    assert captured.out == ""
    assert output.exists()
