"""Unit tests for update_offsets.update_lines() and read_binary_file()."""

from io import BytesIO, StringIO
from pathlib import Path

import pytest
from pypdf import PdfReader
from rich.console import Console

from pdfly.update_offsets import read_binary_file, update_lines

HEADER = "%PDF-1.4\n"
OBJECTS = (
    "1 0 obj\n"
    "<< /Type /Catalog /Pages 2 0 R >>\n"
    "endobj\n"
    "2 0 obj\n"
    "<< /Type /Pages /Kids [3 0 R] /Count 1 >>\n"
    "endobj\n"
    "3 0 obj\n"
    "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 100 100] /Contents 4 0 R >>\n"
    "endobj\n"
)
STREAM_OBJECT = "4 0 obj\n<< /Length 00 >>\nstream\nBT ET\nendstream\nendobj\n"
# The offsets are all wrong on purpose: update_lines() has to fix them
XREF = (
    "xref\n"
    "0 5\n"
    "0000000000 65535 f \n"
    "0000000000 00000 n \n"
    "0000000000 00000 n \n"
    "0000000000 00000 n \n"
    "0000000000 00000 n \n"
)
TRAILER = "trailer << /Size 5 /Root 1 0 R >>\n"
STARTXREF = "startxref\n0\n"
EOF = "%%EOF\n"


def make_pdf(
    stream_object: str = STREAM_OBJECT,
    extra_objects: str = "",
    xref: str = XREF,
    startxref: str = STARTXREF,
) -> list[str]:
    pdf = HEADER + OBJECTS + stream_object + extra_objects + xref
    pdf += TRAILER + startxref + EOF
    return pdf.splitlines(keepends=True)


def run_update_lines(
    lines: list[str], verbose: bool = False
) -> tuple[bytes, str]:
    output = StringIO()
    console = Console(file=output, width=200)
    lines_out = update_lines(lines, "iso-8859-1", console, verbose)
    return "".join(lines_out).encode("iso-8859-1"), output.getvalue()


def assert_xref_offsets_are_correct(pdf: bytes) -> None:
    reader = PdfReader(BytesIO(pdf), strict=True)
    for idnum, offset in reader.xref[0].items():
        assert pdf[offset:].startswith(f"{idnum} 0 obj".encode()), idnum


def test_update_lines() -> None:
    pdf, log = run_update_lines(make_pdf(), verbose=True)

    assert_xref_offsets_are_correct(pdf)
    assert b"<< /Length 05 >>" in pdf  # len("BT ET")
    reader = PdfReader(BytesIO(pdf), strict=True)
    contents = reader.pages[0].get_contents()
    assert contents is not None
    assert contents.get_data() == b"BT ET"
    for message in (
        "line 2: object 1",
        "line 11: object 4",
        "line 12, /Length: << /Length 00 >>",
        "line 13: start stream",
        "line 15: end stream",
        "line 15: Computed /Length 5 of obj 4",
        # The xref entry of object 1, which starts after "%PDF-1.4\n":
        "0000000000 00000 n  -> 0000000009 00000 n",
    ):
        assert message in log


def test_update_lines_not_verbose() -> None:
    pdf, log = run_update_lines(make_pdf(), verbose=False)

    assert_xref_offsets_are_correct(pdf)
    assert log == ""


def test_update_lines_empty_stream() -> None:
    stream_object = STREAM_OBJECT.replace("BT ET\n", "")

    pdf, _ = run_update_lines(make_pdf(stream_object))

    assert_xref_offsets_are_correct(pdf)
    assert b"<< /Length 00 >>" in pdf


def test_update_lines_length_reference() -> None:
    stream_object = STREAM_OBJECT.replace("/Length 00", "/Length 5 0 R")
    length_object = "5 0 obj\n00\nendobj\n"
    xref = XREF.replace("0 5\n", "0 6\n") + "0000000000 00000 n \n"

    pdf, log = run_update_lines(
        make_pdf(stream_object, length_object, xref), verbose=True
    )

    assert_xref_offsets_are_correct(pdf)
    assert b"5 0 obj\n05\nendobj\n" in pdf
    assert "line 12, /Length-reference 5 0 R: << /Length 5 0 R >>" in log
    assert "ref-len 5 of 4: 00 -> 05" in log


def test_update_lines_length_reference_already_correct() -> None:
    stream_object = STREAM_OBJECT.replace("/Length 00", "/Length 5 0 R")
    length_object = "5 0 obj\n05\nendobj\n"
    xref = XREF.replace("0 5\n", "0 6\n") + "0000000000 00000 n \n"
    lines = make_pdf(stream_object, length_object, xref)

    pdf, log = run_update_lines(lines, verbose=True)

    assert_xref_offsets_are_correct(pdf)
    assert b"5 0 obj\n05\nendobj\n" in pdf
    assert "ref-len" not in log


@pytest.mark.parametrize(
    ("lines", "error", "message"),
    [
        pytest.param(
            make_pdf()[:1] + ["1 1 obj\n"] + make_pdf()[2:],
            RuntimeError,
            "generation 1 of object 1 in line 2 is not supported",
            id="generation",
        ),
        pytest.param(
            make_pdf()[:1] + ["endstream\n"] + make_pdf()[1:],
            RuntimeError,
            "line 2: endstream without object-start",
            id="endstream-outside-object",
        ),
        pytest.param(
            make_pdf(STREAM_OBJECT.replace("\nstream\n", "\n")),
            RuntimeError,
            "line 14: endstream without stream",
            id="endstream-without-stream",
        ),
        pytest.param(
            make_pdf(xref=""),
            NotImplementedError,
            "startxref without preceding xref-section",
            id="startxref-without-xref",
        ),
        pytest.param(
            [HEADER, EOF],
            RuntimeError,
            "didn't find any PDF objects",
            id="no-object",
        ),
        pytest.param(
            make_pdf(xref="", startxref=""),
            RuntimeError,
            "didn't find a xref-section",
            id="no-xref",
        ),
        pytest.param(
            make_pdf(startxref=""),
            RuntimeError,
            "didn't find a startxref-section",
            id="no-startxref",
        ),
        pytest.param(
            make_pdf(
                STREAM_OBJECT.replace("/Length 00", "/Length 0").replace(
                    "BT ET", "BT /F1 12 Tf ET"
                )
            ),
            RuntimeError,
            "Not enough digits in /Length-entry 0 of object 4",
            id="length-too-short",
        ),
        pytest.param(
            make_pdf(STREAM_OBJECT.replace("/Length 00", "/Length 9 0 R")),
            RuntimeError,
            "obj 4 has unknown length-obj 9",
            id="unknown-length-object",
        ),
        pytest.param(
            make_pdf(
                STREAM_OBJECT.replace("/Length 00", "/Length 5 0 R").replace(
                    "BT ET", "BT /F1 12 Tf ET"
                ),
                "5 0 obj\n0\nendobj\n",
            ),
            RuntimeError,
            "Not enough digits in /Length-ref-entry 0 of object 4",
            id="length-reference-too-short",
        ),
        pytest.param(
            make_pdf(STREAM_OBJECT.replace("/Length 00", "")),
            RuntimeError,
            "obj 4 with stream-len 5 has no object-length-line",
            id="no-length",
        ),
    ],
)
def test_update_lines_invalid_pdf(
    lines: list[str], error: type[Exception], message: str
) -> None:
    with pytest.raises(error, match=message):
        run_update_lines(lines)


def test_read_binary_file(tmp_path: Path) -> None:
    path = tmp_path / "lines.txt"
    path.write_bytes(b"crlf\r\ncr\rlf\n\xe9-no-line-break-at-the-end")

    lines = read_binary_file(path, "iso-8859-1")

    assert lines == [
        "crlf\r\n",
        "cr\r",
        "lf\n",
        "\xe9-no-line-break-at-the-end",
    ]
