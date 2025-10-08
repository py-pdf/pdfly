"""
Verifies the signature of a signed PDF.

Examples
    pdfly verify input.pdf --pem certs.pem

        Verifies the input.pdf with a PEM certificate bundle.


"""

import sys
from pathlib import Path
from typing import Optional

import typer
from endesive import pdf


def main(filename: Path, pem: Path, verbose: Optional[bool]) -> None:
    x509_certificates = [pem.read_bytes()]
    results = pdf.verify(filename.read_bytes(), x509_certificates)
    for hash_ok, signature_ok, cert_ok in results:
        if not signature_ok:
            print(f"Signature ok: {signature_ok}", file=sys.stderr)
        elif verbose:
            print(f"Signature ok: {signature_ok}")
        if not hash_ok:
            print(f"Content hash ok: {hash_ok}", file=sys.stderr)
        elif verbose:
            print(f"Content hash ok: {hash_ok}")
        if not cert_ok:
            print(f"Certificate ok: {cert_ok}", file=sys.stderr)
        elif verbose:
            print(f"Certificate ok: {cert_ok}")

    for hash_ok, signature_ok, cert_ok in results:
        if not signature_ok or not hash_ok or not cert_ok:
            print("Failure", file=sys.stderr)
            typer.Exit(code=1)

    print("Success")
