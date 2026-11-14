"""
Remove password protection from an encrypted PDF file.

The decrypted PDF is written to OUTPUT_FILE. If OUTPUT_FILE is omitted,
the PDF is written to standard output, so the command can be used in pipes.

Examples
    pdfly decrypt encrypted.pdf decrypted.pdf

    pdfly decrypt --password secret encrypted.pdf > decrypted.pdf

    pdfly decrypt < encrypted.pdf > decrypted.pdf

"""

import sys
from io import BytesIO
from pathlib import Path
from typing import NoReturn

import typer
from pypdf import PasswordType, PdfReader, PdfWriter


def main(
    input_file: Path | None,
    output_file: Path | None,
    password: str | None,
) -> None:
    if input_file is None or str(input_file) == "-":
        data = sys.stdin.buffer.read()
    else:
        input_file = Path(input_file)
        if not input_file.is_file():
            error(f"Input file not found: {input_file}")
        data = input_file.read_bytes()

    reader = PdfReader(BytesIO(data))
    if not reader.is_encrypted:
        # Pass unencrypted files through unchanged, so filter chains
        # do not break unexpectedly.
        write_data(data, output_file)
        return

    if password is None:
        # Many encrypted PDFs use an empty user password.
        decrypted = try_decrypt(reader, "")
        if decrypted == PasswordType.NOT_DECRYPTED:
            error(
                "The PDF is encrypted. Please provide the password"
                " using --password."
            )
    else:
        decrypted = try_decrypt(reader, password)
        if decrypted == PasswordType.NOT_DECRYPTED:
            error("Invalid password.")

    writer = PdfWriter(clone_from=reader)
    # pypdf needs to seek in the stream it writes to, and stdout can be a
    # pipe, so the PDF is first written to a buffer, then copied to stdout.
    buffer = BytesIO()
    writer.write(buffer)
    write_data(buffer.getvalue(), output_file)


def try_decrypt(reader: PdfReader, password: str) -> PasswordType:
    try:
        return reader.decrypt(password)
    except Exception:
        return PasswordType.NOT_DECRYPTED


def error(message: str) -> NoReturn:
    print(f"Error: {message}", file=sys.stderr)
    raise typer.Exit(code=1)


def write_data(data: bytes, output_file: Path | None) -> None:
    if output_file is None or str(output_file) == "-":
        sys.stdout.flush()
        sys.stdout.buffer.write(data)
        sys.stdout.buffer.flush()
    else:
        Path(output_file).write_bytes(data)
