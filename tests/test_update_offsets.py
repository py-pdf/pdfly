"""
Every CLI command is called here with a typer CliRunner.

Here should only be end-to-end tests.
"""

import re
from pathlib import Path

import pytest

from .conftest import RESOURCES_ROOT, run_cli


def test_update_offsets(capsys, tmp_path: Path) -> None:
    # Arrange
    input = RESOURCES_ROOT / "file-with-invalid-offsets.pdf"
    file_expected = str(RESOURCES_ROOT / "file-with-fixed-offsets.pdf")

    # Act
    exit_code = run_cli(
        [
            "update-offsets",
            str(input),
        ]
    )

    # Assert
    captured = capsys.readouterr()
    assert exit_code == 0, captured
    assert not captured.err
    assert re.search(r"Wrote\s+" + re.escape(str(input)), captured.out)
    with open(file_expected, encoding="iso-8859-1") as file_exp:
        lines_exp = file_exp.readlines()
    with input.open(encoding="iso-8859-1") as file_act:
        lines_act = file_act.readlines()
    assert len(lines_exp) == len(
        lines_act
    ), f"lines_exp=f{lines_exp}, lines_act=f{lines_act}"
    for line_no, (line_exp, line_act) in enumerate(
        zip(lines_exp, lines_act), start=1
    ):
        assert line_exp == line_act, f"Lines differ in line {line_no}"


# The current implementation doesn't support valid PDF lines as "/Length 5470>> stream".


@pytest.mark.parametrize(
    "input_pdf_filepath",
    [
        "sample-files/002-trivial-libre-office-writer/002-trivial-libre-office-writer.pdf",
        "sample-files/005-libreoffice-writer-password/libreoffice-writer-password.pdf",
        "sample-files/007-imagemagick-images/imagemagick-ASCII85Decode.pdf",
        "sample-files/007-imagemagick-images/imagemagick-CCITTFaxDecode.pdf",
        "sample-files/007-imagemagick-images/imagemagick-images.pdf",
        "sample-files/007-imagemagick-images/imagemagick-lzw.pdf",
        "sample-files/008-reportlab-inline-image/inline-image.pdf",
        "sample-files/009-pdflatex-geotopo/GeoTopo-komprimiert.pdf",
        # "sample-files/011-google-doc-document/google-doc-document.pdf", # stream token in line after /Length
        "sample-files/012-libreoffice-form/libreoffice-form.pdf",
        "sample-files/013-reportlab-overlay/reportlab-overlay.pdf",
        "sample-files/015-arabic/habibi-oneline-cmap.pdf",
        "sample-files/015-arabic/habibi-rotated.pdf",
        "sample-files/015-arabic/habibi.pdf",
        "sample-files/016-libre-office-link/libre-office-link.pdf",
        # "sample-files/017-unreadable-meta-data/unreadablemetadata.pdf", # stream in line after object
        "sample-files/018-base64-image/base64image.pdf",
        # "sample-files/019-grayscale-image/grayscale-image.pdf", # stream in line after object
        "sample-files/020-xmp/output_with_metadata_pymupdf.pdf",
        # "sample-files/021-pdfa/crazyones-pdfa.pdf", # stream in line is after dictionary
        "sample-files/022-pdfkit/pdfkit.pdf",
        "sample-files/023-cmyk-image/cmyk-image.pdf",
        "sample-files/024-annotations/annotated_pdf.pdf",
        "sample-files/025-attachment/with-attachment.pdf",
    ],
)
def test_update_offsets_on_all_reference_files(
    capsys, tmp_path: Path, input_pdf_filepath: Path
) -> None:
    # Arrange
    output_pdf_filepath = tmp_path / "out.pdf"

    # Act
    exit_code = run_cli(
        [
            "update-offsets",
            "--encoding",
            "iso-8859-1",
            input_pdf_filepath,
            "-o",
            str(output_pdf_filepath),
        ]
    )

    # Assert
    captured = capsys.readouterr()
    assert exit_code == 0, captured
    assert not captured.err
    assert f"Wrote {output_pdf_filepath}" in captured.out
    assert output_pdf_filepath.exists()
