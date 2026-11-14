"""
Verifies the signature of a signed PDF.

Examples
    pdfly verify input.pdf --pem certs.pem

        Verifies the input.pdf with a PEM certificate bundle.


"""

import sys
from pathlib import Path

import typer
from endesive.pdf import PDFVerifier


def main(filename: Path, pem: Path, verbose: bool | None) -> None:
    x509_certificates = [pem.read_bytes()]
    try:
        verifier = PDFVerifier(filename.read_bytes(), x509_certificates)
        if not verifier.is_signed:
            raise typer.BadParameter("Signature missing")
        # Unlike endesive.pdf.verify(), which only checks the last signature
        results = verifier.verify_all_signatures()
    except ValueError as error:  # malformed /ByteRange or signature bytes
        raise typer.BadParameter(f"Invalid signature: {error}") from error

    details: list[str] = []
    for result in results:
        hash_ok, signature_ok, cert_ok = (
            result.hashok,
            result.signatureok,
            result.certok,
        )
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
    for result in results:
        if not (result.signatureok and result.hashok and result.certok):
            print(f"Check failed{details_str}.", file=sys.stderr)
            raise typer.Exit(code=1)

    print(f"Check succeeded{details_str}.")
