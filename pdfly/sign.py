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
from contextlib import contextmanager
from pathlib import Path
from typing import Generator, Optional, Union

import fpdf.sign
import typer
from endesive import signer
from fpdf import FPDF, get_scale_factor
from pypdf import PageObject, PdfReader, PdfWriter


def main(
    filename: Path,
    output: Optional[Path],
    in_place: bool,
    p12: Optional[Path],
    p12_password: Optional[str],
) -> None:
    validate_output_args_or_raise(output, in_place)

    with open(filename, "rb") as input_file:
        unsigned_output_buffer = io.BytesIO()

        output_file: Union[
            io.BufferedWriter, tempfile._TemporaryFileWrapper[bytes]
        ]
        if output:
            output_file = open(output, "wb")
        else:
            output_file = tempfile.NamedTemporaryFile(delete_on_close=False)
            output = Path(output_file.name)

        try:
            sign_key = None
            sign_cert = None
            sign_extra_certs = None
            sign_hashalgo = None
            sign_time = None

            reader = PdfReader(input_file)

            with add_to_page(reader.pages[-1]) as pdf:
                pdf.sign_pkcs12(
                    p12,
                    (
                        p12_password.encode()
                        if p12_password is not None
                        else None
                    ),
                )

                sign_key = pdf._sign_key
                sign_cert = pdf._sign_cert
                sign_extra_certs = pdf._sign_extra_certs
                sign_hashalgo = pdf._sign_hashalgo
                sign_time = pdf._sign_time

                # defer actual signing until after the input pdfs contents are merged
                # _sign_key = None prevents FDPF.output() from calculating the signature hash too early
                pdf._sign_key = None

            writer = PdfWriter()
            writer.append_pages_from_reader(reader)
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
                b"<"
                + fpdf.sign._SIGNATURE_CONTENTS_PLACEHOLDER.encode()
                + b">",
            )

            signed_output_buffer = fpdf.sign.sign_content(
                signer,
                content_to_sign,
                sign_key,
                sign_cert,
                sign_extra_certs,
                sign_hashalgo,
                sign_time,
            )

            output_file.write(signed_output_buffer)
        except Exception as error:
            raise RuntimeError(f"Error while reading {filename}") from error
        finally:
            output_file.close()

    if in_place:
        filename.write_bytes(output.read_bytes())
        output.unlink()


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
