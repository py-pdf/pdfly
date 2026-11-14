"""Tests for the `uncompress` command."""

from pathlib import Path

import pytest
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, StreamObject

from .conftest import PROJECT_ROOT, run_cli

SAMPLE_FILES = sorted((PROJECT_ROOT / "sample-files").rglob("*.pdf"))


def content_streams(reader: PdfReader) -> list[StreamObject]:
    streams: list[StreamObject] = []
    for page in reader.pages:
        contents = page.get("/Contents")
        if contents is None:
            continue
        contents = contents.get_object()
        items = contents if isinstance(contents, ArrayObject) else [contents]
        streams.extend(item.get_object() for item in items)
    return streams


@pytest.mark.parametrize(
    "input_pdf_filepath",
    [
        pytest.param(path, id=path.parent.name)
        for path in SAMPLE_FILES
        if path.parent.name
        not in (
            # Encrypted, and uncompress has no --password option:
            "005-libreoffice-writer-password",
            # Its /Pages tree is broken: pypdf cannot list its pages
            "017-unreadable-meta-data",
        )
    ],
)
def test_uncompress_all_sample_files(
    input_pdf_filepath: Path, tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    output_pdf_filepath = tmp_path / "uncompressed_output.pdf"

    exit_code = run_cli(
        ["uncompress", str(input_pdf_filepath), str(output_pdf_filepath)]
    )

    captured = capsys.readouterr()
    assert exit_code == 0, captured.err
    assert "Uncompressed Size" in captured.out
    reader_in = PdfReader(input_pdf_filepath)
    reader_out = PdfReader(output_pdf_filepath)
    assert len(reader_out.pages) == len(reader_in.pages)
    for stream in content_streams(reader_out):
        assert "/Filter" not in stream, "Content stream is still compressed"
    # The decoded page contents are unchanged:
    for page_in, page_out in zip(
        reader_in.pages, reader_out.pages, strict=True
    ):
        contents_in = page_in.get_contents()
        contents_out = page_out.get_contents()
        if contents_in is None:
            assert contents_out is None
        else:
            assert contents_out is not None
            assert contents_out.get_data() == contents_in.get_data()


def test_uncompress_found_sample_files() -> None:
    # Guard against the sample-files submodule not being checked out,
    # which would silently skip test_uncompress_all_sample_files
    assert len(SAMPLE_FILES) > 10


def test_uncompress_page_without_contents(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    input_pdf = tmp_path / "blank.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=100, height=100)
    writer.write(input_pdf)
    output_pdf = tmp_path / "out.pdf"

    exit_code = run_cli(["uncompress", str(input_pdf), str(output_pdf)])

    assert exit_code == 0, capsys.readouterr().err
    page = PdfReader(output_pdf).pages[0]
    assert "/Contents" not in page
