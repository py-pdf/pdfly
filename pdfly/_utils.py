import sys
from enum import Enum

from pypdf import PasswordType, PdfReader
from rich.console import Console


class OutputOptions(Enum):
    json = "json"
    text = "text"

def decrypt_or_exit(
    reader: PdfReader, password: str | None, console: Console
) -> None:
    """Decrypt reader with password, or print the standard error and exit(1)."""
    if (
        password is not None
        and reader.decrypt(password) == PasswordType.NOT_DECRYPTED
    ):
        console.print(
            "[red]Error: the decrypting password provided is invalid"
        )
        sys.exit(1)
