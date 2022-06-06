"""Show metadata of a PDF file"""

from enum import Enum
from pathlib import Path
from typing import Optional, Tuple

from pydantic import BaseModel
from PyPDF2 import PdfReader


class MetaInfo(BaseModel):
    title: Optional[str] = None
    producer: Optional[str] = None
    pages: int
    encrypted: bool
    file_size: int  # in bytes
    page_size: Tuple[float, float]  # (width, height)
    pdf_file_version: str
    page_mode: Optional[str]
    page_layout: Optional[str]


class OutputOptions(Enum):
    json = "json"
    text = "text"


def main(pdf: Path, output: OutputOptions) -> None:
    with open(pdf, "rb") as f:
        reader = PdfReader(f)
        info = reader.metadata
        x1, y1, x2, y2 = reader.pages[0].mediabox

        reader.stream.seek(0)
        pdf_file_version = reader.stream.readline().decode()
        meta = MetaInfo(
            pages=len(reader.pages),
            encrypted=reader.is_encrypted,
            file_size=pdf.stat().st_size,
            page_size=(x2 - x1, y2 - y1),
            page_mode=reader.page_mode,
            pdf_file_version=pdf_file_version,
            page_layout=reader.page_layout,
        )
        if info is not None:
            meta.title = info.title
            meta.producer = info.producer

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
        table.add_row("Page Layout", meta.page_layout)
        table.add_row("Page Mode", meta.page_mode)

        console = Console()
        console.print(table)
