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

    if len(results) == 0:
        raise typer.BadParameter("Signature missing")

    details: list[str] = []
    for hash_ok, signature_ok, cert_ok in results:
        if not signature_ok:
            details.append("Signature not ok")
        elif verbose:
            details.append("Signature ok")
        if not hash_ok:
            details.append("Content hash not ok")
        elif verbose:
            details.append("Content hash ok")
        if not cert_ok:
            details.append("Certificate not ok")
        elif verbose:
            details.append("Certificate ok")

    details_str = "" if len(details) == 0 else " (" + ", ".join(details) + ")"
    for hash_ok, signature_ok, cert_ok in results:
        if not signature_ok or not hash_ok or not cert_ok:
            print(f"Check failed{details_str}.", file=sys.stderr)
            raise typer.Exit(code=1)

    print(f"Check succeeded{details_str}.")
