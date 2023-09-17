"""
Every CLI command is called here with a typer CliRunner.

Here should only be end-to-end tests.
"""

from pathlib import Path

from typer.testing import CliRunner

from pdfly.cli import entry_point

runner = CliRunner()


def test_x2pdf(tmp_path: Path) -> None:
    # Arrange
    output = tmp_path / "out.pdf"
    assert not output.exists()

    # Act
    result = runner.invoke(
        entry_point,
        [
            "x2pdf",
            "sample-files/003-pdflatex-image/page-0-Im1.jpg",
            str(output),
        ],
    )

    # Assert
    assert result.exit_code == 0, result.stdout
    assert result.stdout == ""
    assert output.exists()
