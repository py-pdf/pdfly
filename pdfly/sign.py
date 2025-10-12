"""
Creates a signed PDF from an existing PDF file.

Examples
    pdfly sign input.pdf --p12 certs.p12 -o signed.pdf

        Signs the input.pdf with a PKCS12 certificate archive. Writes the resulting signed pdf into signed.pdf.

    pdfly sign document.pdf --p12 certs.p12 --in-place

        Signs the document.pdf with a PKCS12 certificate archive. Modifies the input file in-place.

"""

import io
import tempfile
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from typing import Optional, Union

import fpdf.sign
import typer
from cryptography.hazmat.primitives.serialization import pkcs12
from endesive import signer
from fpdf import FPDF, get_scale_factor
from pypdf import PageObject, PdfReader, PdfWriter
from pypdf.generic import DictionaryObject, PdfObject


def main(
    filename: Path,
    output: Optional[Path],
    in_place: bool,
    p12: Path,
    p12_password: Optional[str],
) -> None:
    validate_output_args_or_raise(output, in_place)

    pdf_reader = PdfReader(filename)
    pdf_is_unsigned_or_raise(pdf_reader)

    output_file: Union[io.BufferedWriter, tempfile._TemporaryFileWrapper]
    if output:
        output_file = open(output, "wb")
    else:
        output_file = tempfile.NamedTemporaryFile(
            delete=False
        )  # will be deleted by output.unlink() later on
        output = Path(output_file.name)

    try:
        _sign_pdf_contents(pdf_reader, output_file, p12, p12_password)
    finally:
        output_file.close()

    if in_place:
        filename.write_bytes(output.read_bytes())
        output.unlink()


def pdf_is_unsigned_or_raise(pdf_reader: PdfReader) -> None:
    for page in pdf_reader.pages:
        if page.annotations is None:
            continue

        if any(is_signature(annotation) for annotation in page.annotations):
            raise typer.BadParameter("PDF is already signed.")


def is_signature(annotation: PdfObject) -> bool:
    resolved_annotation_object = annotation.get_object()
    if resolved_annotation_object is None:
        return False

    if type(resolved_annotation_object) is not DictionaryObject:
        return False

    subtype = resolved_annotation_object["/Subtype"]
    if subtype != "/Widget":
        return False

    fieldtype = resolved_annotation_object["/FT"]
    return fieldtype == "/Sig"


def _sign_pdf_contents(
    pdf_reader: PdfReader,
    output_file: Union[io.BufferedWriter, tempfile._TemporaryFileWrapper],
    p12: Path,
    p12_password: Optional[str],
) -> None:
    unsigned_output_buffer = io.BytesIO()

    with add_to_page(pdf_reader.pages[-1]) as pdf:
        with p12.open("rb") as pkcs_file:
            hashalgo = "sha256"
            sign_time = pdf.creation_date

            key, cert, extra_certs = pkcs12.load_key_and_certificates(
                pkcs_file.read(),
                (p12_password.encode() if p12_password is not None else None),
            )
        pdf.sign(
            key=key,
            cert=cert,
            extra_certs=extra_certs,
            hashalgo=hashalgo,
            signing_time=sign_time,
        )

        # defer actual signing until after the input pdfs contents are merged
        # _sign_key = None prevents FDPF.output() from calculating the signature hash too early
        pdf._sign_key = None

    writer = PdfWriter()
    writer.append_pages_from_reader(pdf_reader)
    writer.write(unsigned_output_buffer)

    # Now that output_buffer contains the contents to be signed
    # we can generate the cryptographic signature using fpdf2.sign.sign_content

    # patch placeholder values to match how fpdf.sign.sign_content() expects them
    content_to_sign = bytearray(unsigned_output_buffer.getbuffer())
    content_to_sign = content_to_sign.replace(
        _SIGNATURE_BYTERANGE_PLACEHOLDER.encode(),
        fpdf.sign._SIGNATURE_BYTERANGE_PLACEHOLDER.encode(),
    )
    content_to_sign = content_to_sign.replace(
        b"(" + _SIGNATURE_CONTENTS_PLACEHOLDER.encode() + b")",
        b"<" + fpdf.sign._SIGNATURE_CONTENTS_PLACEHOLDER.encode() + b">",
    )

    signed_output_buffer = fpdf.sign.sign_content(
        signer,
        content_to_sign,
        key,
        cert,
        extra_certs,
        hashalgo,
        sign_time,
    )
    output_file.write(signed_output_buffer)


@contextmanager
def add_to_page(reader_page: PageObject, unit: str = "mm") -> Generator[FPDF]:
    k = get_scale_factor(unit)
    format = (reader_page.mediabox[2] / k, reader_page.mediabox[3] / k)
    pdf = FPDF(format=format, unit=unit)
    pdf.add_page()
    yield pdf
    page_overlay = PdfReader(io.BytesIO(pdf.output())).pages[0]
    reader_page.merge_page(page2=page_overlay)


def validate_output_args_or_raise(
    output: Optional[Path], in_place: bool
) -> None:
    if not in_place and output is None:
        raise typer.BadParameter(
            "One of the options --output or --in-place is required."
        )


# fpdf.sign placeholder values - in the form after PdfWriter serialized them
_SIGNATURE_BYTERANGE_PLACEHOLDER = "[ 0 0 0 0 ]"
_SIGNATURE_CONTENTS_PLACEHOLDER = "\\000" * 0x2000
