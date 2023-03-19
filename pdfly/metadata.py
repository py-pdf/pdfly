"""Show metadata of a PDF file"""

import stat
from datetime import datetime
from pathlib import Path
from typing import Optional, Set

from pydantic import BaseModel
from pypdf import PdfReader

from ._utils import OutputOptions


class MetaInfo(BaseModel):
    title: Optional[str] = None
    producer: Optional[str] = None
    author: Optional[str] = None
    pages: int
    encrypted: bool
    pdf_file_version: str
    page_mode: Optional[str]
    page_layout: Optional[str]

    # OS Information
    file_permissions: str
    file_size: int  # in bytes
    creation_time: datetime
    modification_time: datetime
    access_time: datetime


def main(pdf: Path, output: OutputOptions) -> None:
    reader = PdfReader(str(pdf))
    info = reader.metadata

    reader.stream.seek(0)
    pdf_file_version = reader.stream.read(8).decode("utf-8")
    pdf_stat = pdf.stat()
    meta = MetaInfo(
        pages=len(reader.pages),
        encrypted=reader.is_encrypted,
        page_mode=reader.page_mode,
        pdf_file_version=pdf_file_version,
        page_layout=reader.page_layout,
        # OS Info
        file_permissions=f"{stat.filemode(pdf_stat.st_mode)}",
        file_size=pdf_stat.st_size,
        creation_time=datetime.fromtimestamp(pdf_stat.st_ctime),
        modification_time=datetime.fromtimestamp(pdf_stat.st_mtime),
        access_time=datetime.fromtimestamp(pdf_stat.st_atime),
    )
    if info is not None:
        meta.title = info.title
        meta.producer = info.producer
        meta.author = info.author

    if output == OutputOptions.json:
        print(meta.json())
    else:
        from rich.console import Console
        from rich.table import Table

        table = Table(title="PDF Data")
        table.add_column(
            "Attribute", justify="right", style="cyan", no_wrap=True
        )
        table.add_column("Value", style="white")

        table.add_row("Title", meta.title)
        table.add_row("Producer", meta.producer)
        table.add_row("Author", meta.author)
        table.add_row("Pages", f"{meta.pages:,}")
        table.add_row("Encrypted", f"{meta.encrypted}")
        table.add_row("PDF File Version", meta.pdf_file_version)
        table.add_row("Page Layout", meta.page_layout)
        table.add_row("Page Mode", meta.page_mode)
        embedded_fonts: Set[str] = set()
        unemedded_fonts: Set[str] = set()
        for page in reader.pages:
            emb, unemb = page._get_fonts()
            embedded_fonts = embedded_fonts.union(set(emb))
            unemedded_fonts = unemedded_fonts.union(set(unemb))
        table.add_row("Fonts (unembedded)", ", ".join(sorted(unemedded_fonts)))
        table.add_row("Fonts (embedded)", ", ".join(sorted(embedded_fonts)))

        os_table = Table(title="Operating System Data")
        os_table.add_column(
            "Attribute", justify="right", style="cyan", no_wrap=True
        )
        os_table.add_column("Value", style="white")
        os_table.add_row("File Name", f"{pdf}")
        os_table.add_row("File Permissions", f"{meta.file_permissions}")
        os_table.add_row("File Size", f"{meta.file_size:,} bytes")
        os_table.add_row(
            "Creation Time", f"{meta.creation_time:%Y-%m-%d %H:%M:%S}"
        )
        os_table.add_row(
            "Modification Time", f"{meta.modification_time:%Y-%m-%d %H:%M:%S}"
        )
        os_table.add_row(
            "Access Time", f"{meta.access_time:%Y-%m-%d %H:%M:%S}"
        )

        console = Console()
        console.print(os_table)
        console.print(table)
        console.print(
            "Use the 'pagemeta' subcommand to get details about a single page"
        )
