"""
Every CLI command is called here with a typer CliRunner.

Here should only be end-to-end tests.
"""

from pathlib import Path

from .conftest import run_cli


def test_x2pdf_with_format(capsys, tmp_path: Path) -> None:
    # Arrange
    output = tmp_path / "out.pdf"
    assert not output.exists()
    
    formats_to_test = [
        "Letter",
        "A4-portrait",
        "A4-landscape",
        "210x297",
        "invalid-format"
    ]
    
    for format_option in formats_to_test:
        # Act
        exit_code = run_cli(
            [
                "x2pdf",
                "sample-files/003-pdflatex-image/page-0-Im1.jpg",
                "--output",
                str(output),
                "--format",
                format_option,
            ]
        )

        # Assert
        captured = capsys.readouterr()
        
        # For valid formats, we expect a successful exit code and the output file to exist
        if format_option != "invalid-format":
            assert exit_code == 0, captured
            assert captured.out == ""
            assert output.exists()
        else:
            # For an invalid format, we expect a non-zero exit code (indicating failure)
            assert exit_code != 0
            assert "Invalid format" in captured.err  # Check for expected error message
        output.unlink(missing_ok=True)  # Clean up for the next test iteration
