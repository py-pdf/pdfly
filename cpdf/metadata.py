"""Show metadata of a PDF file"""

from enum import Enum
from pathlib import Path
from typing import Optional, Tuple

from pydantic import BaseModel
from PyPDF2 import PdfFileReader


class MetaInfo(BaseModel):
    title: Optional[str] = None
    producer: Optional[str] = None
    pages: int
    encrypted: bool
    file_size: int  # in bytes
    page_size: Tuple[float, float]  # (width, height)
    pdf_file_version: str


class OutputOptions(Enum):
    json = "json"
    text = "text"


def main(pdf: Path, output: OutputOptions) -> None:
    with open(pdf, "rb") as f:
        reader = PdfFileReader(f)
        info = reader.getDocumentInfo()
        x1, y1, x2, y2 = reader.getPage(0).mediaBox

        reader.stream.seek(0)
        pdf_file_version = reader.stream.readline().decode()

        meta = MetaInfo(
            title=info.title,
            producer=info.producer,
            pages=reader.getNumPages(),
            encrypted=reader.isEncrypted,
            file_size=pdf.stat().st_size,
            page_size=(x2 - x1, y2 - y1),
            pdf_file_version=pdf_file_version,
        )

    if output == OutputOptions.json:
        print(meta.json())
    else:
        from rich.console import Console
        from rich.table import Table

        table = Table(title=f"{pdf}")
        table.add_column("Attribute", justify="right", style="cyan", no_wrap=True)
        table.add_column("Value", style="white")

        table.add_row("Title", meta.title)
        table.add_row("Producer", meta.producer)
        table.add_row("Pages", f"{meta.pages:,}")
        table.add_row("Encrypted", f"{meta.encrypted}")
        table.add_row("File size", f"{meta.file_size:,} bytes")
        table.add_row(
            "Page size", f"{meta.page_size[0]} x {meta.page_size[1]} pts (w x h)"
        )
        table.add_row("PDF File Version", meta.pdf_file_version)

        console = Console()
        console.print(table)
